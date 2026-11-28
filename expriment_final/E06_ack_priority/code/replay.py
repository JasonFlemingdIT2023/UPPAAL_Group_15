"""Run the packaged UPPAAL cases using their original verifier options."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from run_coordination_experiments import ROOT, run_one, write_json


def run_case(row, verifier, target, limit):
    target.mkdir(parents=True, exist_ok=False)
    memory = int(row['memory_limit_bytes'])
    options = json.loads(row['verifyta_options'])
    command = [str(verifier), *options, 'model.xml', 'query.q']
    with tempfile.TemporaryDirectory(prefix='uppaal_replay_') as directory:
        if not directory.isascii():
            raise ValueError('Set TEMP/TMP to a writable ASCII-only directory.')
        scratch = Path(directory)
        shutil.copyfile(ROOT/row['model'], scratch/'model.xml')
        shutil.copyfile(ROOT/row['query_file'], scratch/'query.q')
        outcome = run_one(command, target, limit, memory, scratch)
        for trace in scratch.glob('trace*'):
            shutil.copyfile(trace, target/trace.name)
    formula = (ROOT/row['query_file']).read_text(encoding='utf-8')
    if '-->' in formula or any(line.lstrip().startswith('A<>') for line in formula.splitlines()):
        for field in ('explored_states', 'stored_states', 'cpu_user_ms', 'reported_resident_kib'):
            outcome[field] = None
    write_json(target/'result.json', dict(outcome, case=row, effective_time_limit_seconds=limit))
    return outcome['result']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='List runs and property IDs.')
    group.add_argument('--all', action='store_true', help='Replay the study, including timed-out cases.')
    group.add_argument('--run', help='Select a specific run ID.')
    parser.add_argument('--property', help='Filter by property ID.')
    parser.add_argument('--configuration', help='Filter by configuration ID.')
    parser.add_argument('--verifyta', default=os.environ.get('UPPAAL_VERIFYTA'))
    parser.add_argument('--limit', type=float, help='Override the per-query wall-clock limit.')
    args = parser.parse_args()
    with (ROOT/'code/cases.csv').open(encoding='utf-8', newline='') as stream:
        cases = [r for r in csv.DictReader(stream)
                 if (not args.run or r['run'] == args.run)
                 and (not args.property or r['property'] == args.property)
                 and (not args.configuration or r['configuration'] == args.configuration)
                 and (not args.all or r['include_in_batch'] == 'True')]
    if not cases:
        parser.error('No cases match the selection.')
    if args.list:
        for run in sorted({r['run'] for r in cases}):
            selected = [r for r in cases if r['run'] == run]
            print(run, len(selected), ','.join(sorted({r['property'] for r in selected})))
        return
    if not args.verifyta or not Path(args.verifyta).is_file():
        parser.error('Set UPPAAL_VERIFYTA or pass --verifyta PATH.')
    if args.limit is not None and args.limit <= 0:
        parser.error('--limit must be positive.')
    verifier = Path(args.verifyta).resolve()
    version = subprocess.run([str(verifier), '--version'], capture_output=True, text=True, timeout=30)
    if version.returncode:
        raise SystemExit(version.stderr or version.stdout)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = ROOT/'results/reproduced'/f'{stamp}_replay'
    output.mkdir(parents=True)
    write_json(output/'manifest.json', dict(version=version.stdout + version.stderr, selected_cases=len(cases)))
    print(f'OUTPUT {output}', flush=True)
    outcomes = Counter()
    for number, case in enumerate(cases, start=1):
        limit = args.limit if args.limit is not None else float(case['limit_seconds'])
        target = output / f"{number:04d}_{case['property']}"
        status = run_case(case, verifier, target, limit)
        outcomes[status] += 1
        print(case['run'], case['configuration'], case['property'], status, flush=True)
    write_json(output/'summary.json', dict(outcomes))
    if outcomes['tool_error'] or outcomes['unknown']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
