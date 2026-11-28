"""Verify the Prepared boundary, then universally quantify heartbeat phases.

The proof copy admits arbitrary real heartbeat ages in [0,20] at activation,
including pending heartbeats via age 20, and an optional heartbeat already in
flight with arbitrary residual service in [0,3]. Original post-boundary protocol
edges are retained. See the accompanying completion-proof note for the mapping.
"""
import argparse
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
from run_E06_completion_bound import semantic


def loc(template, name):
    return next(l.get('id') for l in template.findall('location') if l.findtext('name') == name)


def add_location(template, ident, name, invariant=None):
    node = ET.Element('location', {'id': ident, 'x': '0', 'y': '0'})
    ET.SubElement(node, 'name').text = name
    if invariant:
        ET.SubElement(node, 'label', {'kind': 'invariant'}).text = invariant
    template.insert(list(template).index(template.find('init')), node)


def add_edge(template, source, target, **labels):
    edge = ET.SubElement(template, 'transition')
    ET.SubElement(edge, 'source', {'ref': source})
    ET.SubElement(edge, 'target', {'ref': target})
    for kind, text in labels.items():
        ET.SubElement(edge, 'label', {'kind': kind}).text = text


def prepare():
    base = make_model(3, 14, n=3, heartbeat='active', scheduler='ack_priority')
    original = ET.fromstring(base)
    assert semantic(original) == semantic(ET.parse(ROOT/'models/09_ack_priority.xml').getroot())
    root = copy.deepcopy(original)
    declarations = root.find('declaration')
    for name in ['uploadDone', 'missionInstalled']:
        old = f'bool {name}[N];'
        assert declarations.text.count(old) == 1
        declarations.text = declarations.text.replace(old, f'bool {name}[N] = {{true, true, true}};')
    declarations.text += '\nclock bootClock;\nbool bootReady[N];\nbroadcast chan activateProof;\n'
    templates = {t.findtext('name'): t for t in root.findall('template')}
    sup = templates['GCSSupervisor']
    add_location(sup, 'proofSupBoot', 'ProofBoot')
    sup.find('init').set('ref', 'proofSupBoot')
    add_edge(sup, 'proofSupBoot', loc(sup, 'Prepared'), synchronisation='activateProof?')
    hb = templates['HBSender']
    add_location(hb, 'proofHBChoose', 'ProofChoosePhase')
    add_location(hb, 'proofHBDormant', 'ProofDormant')
    hb.find('init').set('ref', 'proofHBChoose')
    add_edge(hb, 'proofHBChoose', 'proofHBDormant', assignment='period = 0, bootReady[id] = true')
    add_edge(hb, 'proofHBDormant', loc(hb, 'Waiting'), synchronisation='activateProof?')
    net = templates['PacketNetwork']
    add_location(net, 'proofNetBoot', 'ProofBoot')
    add_location(net, 'proofNetResidual', 'ProofResidualHeartbeat', 't <= D_MAX')
    net.find('init').set('ref', 'proofNetBoot')
    add_edge(net, 'proofNetBoot', loc(net, 'Idle'), synchronisation='activateProof?')
    add_edge(net, 'proofNetBoot', 'proofNetResidual', select='d : drone_id',
             synchronisation='activateProof?', assignment='storePacket(d, PK_HEARTBEAT, 0, 0), t = 0')
    add_edge(net, 'proofNetResidual', loc(net, 'Delivered'), synchronisation='heartbeat_rx[packet.peer]!')
    boot = ET.Element('template')
    ET.SubElement(boot, 'name').text = 'ProofBootstrap'
    node = ET.SubElement(boot, 'location', {'id': 'proofBootWait'})
    ET.SubElement(node, 'name').text = 'ChoosePhases'
    ET.SubElement(node, 'label', {'kind': 'invariant'}).text = 'bootClock <= HB_PERIOD'
    node = ET.SubElement(boot, 'location', {'id': 'proofBootDone'})
    ET.SubElement(node, 'name').text = 'Finished'
    ET.SubElement(boot, 'init', {'ref': 'proofBootWait'})
    add_edge(boot, 'proofBootWait', 'proofBootDone',
             guard='bootClock == HB_PERIOD && forall (i : drone_id) bootReady[i]',
             synchronisation='activateProof!')
    root.insert(list(root).index(root.find('system')), boot)
    root.find('system').text = '\nSupervisor = GCSSupervisor();\nLink = PacketNetwork();\nBootstrap = ProofBootstrap();\nsystem Supervisor, Link, CommandClient, CommandServer, HBSender, ConnectionMonitor, Bootstrap;\n'
    # All original templates, locations, declarations, transitions and labels are
    # unchanged. Only new bootstrap locations/edges and initial references differ.
    check = copy.deepcopy(root)
    check.remove(next(t for t in check.findall('template') if t.findtext('name') == 'ProofBootstrap'))
    for t in check.findall('template'):
        old = next(o for o in original.findall('template') if o.findtext('name') == t.findtext('name'))
        for node in list(t):
            added = (node.tag == 'location' and node.get('id', '').startswith('proof')) or (
                node.tag == 'transition' and (node.find('source').get('ref').startswith('proof') or node.find('target').get('ref').startswith('proof')))
            if added:
                t.remove(node)
        t.find('init').set('ref', old.find('init').get('ref'))
        assert semantic(t) == semantic(old)
    check.find('declaration').text = original.findtext('declaration')
    check.find('system').text = original.findtext('system')
    assert semantic(check) == semantic(original)
    return base, ET.tostring(root, encoding='unicode')


