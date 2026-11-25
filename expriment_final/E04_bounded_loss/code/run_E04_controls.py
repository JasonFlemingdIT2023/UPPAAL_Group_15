"""Run the explicit E04 controls and diagnostic cases sequentially."""
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
    for retry in range(3):
        cases.append(('unrestricted', ['--suite', 'pilot', '--drones', '1', '--loss-mode', 'legacy_both', '--ack-timeout', '24', '--max-retry', str(retry), '--properties', 'P01', 'P08', 'P10', 'P11', 'P25']))
    for n in [1, 3]:
        for retry in range(3):
            cases.append(('reliable_control', ['--suite', 'pilot', '--drones', str(n), '--ack-timeout', '24', '--max-retry', str(retry), '--properties', 'P01', 'P08', 'P15', 'P25']))
    cases.append(('timing_control', ['--suite', 'E04', '--drones', '3', '--loss-budget', '0', '--max-retry', '0', '--ack-timeout', '14', '--properties', 'P01', 'P08', 'P10', 'P15', 'P25']))
    for n in [1, 3]:
        cases.append(('diagnostics', ['--suite', 'E04', '--drones', str(n), '--loss-budget', '0', '--max-retry', '0', '--properties', 'P26', '--trace']))
    for k, retry, pid in [(2, 2, 'P28'), (2, 1, 'P11'), (1, 0, 'P10')]:
        cases.append(('diagnostics', ['--suite', 'E04', '--drones', '1', '--loss-budget', str(k), '--max-retry', str(retry), '--properties', pid, '--trace']))
    cases.append(('diagnostics', ['--suite', 'E04', '--drones', '3', '--loss-budget', '0', '--max-retry', '0', '--ack-timeout', '14', '--properties', 'P08', '--trace']))
    index = {}
    commands = []
    log = BASE/('E04_controls_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.log')
    with log.open('w', encoding='utf-8') as stream:
        for category, args in cases:
            command = [sys.executable, str(ROOT/'code/run_coordination_experiments.py'), '--verifyta', verifier, *args]
            commands.append(command)
            proc = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            run = None
            for line in proc.stdout:
                stream.write(line); stream.flush()
                if line.startswith('OUTPUT '): run = Path(line.strip()[7:]).name
                if line.startswith(('OUTPUT ', 'COMPLETE ')) or 'tool_error' in line: print(line.rstrip(), flush=True)
            if proc.wait() != 0: raise SystemExit(f'Control failed: see {log}')
            assert run is not None
            index.setdefault(category, []).append(run)
    target = BASE
    target.mkdir(exist_ok=True, parents=True)
    data = {'runs': index, 'expected_counts': {'unrestricted': 15, 'reliable_control': 24, 'timing_control': 5, 'diagnostics': 6},
            'control_commands': commands, 'control_console_log': str(log.relative_to(ROOT))}
    (target/'E04_controls_index.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Controls and evidence index complete.', flush=True)

if __name__ == '__main__': main()
