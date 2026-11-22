#!/usr/bin/env python3
"""Run the small network experiments with the local UPPAAL verifier.

Usage, from the project folder:
    python3 scripts/run_network_checks.py

If verifyta is not in the default macOS location, set UPPAAL_VERIFYTA to its path first.
The script writes the model copies, logs and traces to results/network_runs/
and the per-query results to results/network_results.csv.
"""
from pathlib import Path
import csv
import hashlib
import os
import re
import subprocess
import time
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'models/network_model.xml'
FINAL_OUT = ROOT / 'results/network_runs'
OUT = FINAL_OUT
VERIFYTA = Path(os.environ.get('UPPAAL_VERIFYTA', str(Path.home() / 'Applications/UPPAAL-5.0.0.app/Contents/app/bin/verifyta')))
# (run name, LOSS_MODE, D_MAX). D_MIN = 1 and K_LOSS = 1 in every run.
CASES = [('reliable', 0, 3), ('lossy', 1, 3), ('bounded_loss', 2, 3), ('slow_reliable', 0, 5)]

def invoke(args, timeout=120):
    # Run verifyta once and return its output and how long it took.
    start = time.monotonic()
    p = subprocess.run([str(VERIFYTA), *map(str, args)], capture_output=True, text=True, timeout=timeout)
    return p, time.monotonic() - start

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = MODEL.read_text()
    # The runs are made by text replacement, so stop if the base model no longer has these exact lines.
    for declaration in ('const int LOSS_MODE = 1;', 'const int D_MIN = 1;',
                        'const int D_MAX = 3;', 'const int K_LOSS = 1;'):
        if base.count(declaration) != 1:
            raise SystemExit(f'Expected one {declaration} in the base model; update the experiment settings first.')
    # Save the verifier version so every result can be traced back to it.
    version, _ = invoke(['--version'])
    (OUT / 'version.log').write_text(version.stdout + version.stderr)
    if version.returncode:
        raise SystemExit('Could not run verifyta; saved results were not changed.\n' + version.stderr.strip())
    version_line = next((line for line in version.stdout.splitlines() if line.startswith('UPPAAL ')), None)
    if not version_line:
        raise SystemExit('Could not identify the verifier version; saved results were not changed.')
    rows = []
    for name, mode, maximum in CASES:
        # Make a copy of the model with this run's settings and hash it.
        text = base.replace('const int LOSS_MODE = 1;', f'const int LOSS_MODE = {mode};').replace('const int D_MAX = 3;', f'const int D_MAX = {maximum};')
        if text == base and name != 'lossy':
            raise SystemExit('Parameter replacement failed')
        model = OUT / (name + '.xml')
        model.write_text(text)
        digest = hashlib.sha256(model.read_bytes()).hexdigest()
        # Check all 18 embedded queries on that copy and keep the raw log.
        result, seconds = invoke([model])
        log = OUT / (name + '.log')
        output = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', result.stdout + result.stderr)
        log.write_text(output)
        if result.returncode:
            raise SystemExit(f'{name} failed; saved results were not changed.\n{output.strip()}')
        # Split the log into one block per query and read the result of each.
        blocks = re.split(r'Verifying formula (\d+) at .*?\n', output)[1:]
        if len(blocks) != 36:
            raise SystemExit(f'Expected 18 queries for {name}; saved results were not changed.')
        for number, block in zip(blocks[::2], blocks[1::2]):
            formula = re.search(r' -- Formula: (.*)', block).group(1)
            match = re.search(r' -- Formula is (NOT satisfied|satisfied)\.', block)
            if not match:
                raise SystemExit(f'Missing result for query {number}, {name}')
            # Only N18 has a sup value. It is copied as verifyta prints it, e.g. "9:" means 9.
            measure = re.search(r'sup: ([^\n]+)', block)
            rows.append([name, digest, version_line, mode, 1, maximum, 1, 'N'+number, formula, match.group(1), measure.group(1).strip() if measure else '', f'{seconds:.3f}', str((FINAL_OUT / log.name).relative_to(ROOT))])
        print(f'{name}: {len(blocks)//2} queries, {seconds:.3f}s, sha256 {digest}')
    with (OUT.parent / 'network_results.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['run','model_sha256','tool_version','loss_mode','d_min','d_max','k_loss','property_id','query','result','supremum','run_seconds_all_queries','log'])
        writer.writerows(rows)
    # Three example traces (verifyta -t 0), all taken from the unrestricted-loss copy.
    for name, query in [('delivery_trace', 'E<> delivered > 0'), ('loss_trace', 'E<> lost > 0'), ('contention_trace', 'E<> (pending[0] && pending[1] && Link.Transmitting)')]:
        query_file = OUT / (name + '.q')
        query_file.write_text(query + '\n')
        result, _ = invoke(['-t', '0', OUT / 'lossy.xml', query_file])
        (OUT / (name + '.log')).write_text(re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', result.stdout + result.stderr))
        if result.returncode or 'Formula is satisfied' not in result.stdout:
            raise SystemExit(f'Trace failed: {name}')
    print('Saved results and three witness traces.')

if __name__ == '__main__':
    # Keep the saved results if the verifier or any query fails.
    with tempfile.TemporaryDirectory(prefix='uppaal-network-') as stage:
        OUT = Path(stage) / 'network_runs'
        main()
        FINAL_OUT.mkdir(parents=True, exist_ok=True)
        for item in OUT.iterdir():
            shutil.copy2(item, FINAL_OUT / item.name)
        shutil.copy2(OUT.parent / 'network_results.csv', ROOT / 'results/network_results.csv')
        note = FINAL_OUT / 'README_rerun.txt'
        if note.exists():
            note.write_text(
                'An earlier rerun failed and overwrote the original reliable and version logs. '
                'A later complete rerun succeeded; network_results.csv and the current run logs '
                'now record the new results. The original overwritten logs cannot be recovered.\n'
            )
        print('Check the documentation against these new results before sharing.')
