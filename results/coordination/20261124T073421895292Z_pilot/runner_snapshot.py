"""Reproducible, sequential baseline/E02 checks. No edits to the source model."""
import argparse
import csv
import hashlib
import json
import os
import platform
import re
import subprocess
import shutil
import tempfile
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import psutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'models/08_final_version.xml'
PROPERTIES = {
    'P01': ('Success reachable', 'E<> Supervisor.Done'),
    'P02': ('ARM prerequisite', 'A[] forall (i : drone_id) (armed[i] imply missionInstalled[i])'),
    'P03': ('START prerequisite', 'A[] forall (i : drone_id) (started[i] imply armed[i])'),
    'P04': ('Success requires START evidence', 'A[] (Supervisor.Done imply forall (i : drone_id) cmdAccepted[i][START])'),
    'P05': ('No pre-outcome deadlock', 'A[] (deadlock imply (Supervisor.Done || Supervisor.Aborted))'),
    'P06': ('Admitted packet eventually leaves', 'Link.Transmitting --> Link.Idle'),
    'P07': ('Service time window', 'A[] ((Link.Delivered || Link.Lost) imply (Link.t >= D_MIN && Link.t <= D_MAX))'),
    'P08': ('Drone 0 timeout exhaustion reachable', 'E<> CommandClient(0).Failed'),
    'P09': ('Drone 0 retry reachable', 'E<> (CommandClient(0).retries > 0)'),
    'P10': ('ARM executed despite failed confirmation', 'E<> (cmdFailed[0][ARM] && armed[0])'),
    'P11': ('ARM not yet executed at failed confirmation', 'E<> (cmdFailed[0][ARM] && !armed[0])'),
    'P12': ('Loss reachable', 'E<> Link.Lost'),
    'P13': ('Success agrees with drone states', 'A[] (Supervisor.Done imply forall (i : drone_id) started[i])'),
    'P14': ('Confirmed missions contain every item', 'A[] ((uploadDone[0] imply (missionInstalled[0] && Drone0.receivedCount == MISSION_SIZE)) && (uploadDone[1] imply (missionInstalled[1] && Drone1.receivedCount == MISSION_SIZE)) && (uploadDone[2] imply (missionInstalled[2] && Drone2.receivedCount == MISSION_SIZE)))'),
    'P15': ('Any drone failure reachable', 'E<> exists (i : drone_id) cmdFailed[i][ARM] || exists (i : drone_id) cmdFailed[i][START]'),
    'P16': ('Prepared fleet eventually reaches an outcome', 'Supervisor.Prepared --> (Supervisor.Done || Supervisor.Aborted)'),
}
OPTIONS = ['-s', '-u', '-o', '0', '--state-representation', '1', '-S', '1', '-n', '0', '-r', '1']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def make_model(dmax, timeout):
    text = SOURCE.read_text(encoding='utf-8')
    for name, value in [('D_MAX', dmax), ('ACK_TIMEOUT', timeout)]:
        text, count = re.subn(rf'const int {name} = \d+;', f'const int {name} = {value};', text)
        if count != 1:
            raise ValueError(f'Expected exactly one declaration for {name}')
    original = ET.fromstring(SOURCE.read_text(encoding='utf-8'))
    generated = ET.fromstring(text)
    # Guard against accidental template/system changes.
    for tag in ['template', 'system', 'queries']:
        assert [ET.tostring(x) for x in original.findall(tag)] == [ET.tostring(x) for x in generated.findall(tag)]
    assert 'const bool LOSSY = false;' in generated.findtext('declaration')
    return text

