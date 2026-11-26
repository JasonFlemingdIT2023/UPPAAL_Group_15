"""Reproducible baseline and E01-E06 checks. Source model is read-only."""
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
SOURCE = ROOT / 'code/models/08_final_version.xml'
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
    'P17': ('ARM accepted after timeout-triggered retry counter increment', 'E<> (cmdAccepted[0][ARM] && CommandClient(0).current == ARM && CommandClient(0).retries > 0)'),
    'P18': ('ARM still absent at a quiescent aborted outcome', 'E<> (Supervisor.Aborted && Link.Idle && CommandClient(0).Failed && CommandClient(1).Idle && CommandClient(2).Idle && CommandServer(0).Idle && CommandServer(1).Idle && CommandServer(2).Idle && !armed[0] && cmdFailed[0][ARM])'),
    'P19': ('Command request loss reachable', 'E<> (Link.Lost && Link.packet.kind == PK_COMMAND)'),
    'P20': ('Command acknowledgement loss reachable', 'E<> (Link.Lost && (Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))'),
    'P21': ('Mission-message loss unreachable', 'A[] (Link.Lost imply (Link.packet.kind == PK_COMMAND || Link.packet.kind == PK_ACCEPTED || Link.packet.kind == PK_DENIED))'),
}
PROPERTIES['P22'] = ('Unexecuted ARM after confirmation failure eventually executes', '(cmdFailed[0][ARM] && !armed[0]) --> armed[0]')
PROPERTIES['P23'] = ('Any drone retry counter increment reachable', 'E<> (CommandClient(0).retries > 0 || CommandClient(1).retries > 0 || CommandClient(2).retries > 0)')
PROPERTIES['P24'] = ('Every drone heartbeat can be observed', 'E<> forall (i : drone_id) heartbeatSeen[i]')
PROPERTIES['P25'] = ('Prepared fleet inevitably succeeds', 'Supervisor.Prepared --> Supervisor.Done')
PROPERTIES['P26'] = ('Unconditional eventual success from initialization', 'A<> Supervisor.Done')
PROPERTIES['P27'] = ('Global loss budget respected', 'A[] Link.lossCount <= LOSS_BUDGET')
PROPERTIES['P28'] = ('Success after consuming the entire loss budget reachable', 'E<> (Supervisor.Done && Link.lossCount == LOSS_BUDGET)')
PROPERTIES['P29'] = ('ACK pending flags exactly reflect server reply states', 'A[] (ackPending[0] == CommandServer(0).Decide)')
for _i in range(4):
    PROPERTIES[f'P{30+_i}'] = (f'Drone {_i} pending heartbeat eventually gains admission', f'HBSender({_i}).Pending --> HBSender({_i}).Waiting')
PROPERTIES['P34'] = ('Success with every heartbeat observed reachable', 'E<> (Supervisor.Done && forall (i : drone_id) heartbeatSeen[i])')
PROPERTIES['P35'] = ('No drone exhausts command retries', 'A[] forall (i : drone_id) (!cmdFailed[i][ARM] && !cmdFailed[i][START])')
PROPERTIES['P36'] = ('No command retry counter increment', 'A[] (CommandClient(0).retries == 0)')
PROPERTIES['P37'] = ('Every admitted command waits at most two packet service windows for reply', 'A[] (CommandClient(0).WaitAck imply CommandClient(0).x <= 2 * D_MAX)')
PROPERTIES['P38'] = ('A START ACK is delivered exactly two maximum service windows after admission', 'E<> (Link.Delivered && Link.packet.kind == PK_ACCEPTED && Link.packet.peer == 0 && Link.packet.cmd == START && cmdAccepted[0][START] && CommandClient(0).x == 2 * D_MAX)')
for _i in range(3):
    PROPERTIES[f'P{39+_i}'] = (f'Drone {_i} dispatched command eventually completes', f'CommandClient({_i}).Sending --> CommandClient({_i}).Idle')
