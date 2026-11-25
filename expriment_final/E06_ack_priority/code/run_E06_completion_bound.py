"""Check a passive completion timer; keep the E06 production model unchanged."""
import argparse
import os
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from run_coordination_experiments import ROOT, SOURCE, make_model, run_one, sha, write_json


def semantic(node):
    return (node.tag, tuple(sorted((k, v) for k, v in node.attrib.items()
                                  if k not in ['x', 'y'])), (node.text or '').strip(),
            tuple(semantic(c) for c in node if c.tag not in ['nail', 'queries']))


def instrument():
    base = make_model(3, 14, n=3, heartbeat='active', scheduler='ack_priority')
    original = ET.fromstring(base)
    root = copy.deepcopy(original)
    addition = '\n// Passive observation only: no guards or invariants use these.\nclock completionAge;\nbool completionStarted = false;\n'
    root.find('declaration').text += addition
    supervisor = next(t for t in root.findall('template') if t.findtext('name') == 'GCSSupervisor')
    prepared = next(l.get('id') for l in supervisor.findall('location') if l.findtext('name') == 'Prepared')
    edges = [e for e in supervisor.findall('transition') if e.find('target').get('ref') == prepared]
    assert len(edges) == 1 and not any(l.get('kind') == 'assignment' for l in edges[0].findall('label'))
    update = ET.Element('label', {'kind': 'assignment', 'x': '0', 'y': '0'})
    update.text = 'completionAge = 0, completionStarted = true'
    # UPPAAL requires labels before nails.
    edge = edges[0]
    first_nail = next((i for i, c in enumerate(edge) if c.tag == 'nail'), len(edge))
    edge.insert(first_nail, update)
    instrumented = ET.tostring(root, encoding='unicode')
    # Removing exactly the observation data recovers the entire original model.
    edge.remove(update)
    root.find('declaration').text = root.find('declaration').text.removesuffix(addition)
    assert semantic(root) == semantic(original)
    assert semantic(original) == semantic(ET.parse(ROOT/'code/models/09_ack_priority.xml').getroot())
    return base, instrumented


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verifyta', default=os.environ.get('UPPAAL_VERIFYTA'))
    p.add_argument('--limit', type=float, default=120)
    p.add_argument('--bound', type=int, default=120)
    p.add_argument('--state-representation', type=int, choices=[0, 1, 3], default=3)
    p.add_argument('--property', choices=['bound', 'no_abort', 'no_deadlock'], default='bound')
    args = p.parse_args()
    if not args.verifyta or not Path(args.verifyta).is_file():
        p.error('Set UPPAAL_VERIFYTA or pass --verifyta')
    args.verifyta = str(Path(args.verifyta).resolve())
    assert args.limit > 0 and args.bound > 0
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder = ROOT/'results/reproduced'/f'{stamp}_E06_completion_bound'
    folder.mkdir(parents=True)
    base, model = instrument()
    (folder/'base_model.xml').write_text(base, encoding='utf-8', newline='')
    (folder/'model.xml').write_text(model, encoding='utf-8', newline='')
    queries = {
        'bound': f'A[] ((completionStarted && !Supervisor.Done) imply completionAge <= {args.bound})',
        'no_abort': 'A[] !Supervisor.Aborted',
        'no_deadlock': 'A[] (completionStarted imply !deadlock)',
    }
    query = queries[args.property]
    (folder/'query.q').write_text(query+'\n', encoding='utf-8')
    shutil.copyfile(__file__, folder/'runner_snapshot.py')
    shutil.copyfile(ROOT/'code/run_coordination_experiments.py', folder/'core_runner_snapshot.py')
    version = subprocess.run([args.verifyta, '--version'], capture_output=True, text=True, timeout=30)
    (folder/'tool_version.log').write_text(version.stdout+version.stderr, encoding='utf-8')
    assert version.returncode == 0
    options = ['-s', '-u', '-o', '0', '--state-representation', str(args.state_representation), '-S', '1', '-n', '0', '-r', '1']
    command = [args.verifyta, *options, 'model.xml', 'query.q']
    meta = dict(experiment_id='E06_completion_bound', property=args.property, query=query,
                passive_instrumentation_audit='Removing only the new declaration and update restores base model semantics; base matches GUI model semantics.',
                base_model_sha256=sha(folder/'base_model.xml'), model_sha256=sha(folder/'model.xml'),
                query_sha256=sha(folder/'query.q'), source_model_sha256=sha(SOURCE),
                gui_model_sha256=sha(ROOT/'code/models/09_ack_priority.xml'), verifyta_sha256=sha(Path(args.verifyta)),
                runner_sha256=sha(Path(__file__)), core_runner_sha256=sha(ROOT/'code/run_coordination_experiments.py'),
                state_representation=args.state_representation, time_limit_seconds=args.limit, memory_limit_bytes=8*1024**3,
                concurrency_note='May overlap the extended direct P25 verification; runtime is not a controlled performance comparison.')
    write_json(folder/'manifest.json', meta)
    write_json(folder/'command.json', command)
    print('OUTPUT', folder, flush=True)
    with tempfile.TemporaryDirectory(prefix='uppaal_completion_') as scratch:
        assert scratch.isascii()
        for name in ['model.xml', 'query.q']:
            shutil.copyfile(folder/name, Path(scratch)/name)
            assert sha(folder/name) == sha(Path(scratch)/name)
        write_json(folder/'execution.json', {'cwd': scratch})
        result = run_one(command, folder, args.limit, meta['memory_limit_bytes'], scratch)
    write_json(folder/'result.json', dict(**meta, **result))
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