def boundary_query():
    fleet = 'forall (i : drone_id) (uploadDone[i] && missionInstalled[i] && !armed[i] && !started[i] && !ackPending[i] && !Supervisor.armSent[i] && !Supervisor.startSent[i] && forall (c : cmd_id) (!cmdAccepted[i][c] && !cmdDenied[i][c] && !cmdFailed[i][c]))'
    parts = [fleet, '(Link.Idle || Link.Delivered || (Link.Transmitting && Link.packet.kind == PK_HEARTBEAT))']
    for i in range(3):
        parts += [f'Sender{i}.Done', f'Drone{i}.Uploaded', f'CommandClient({i}).Idle',
                  f'CommandClient({i}).current == ARM', f'CommandClient({i}).retries == 0',
                  f'CommandServer({i}).Idle', f'CommandServer({i}).current == ARM',
                  f'((HBSender({i}).Waiting && HBSender({i}).period <= HB_PERIOD) || (HBSender({i}).Pending && HBSender({i}).period >= HB_PERIOD))']
    return 'A[] (Supervisor.Prepared imply ('+' && '.join(parts)+'))'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verifyta', default=r'D:\Tools\UPPAAL-5.1.0-beta6\bin\verifyta.exe')
    p.add_argument('--mode', choices=['boundary', 'progress'], default='progress')
    p.add_argument('--limit', type=float, default=300)
    p.add_argument('--state-representation', type=int, choices=[0, 1, 3], default=1)
    args = p.parse_args()
    assert args.limit > 0
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder = ROOT/'results/coordination'/f'{stamp}_E06_prepared_{args.mode}'
    folder.mkdir()
    base, abstract = prepare()
    model = base if args.mode == 'boundary' else abstract
    query = boundary_query() if args.mode == 'boundary' else 'A<> Supervisor.Done'
    (folder/'base_model.xml').write_text(base, encoding='utf-8', newline='')
    (folder/'model.xml').write_text(model, encoding='utf-8', newline='')
    (folder/'query.q').write_text(query+'\n', encoding='utf-8')
    for name in ['run_E06_prepared_abstraction.py', 'run_E06_completion_bound.py', 'run_coordination_experiments.py']:
        shutil.copyfile(ROOT/'scripts'/name, folder/name)
    version = subprocess.run([args.verifyta, '--version'], capture_output=True, text=True, timeout=30)
    (folder/'tool_version.log').write_text(version.stdout+version.stderr, encoding='utf-8')
    assert version.returncode == 0
    options = ['-s', '-u', '-o', '1', '--state-representation', str(args.state_representation), '-S', '1', '-n', '0', '-r', '1', '-t', '0']
    command = [args.verifyta, *options, 'model.xml', 'query.q']
    meta = dict(experiment_id='E06_prepared_'+args.mode, query=query,
                base_model_sha256=sha(folder/'base_model.xml'), model_sha256=sha(folder/'model.xml'), query_sha256=sha(folder/'query.q'),
                source_model_sha256=sha(SOURCE), gui_model_sha256=sha(ROOT/'models/09_ack_priority.xml'), verifyta_sha256=sha(Path(args.verifyta)),
                runner_sha256=sha(Path(__file__)), state_representation=args.state_representation,
                time_limit_seconds=args.limit, memory_limit_bytes=8*1024**3,
                concurrency_note='May overlap extended direct verification; not a controlled runtime comparison.',
                structural_audit='Original protocol templates recover exactly after removing bootstrap additions and restoring init refs.')
    write_json(folder/'manifest.json', meta)
    write_json(folder/'command.json', command)
    print('OUTPUT', folder, flush=True)
    with tempfile.TemporaryDirectory(prefix='uppaal_prepared_') as scratch:
        assert scratch.isascii()
        for name in ['model.xml', 'query.q']:
            shutil.copyfile(folder/name, Path(scratch)/name)
            assert sha(folder/name) == sha(Path(scratch)/name)
        write_json(folder/'execution.json', {'cwd': scratch})
        result = run_one(command, folder, args.limit, meta['memory_limit_bytes'], scratch)
    if args.mode == 'progress':
        for key in ['explored_states', 'stored_states', 'cpu_user_ms', 'reported_resident_kib']:
            result[key] = None
    write_json(folder/'result.json', dict(**meta, **result))
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