PROPERTIES['P42'] = ('Arming phase eventually completes', 'Supervisor.Arming --> Supervisor.Starting')
PROPERTIES['P43'] = ('Starting phase eventually completes', 'Supervisor.Starting --> Supervisor.Done')
PROPERTIES['P44'] = ('Prepared phase eventually starts arming', 'Supervisor.Prepared --> Supervisor.Arming')
PROPERTIES['P45'] = ('No deadlock with heartbeat active', 'A[] !deadlock')
PROPERTIES['P46'] = ('In-flight mission packets have a matching receiver', '')
OPTIONS = ['-s', '-u', '-o', '0', '--state-representation', '1', '-S', '1', '-n', '0', '-r', '1']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def property_for(pid, n):
    title, formula = PROPERTIES[pid]
    if pid == 'P14':
        clauses = [f'(uploadDone[{i}] imply (missionInstalled[{i}] && Drone{i}.receivedCount == MISSION_SIZE))' for i in range(n)]
        formula = 'A[] (' + ' && '.join(clauses) + ')'
    elif pid == 'P18':
        parts = ['Supervisor.Aborted', 'Link.Idle', 'CommandClient(0).Failed']
        parts += [f'CommandClient({i}).Idle' for i in range(1, n)]
        parts += [f'CommandServer({i}).Idle' for i in range(n)]
        parts += ['!armed[0]', 'cmdFailed[0][ARM]']
        formula = 'E<> (' + ' && '.join(parts) + ')'
    elif pid == 'P23':
        formula = 'E<> (' + ' || '.join(f'CommandClient({i}).retries > 0' for i in range(n)) + ')'
    elif pid == 'P29':
        formula = 'A[] (' + ' && '.join(f'(ackPending[{i}] == CommandServer({i}).Decide)' for i in range(n)) + ')'
    elif pid == 'P36':
        formula = 'A[] (' + ' && '.join(f'CommandClient({i}).retries == 0' for i in range(n)) + ')'
    elif pid == 'P37':
        formula = 'A[] (' + ' && '.join(f'(CommandClient({i}).WaitAck imply CommandClient({i}).x <= 2 * D_MAX)' for i in range(n)) + ')'
    elif pid == 'P46':
        clauses = []
        for i in range(n):
            clause = (
                f'(Link.packet.kind == PK_COUNT imply Drone{i}.WaitCount) && '
                f'((Link.packet.kind == PK_REQUEST || Link.packet.kind == PK_MISSION_ACK) imply Sender{i}.WaitRequest) && '
                f'(Link.packet.kind == PK_ITEM imply (Drone{i}.WaitItem && Drone{i}.nextSequence == Link.packet.seq))'
            )
            clauses.append(f'(Link.packet.peer == {i} imply ({clause}))')
        formula = 'A[] (Link.Transmitting imply (' + ' && '.join(clauses) + '))'
    return title, formula