def run_one(command, folder, limit, memory_bytes, cwd):
    start = time.monotonic()
    reason = None
    sampled_peak = 0
    with (folder / 'stdout.log').open('wb') as out, (folder / 'stderr.log').open('wb') as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, cwd=cwd)
        monitor = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                sampled_peak = max(sampled_peak, monitor.memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            if time.monotonic() - start >= limit:
                reason = 'timeout'
            elif sampled_peak >= memory_bytes:
                reason = 'memory_limit'
            if reason:
                process.kill()
                process.wait()
                break
            time.sleep(0.05)
    elapsed = time.monotonic() - start
    output = '\n'.join((folder / n).read_text(encoding='utf-8', errors='replace') for n in ['stdout.log', 'stderr.log'])
    if reason:
        result = reason
    elif process.returncode != 0 or 'Failed to retrieve license' in output:
        result = 'tool_error'
    elif re.search(r'Formula is NOT satisfied', output):
        result = 'not_satisfied'
    elif re.search(r'Formula is satisfied', output):
        result = 'satisfied'
    else:
        result = 'unknown'
    metrics = {}
    for key, pattern in [('explored_states', r'States explored\s*:\s*(\d+)'), ('stored_states', r'States stored\s*:\s*(\d+)')]:
        match = re.search(pattern, output, re.I)
        metrics[key] = int(match.group(1)) if match else None
    return dict(result=result, wall_seconds=round(elapsed, 4), returncode=process.returncode,
                sampled_peak_rss_bytes=sampled_peak, **metrics)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifyta', default=os.environ.get('UPPAAL_VERIFYTA'))
    parser.add_argument('--suite', choices=['pilot', 'baseline', 'E02'], default='pilot')
    parser.add_argument('--properties', nargs='+', choices=list(PROPERTIES))
    parser.add_argument('--limit', type=float, default=120)
    parser.add_argument('--memory-gib', type=float, default=8)
    parser.add_argument('--repetition', type=int, default=1)
    parser.add_argument('--trace', action='store_true')
    parser.add_argument('--dmax', type=int)
    parser.add_argument('--ack-timeout', type=int)
    args = parser.parse_args()
    if not args.verifyta or not Path(args.verifyta).is_file():
        parser.error('Provide --verifyta or UPPAAL_VERIFYTA pointing to verifyta.exe')
    if args.limit <= 0 or args.memory_gib <= 0:
        parser.error('Resource limits must be positive')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    outdir = ROOT / 'results/coordination' / f'{stamp}_{args.suite}'
    outdir.mkdir(parents=True, exist_ok=False)
    version = subprocess.run([args.verifyta, '--version'], capture_output=True, text=True, timeout=30)
    (outdir / 'tool_version.log').write_text(version.stdout + version.stderr, encoding='utf-8')
    if version.returncode or 'Failed to retrieve license' in version.stdout + version.stderr:
        raise SystemExit(f'Verifier preflight failed; see {outdir}')
    tool_version = next((line for line in version.stdout.splitlines() if line.startswith('UPPAAL')), version.stdout.strip())
    metadata = dict(run_id=stamp, suite=args.suite, source_model_sha256=sha(SOURCE),
                    git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    runner_sha256=sha(Path(__file__)), tool_version=tool_version,
                    verifyta_path=args.verifyta, verifyta_sha256=sha(Path(args.verifyta)),
                    platform=platform.platform(), cpu=platform.processor(),
                    logical_cpus=os.cpu_count(), physical_memory_bytes=psutil.virtual_memory().total,
                    search_options=OPTIONS, trace_enabled=args.trace, time_limit_seconds=args.limit,
                    memory_limit_bytes=int(args.memory_gib * 1024**3), repetition=args.repetition,
                    rss_measurement='Verifier RSS sampled every 50 ms; lower bound on peak, excludes GUI/runner',
                    liveness_summary_note='verifyta -u warns that summary statistics are incorrect for liveness; state counts omitted for leads-to queries')
    write_json(outdir / 'manifest.json', metadata)
    shutil.copyfile(Path(__file__), outdir / 'runner_snapshot.py')
    configs = [(3, 14)] if args.suite != 'E02' else [(d, t) for d in [2, 3, 5] for t in [6, 14, 24]]
    if args.dmax is not None or args.ack_timeout is not None:
        configs = [(args.dmax or 3, args.ack_timeout or 14)]
    ids = args.properties or (['P01'] if args.suite == 'pilot' else list(PROPERTIES) if args.suite == 'baseline' else ['P01', 'P02', 'P03', 'P04', 'P05', 'P08', 'P09', 'P15'])
    rows = []
    print(f'OUTPUT {outdir}', flush=True)
    for dmax, timeout in configs:
        cid = f'dmax{dmax}_timeout{timeout}'
        config_dir = outdir / cid
        config_dir.mkdir()
        model = config_dir / 'model.xml'
        model.write_text(make_model(dmax, timeout), encoding='utf-8', newline='')
        for pid in ids:
            folder = config_dir / pid
            folder.mkdir()
            title, formula = PROPERTIES[pid]
            query = folder / 'query.q'
            query.write_text(f'// {pid}: {title}\n{formula}\n', encoding='utf-8')
            command = [str(Path(args.verifyta).resolve()), *OPTIONS]
            if args.trace:
                # Plain diagnostic text is robust; this beta's -X XML export crashes.
                command += ['-t', '0']
            command += ['model.xml', 'query.q']
            write_json(folder / 'command.json', command)
            print(f'RUN {cid} {pid}', flush=True)
            # Native verifyta rejects Unicode paths on this Windows installation.
            # Stage byte-identical inputs in an ASCII directory; archive outputs here.
            with tempfile.TemporaryDirectory(prefix='uppaal_experiment_') as scratch:
                scratch = Path(scratch)
                if not str(scratch).isascii():
                    raise RuntimeError('Set TEMP to an ASCII-only directory')
                shutil.copyfile(model, scratch / 'model.xml')
                shutil.copyfile(query, scratch / 'query.q')
                assert sha(scratch / 'model.xml') == sha(model)
                assert sha(scratch / 'query.q') == sha(query)
                write_json(folder / 'execution.json', {'cwd': str(scratch), 'staged_model': str(model), 'staged_query': str(query)})
                result = run_one(command, folder, args.limit, metadata['memory_limit_bytes'], scratch)
                for trace in scratch.glob('trace*'):
                    shutil.copyfile(trace, folder / trace.name)
            if '-->' in formula:
                result['explored_states'] = result['stored_states'] = None
            row = dict(experiment_id=args.suite, configuration_id=cid, property_id=pid,
                       N=3, mission_size=3, d_min=1, d_max=dmax, ack_timeout=timeout, max_retry=2,
                       loss_mode='reliable', heartbeat_mode='inactive', model_sha256=sha(model),
                       query_sha256=sha(query), query=formula, log_path=str(folder.relative_to(ROOT)),
                       **metadata, **result)
            write_json(folder / 'result.json', row)
            rows.append(row)
            with (outdir / 'summary.csv').open('w', encoding='utf-8-sig', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(row))
                writer.writeheader()
                writer.writerows(rows)
            print(f"RESULT {cid} {pid} {result['result']} {result['wall_seconds']}s", flush=True)
            if result['result'] in ['tool_error', 'unknown']:
                raise SystemExit(f'Unexpected verifier output; inspect {folder}')
    assert sha(SOURCE) == metadata['source_model_sha256']
    print(f'COMPLETE {len(rows)} query invocations: {outdir}', flush=True)

if __name__ == '__main__':
    main()
