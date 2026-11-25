"""Sequential ACK-priority comparisons, instrumentation controls and concrete traces."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'results/reproduced'

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verifyta', default=os.environ.get('UPPAAL_VERIFYTA'))
    args = parser.parse_args()
    if not args.verifyta or not Path(args.verifyta).is_file():
        parser.error('Set UPPAAL_VERIFYTA or pass --verifyta')
    verifier = str(Path(args.verifyta).resolve())
    BASE.mkdir(parents=True, exist_ok=True)
    cases = []
    for n in [1, 2]:
        for scheduler in ['original', 'ack_priority']:
            properties = ['P01', 'P03', 'P05', 'P06', 'P15', 'P24', 'P25', 'P34', 'P35', 'P36', 'P37'] + [f'P{30+i}' for i in range(n)]
            if scheduler == 'ack_priority': properties += ['P29']
            cases.append(('small_exact', ['--drones', str(n), '--scheduler', scheduler, '--properties', *properties]))
    cases.append(('instrumentation_control', ['--drones', '2', '--scheduler', 'observed', '--properties', 'P01', 'P15', 'P25', 'P29', 'P30', 'P31', 'P35', 'P36', 'P37', 'P34']))
    cases.append(('diagnostics', ['--drones', '3', '--scheduler', 'original', '--search-order', '1', '--trace', '--properties', 'P35', 'P34']))
    cases.append(('diagnostics', ['--drones', '3', '--scheduler', 'ack_priority', '--search-order', '1', '--trace', '--properties', 'P34', 'P38']))
    cases.append(('original_overapprox', ['--drones', '3', '--scheduler', 'original', '--state-representation', '3', '--properties', 'P03', 'P35', 'P30', 'P31', 'P32']))
    runs = {}
    counts = {'small_exact': 52, 'instrumentation_control': 10, 'diagnostics': 4, 'original_overapprox': 5}
    log = BASE/('E06_followups_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.log')
    commands = []
    with log.open('w', encoding='utf-8') as stream:
        for category, args in cases:
            cmd = [sys.executable, str(ROOT/'code/run_coordination_experiments.py'), '--verifyta', verifier, '--suite', 'E06', *args]
            commands.append(cmd)
            proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            run = None
            for line in proc.stdout:
                stream.write(line); stream.flush()
                if line.startswith('OUTPUT '): run = Path(line.strip()[7:]).name
                if line.startswith(('OUTPUT ', 'COMPLETE ')) or any(x in line for x in ['maybe', 'timeout', 'tool_error']):
                    if line.startswith('RUN '): continue
                    print(line.rstrip(), flush=True)
            if proc.wait() != 0: raise SystemExit(f'Followup failed: {log}')
            assert run is not None
            runs.setdefault(category, []).append(run)
    folder = BASE
    folder.mkdir(exist_ok=True, parents=True)
    data = {'runs': runs, 'expected_counts': counts, 'followup_commands': commands,
            'console_log': str(log.relative_to(ROOT)),
            'excluded_attempts': {
                '20261125T150852402927Z_E06': 'XML label order rejected; corrected before verification study.',
                '20261125T151458396871Z_E06': 'Formula MAY NOT be satisfied was not recognized by the first parser; rerun with explicit maybe classification.',
                '20261125T150937929404Z_E06/P03': 'Unfinished query stopped after the two preceding exact searches exhausted their budgets; only three completed result records included.'
            },
            'historical_failure_trace': '20261125T132904048744Z_E05/n3_dmax3_timeout14_hb_active_period20/P08'}
    (folder/'E06_followups_index.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print('E06 followups and evidence index complete.', flush=True)

if __name__ == '__main__': main()