def make_model(dmax, timeout, loss_mode=None, n=None, heartbeat='inactive', hb_period=20, hb_offsets='synchronous', max_retry=2, loss_budget=None, scheduler='original'):
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
    if loss_mode == 'legacy_both':
        text = text.replace('const bool LOSSY = false;', 'const bool LOSSY = true;')
    elif loss_mode is not None:
        commands, acks = {'reliable': (False, False), 'request': (True, False), 'reply': (False, True), 'both': (True, True)}[loss_mode]
        old_guard = 'LOSSY && t >= D_MIN && (packet.kind == PK_COMMAND || packet.kind == PK_ACCEPTED || packet.kind == PK_DENIED)'
        new_guard = 't >= D_MIN && ((DROP_COMMANDS && packet.kind == PK_COMMAND) || (DROP_ACKS && (packet.kind == PK_ACCEPTED || packet.kind == PK_DENIED)))'
        old_encoded, new_encoded = (g.replace('&', '&amp;').replace('>', '&gt;') for g in [old_guard, new_guard])
        assert text.count(old_encoded) == 1
        declarations = f'const bool DROP_COMMANDS = {str(commands).lower()};\nconst bool DROP_ACKS = {str(acks).lower()};'
        text = text.replace('const bool LOSSY = false;', declarations).replace(old_encoded, new_encoded)
        # Revert precisely the permitted changes and require identical baseline bytes.
        assert text.replace(declarations, 'const bool LOSSY = false;').replace(new_encoded, old_encoded) == make_model(dmax, timeout)
        ET.fromstring(text)
    if n is not None:
        if not 1 <= n <= 4:
            raise ValueError('Validated fleet sizes are 1..4')
        before = ET.fromstring(text)
        text, count = re.subn(r'const int N = 3;', f'const int N = {n};', text)
        assert count == 1
        declarations = ['Supervisor = GCSSupervisor();']
        declarations += [f'Sender{i} = MissionSender({i});' for i in range(n)]
        declarations += [f'Drone{i} = MissionReceiver({i});' for i in range(n)]
        declarations += ['Link = PacketNetwork();']
        instances = ['Supervisor'] + [f'Sender{i}' for i in range(n)] + [f'Drone{i}' for i in range(n)]
        instances += ['Link', 'CommandClient', 'CommandServer']
        declarations += ['system ' + ', '.join(instances) + ';']
        text, count = re.subn(r'<system>.*?</system>', '<system>\n' + '\n'.join(declarations) + '\n</system>', text, flags=re.S)
        assert count == 1
        # Inherited embedded queries mention three drones and inactive heartbeats.
        # External, per-configuration query files are the experiment's actual suite.
        text, count = re.subn(r'<queries>.*?</queries>', '<queries><query><formula>E&lt;&gt; Supervisor.Done</formula><comment>Safe GUI starter; experiment uses external queries.q.</comment></query></queries>', text, flags=re.S)
        assert count == 1
        after = ET.fromstring(text)
        assert [ET.tostring(t) for t in before.findall('template')] == [ET.tostring(t) for t in after.findall('template')]
        assert after.findtext('declaration').replace(f'const int N = {n};', 'const int N = 3;') == before.findtext('declaration')
    if heartbeat == 'active':
        if n is None:
            raise ValueError('Active-heartbeat variants require an explicit fleet size')
        old = 'Link, CommandClient, CommandServer;'
        new = 'Link, CommandClient, CommandServer, HBSender, ConnectionMonitor;'
        assert text.count(old) == 1
        text = text.replace(old, new)
        assert text.replace(new, old) == make_model(dmax, timeout, loss_mode, n)
    if hb_period != 20:
        assert hb_period > 0 and text.count('const int HB_PERIOD = 20;') == 1
        text = text.replace('const int HB_PERIOD = 20;', f'const int HB_PERIOD = {hb_period};')
    if hb_offsets == 'staggered':
        if heartbeat != 'active' or n is None:
            raise ValueError('Staggered first releases require active heartbeats and explicit N')
        match = re.search(r'<template>\s*<name>HBSender</name>.*?</template>', text, re.S)
        assert match
        original = match.group(0)
        modified = original
        changes = [
            ('clock period;', 'clock period;\nint[0, HB_PERIOD] firstOffset = id * HB_PERIOD / N;'),
            ('period &lt;=HB_PERIOD', 'period &lt;=HB_PERIOD + firstOffset'),
            ('period &gt;= HB_PERIOD', 'period &gt;= HB_PERIOD + firstOffset'),
            ('period = 0', 'period = 0, firstOffset = 0'),
        ]
        for old, new in changes:
            assert modified.count(old) == 1
            modified = modified.replace(old, new)
        text = text[:match.start()] + modified + text[match.end():]
        assert text.replace(modified, original) == make_model(dmax, timeout, loss_mode, n, heartbeat, hb_period)
        ET.fromstring(text)
    if max_retry != 2:
        assert max_retry >= 0 and text.count('const int MAX_RETRY = 2;') == 1
        text = text.replace('const int MAX_RETRY = 2;', f'const int MAX_RETRY = {max_retry};')
    if loss_budget is not None:
        if loss_mode != 'legacy_both' or loss_budget < 0:
            raise ValueError('Bounded loss requires legacy_both and a nonnegative budget')
        before = text
        budget = f'const int LOSS_BUDGET = {loss_budget};\n'
        text = text.replace('const bool LOSSY = true;', budget + 'const bool LOSSY = true;')
        match = re.search(r'<template>\s*<name>PacketNetwork</name>.*?</template>', text, re.S)
        assert match
        old = match.group(0)
        new = old.replace('packet_t packet;', 'packet_t packet;\nint[0, LOSS_BUDGET] lossCount = 0;')
        assert old.count('LOSSY &amp;&amp;') == 1
        new = new.replace('LOSSY &amp;&amp;', 'lossCount &lt; LOSS_BUDGET &amp;&amp; LOSSY &amp;&amp;')
        loss_edge = re.search(r'<transition id="id22">.*?</transition>', new, re.S)
        assert loss_edge and 'kind="assignment"' not in loss_edge.group(0)
        counted = loss_edge.group(0).replace('</transition>', '<label kind="assignment" x="331" y="207">lossCount++</label>\n\t\t</transition>')
        new = new.replace(loss_edge.group(0), counted)
        text = text[:match.start()] + new + text[match.end():]
        assert text.replace(new, old).replace(budget, '') == before
        ET.fromstring(text)
    if scheduler != 'original':
        assert scheduler in ['ack_priority', 'observed']
        before = text
        flag_decl = 'bool ackPending[N];\n'
        assert text.count('bool cmdAccepted[N][NB_CMD];') == 1
        text = text.replace('bool cmdAccepted[N][NB_CMD];', flag_decl + 'bool cmdAccepted[N][NB_CMD];')
        changes = []
        for template_name in ['CommandServer', 'PacketNetwork']:
            match = re.search(r'<template>\s*<name>'+template_name+r'</name>.*?</template>', text, re.S)
            assert match
            old = match.group(0)
            def rewrite_edge(match_edge):
                edge = match_edge.group(0)
                parsed = ET.fromstring(edge)
                def add_label(value):
                    # UPPAAL's XML grammar requires all labels before route nails.
                    return re.sub(r'(?=<nail\b|</transition>)', lambda _: value + '\n\t\t\t', edge, count=1)
                if template_name == 'CommandServer':
                    eid = parsed.get('id')
                    if eid == 'id92':
                        assert edge.count('>current = c</label>') == 1
                        edge = edge.replace('>current = c</label>', '>current = c, ackPending[id] = true</label>')
                    elif eid == 'id93':
                        assert edge.count('>execute(current)</label>') == 1
                        edge = edge.replace('>execute(current)</label>', '>execute(current), ackPending[id] = false</label>')
                    elif eid == 'id94':
                        assert not any(l.get('kind') == 'assignment' for l in parsed.findall('label'))
                        edge = add_label('<label kind="assignment" x="80" y="189">ackPending[id] = false</label>')
                elif scheduler == 'ack_priority' and parsed.find('source').get('ref') == 'id0' and parsed.find('target').get('ref') == 'id1':
                    sync = next(l.text for l in parsed.findall('label') if l.get('kind') == 'synchronisation')
                    if not sync.startswith(('accepted_tx[', 'denied_tx[')):
                        assert not any(l.get('kind') == 'guard' for l in parsed.findall('label'))
                        edge = add_label('<label kind="guard" x="420" y="0">forall (i : drone_id) !ackPending[i]</label>')
                return edge
            new = re.sub(r'<transition\b.*?</transition>', rewrite_edge, old, flags=re.S)
            changes.append((old, new))
            text = text[:match.start()] + new + text[match.end():]
        reversed_text = text.replace(flag_decl, '')
        for old, new in changes: reversed_text = reversed_text.replace(new, old)
        assert reversed_text == before
        ET.fromstring(text)
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
    elif re.search(r'Formula.*\b(?:MAY|MAYBE)\b', output, re.I):
        result = 'maybe'
    elif re.search(r'Formula is NOT satisfied', output):
        result = 'not_satisfied'
    elif re.search(r'Formula is satisfied', output):
        result = 'satisfied'
    else:
        result = 'unknown'
    metrics = {}
    for key, pattern in [('explored_states', r'States explored\s*:\s*(\d+)'), ('stored_states', r'States stored\s*:\s*(\d+)'), ('cpu_user_ms', r'CPU user time used\s*:\s*(\d+) ms'), ('reported_resident_kib', r'Resident memory used\s*:\s*(\d+) KiB')]:
        match = re.search(pattern, output, re.I)
        metrics[key] = int(match.group(1)) if match else None
    return dict(result=result, wall_seconds=round(elapsed, 4), returncode=process.returncode,
                sampled_peak_rss_bytes=sampled_peak, **metrics)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifyta', default=os.environ.get('UPPAAL_VERIFYTA'))
    parser.add_argument('--suite', choices=['pilot', 'baseline', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06'], default='pilot')
    parser.add_argument('--scheduler', choices=['original', 'observed', 'ack_priority'], default='original')
    parser.add_argument('--state-representation', type=int, choices=[0, 1, 3], default=1)
    parser.add_argument('--extrapolation', type=int, choices=[0, 2, 3, 4], default=0)
    parser.add_argument('--max-retry', type=int, choices=[0, 1, 2])
    parser.add_argument('--loss-budget', type=int, choices=[0, 1, 2])
    parser.add_argument('--heartbeat', choices=['inactive', 'active'])
    parser.add_argument('--hb-period', type=int, default=20)
    parser.add_argument('--hb-offsets', choices=['synchronous', 'staggered'], default='synchronous')
    parser.add_argument('--search-order', type=int, choices=[0, 1], default=0)
    parser.add_argument('--drones', type=int, choices=[1, 2, 3, 4])
    parser.add_argument('--loss-mode', choices=['reliable', 'request', 'reply', 'both', 'legacy_both'])
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
    if args.hb_period <= 0:
        parser.error('Heartbeat period must be positive')
    options = OPTIONS.copy()
    options[options.index('-o') + 1] = str(args.search_order)
    options[options.index('--state-representation') + 1] = str(args.state_representation)
    options[options.index('-n') + 1] = str(args.extrapolation)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    outdir = ROOT / 'results/reproduced' / f'{stamp}_{args.suite}'
    outdir.mkdir(parents=True, exist_ok=False)
    version = subprocess.run([args.verifyta, '--version'], capture_output=True, text=True, timeout=30)
    (outdir / 'tool_version.log').write_text(version.stdout + version.stderr, encoding='utf-8')
    if version.returncode or 'Failed to retrieve license' in version.stdout + version.stderr:
        raise SystemExit(f'Verifier preflight failed; see {outdir}')
    tool_version = next((line for line in version.stdout.splitlines() if line.startswith('UPPAAL')), version.stdout.strip())
    metadata = dict(run_id=stamp, suite=args.suite, source_model_sha256=sha(SOURCE),
                    reference_git_commit='2ecefd273fa74ad147060c31bc5d48424331fdfe',
                    runner_sha256=sha(Path(__file__)), tool_version=tool_version,
                    verifyta_path=args.verifyta, verifyta_sha256=sha(Path(args.verifyta)),
                    platform=platform.platform(), cpu=platform.processor(),
                    logical_cpus=os.cpu_count(), physical_memory_bytes=psutil.virtual_memory().total,
                    search_options=options, trace_enabled=args.trace, time_limit_seconds=args.limit,
                    memory_limit_bytes=int(args.memory_gib * 1024**3), repetition=args.repetition,
                    rss_measurement='Verifier RSS sampled every 50 ms; lower bound on peak, excludes GUI/runner',
                    liveness_summary_note='verifyta -u warns that summary statistics are incorrect for liveness; state counts omitted for leads-to queries')
    write_json(outdir / 'manifest.json', metadata)
    shutil.copyfile(Path(__file__), outdir / 'runner_snapshot.py')
    default_timeout = 24 if args.suite == 'E04' else 14
    configs = [(3, default_timeout)] if args.suite != 'E02' else [(d, t) for d in [2, 3, 5] for t in [6, 14, 24]]
    if args.dmax is not None or args.ack_timeout is not None:
        configs = [(args.dmax or 3, args.ack_timeout or default_timeout)]
    ids = args.properties or (['P01'] if args.suite == 'pilot' else [p for p in PROPERTIES if int(p[1:]) <= 17] if args.suite == 'baseline' else [p for p in PROPERTIES if int(p[1:]) <= 22] if args.suite == 'E03' else ['P01', 'P02', 'P03', 'P04', 'P05', 'P08', 'P09', 'P15'])
    if args.suite == 'E01' and not args.properties:
        ids = [f'P{i:02d}' for i in range(1, 10)] + ['P13', 'P14', 'P15', 'P16', 'P23']
    if args.suite == 'E05' and not args.properties:
        ids = ['P01', 'P03', 'P08', 'P24']
    if args.suite == 'E04' and not args.properties:
        ids = [f'P{i:02d}' for i in range(1, 9)] + ['P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P21', 'P25', 'P27', 'P28']
    if args.suite == 'E06' and not args.properties:
        ids = ['P01', 'P03', 'P05', 'P06', 'P08', 'P15', 'P24', 'P25', 'P34']
        if args.scheduler != 'original': ids += ['P29']
        ids += [f'P{30+i}' for i in range(args.drones or 3)]
    modes = [args.loss_mode] if args.loss_mode else ['reliable', 'request', 'reply', 'both'] if args.suite == 'E03' else [None]
    sizes = [args.drones] if args.drones else [1, 2, 3, 4] if args.suite == 'E01' else [1, 2, 3] if args.suite == 'E05' else [None]
    if args.suite == 'E04':
        modes = [args.loss_mode or 'legacy_both']
        sizes = [args.drones or 1]
    if args.suite == 'E06': sizes = [args.drones or 3]
    budgets = [args.loss_budget] if args.loss_budget is not None else [0, 1, 2] if args.suite == 'E04' else [None]
    retries = [args.max_retry] if args.max_retry is not None else [0, 1, 2] if args.suite == 'E04' else [2]
    heartbeats = [args.heartbeat] if args.heartbeat else ['inactive', 'active'] if args.suite == 'E05' else ['inactive']
    if args.suite == 'E06': heartbeats = [args.heartbeat or 'active']
    configs = [(d, t, mode, n, hb, k, retry) for d, t in configs for mode in modes for n in sizes for hb in heartbeats for k in budgets for retry in retries]
    rows = []
    print(f'OUTPUT {outdir}', flush=True)
    for dmax, timeout, mode, n, hb, k, retry in configs:
        cid = (f'n{n}_' if n is not None else '') + f'dmax{dmax}_timeout{timeout}' + (f'_{mode}' if mode else '')
        if args.suite == 'E05' or args.heartbeat:
            cid += f'_hb_{hb}_period{args.hb_period}'
        if args.hb_offsets != 'synchronous':
            cid += f'_{args.hb_offsets}'
        if k is not None:
            cid += f'_budget{k}'
        if args.suite == 'E04' or args.max_retry is not None:
            cid += f'_retry{retry}'
        if args.suite == 'E06' or args.scheduler != 'original':
            cid += f'_scheduler_{args.scheduler}'
        config_dir = outdir / cid
        config_dir.mkdir()
        model = config_dir / 'model.xml'
        model.write_text(make_model(dmax, timeout, mode, n, hb, args.hb_period, args.hb_offsets, retry, k, args.scheduler), encoding='utf-8', newline='')
        suite_text = '\n\n'.join(f'// {pid}: {property_for(pid, n or 3)[0]}\n{property_for(pid, n or 3)[1]}' for pid in ids)
        (config_dir / 'queries.q').write_text(suite_text + '\n', encoding='utf-8')
        for pid in ids:
            folder = config_dir / pid
            folder.mkdir()
            title, formula = property_for(pid, n or 3)
            query = folder / 'query.q'
            query.write_text(f'// {pid}: {title}\n{formula}\n', encoding='utf-8')
            command = [str(Path(args.verifyta).resolve()), *options]
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
            if '-->' in formula or formula.lstrip().startswith('A<>'):
                result['explored_states'] = result['stored_states'] = None
                result['cpu_user_ms'] = result['reported_resident_kib'] = None
            row = dict(experiment_id=args.suite, configuration_id=cid, property_id=pid,
                       N=n or 3, mission_size=3, d_min=1, d_max=dmax, ack_timeout=timeout, max_retry=retry,
                       loss_mode='bounded_both' if k is not None else mode or 'reliable', loss_budget=k,
                       heartbeat_mode=hb, heartbeat_period=args.hb_period,
                       scheduler=args.scheduler,
                       heartbeat_offsets=('first eligible at HB_PERIOD + floor(id * HB_PERIOD / N); subsequent period measured from admission' if args.hb_offsets == 'staggered' else 'all clocks initially zero'), model_sha256=sha(model),
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
