"""Audit the two verifier premises of the E06 compositional completion proof."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from run_coordination_experiments import ROOT, sha, write_json
from run_E06_prepared_abstraction import prepare, boundary_query
from run_E06_completion_bound import semantic


def main():
    base = ROOT/'results/coordination'
    index = json.loads((ROOT/'experiments/E06_ack_priority/completion_evidence.json').read_text(encoding='utf-8'))
    original, abstract = prepare()
    rows = {}
    for key, model, query in [('boundary_run', original, boundary_query()),
                              ('progress_run', abstract, 'A<> Supervisor.Done')]:
        folder = base/index[key]
        row = json.loads((folder/'result.json').read_text(encoding='utf-8'))
        assert row['result'] == 'satisfied' and row['returncode'] == 0
        raw = (folder/'stdout.log').read_text(encoding='utf-8')
        assert 'Formula is satisfied.' in raw and 'MAY' not in raw
        assert not (folder/'stderr.log').read_text(encoding='utf-8').strip()
        for name, field in [('base_model.xml', 'base_model_sha256'), ('model.xml', 'model_sha256'),
                            ('query.q', 'query_sha256'), ('run_E06_prepared_abstraction.py', 'runner_sha256')]:
            assert sha(folder/name) == row[field]
        for file, field in [('models/08_final_version.xml', 'source_model_sha256'),
                            ('models/09_ack_priority.xml', 'gui_model_sha256')]:
            assert sha(ROOT/file) == row[field]
        command = json.loads((folder/'command.json').read_text(encoding='utf-8'))
        assert sha(Path(command[0])) == row['verifyta_sha256']
        assert command[-2:] == ['model.xml', 'query.q']
        expected_rep = 3 if key == 'boundary_run' else 1
        assert row['state_representation'] == expected_rep
        assert command[command.index('--state-representation')+1] == str(expected_rep)
        assert row['query'] == query and (folder/'query.q').read_text(encoding='utf-8').strip() == query
        assert semantic(ET.parse(folder/'model.xml').getroot()) == semantic(ET.fromstring(model))
        assert (folder/'base_model.xml').read_text(encoding='utf-8') == original
        rows[key] = dict(run=index[key], query=query, result=row['result'],
                         state_representation=expected_rep, wall_seconds=row['wall_seconds'],
                         sampled_peak_rss_bytes=row['sampled_peak_rss_bytes'],
                         model_sha256=row['model_sha256'], query_sha256=row['query_sha256'])
    direct = base/index['extended_direct_run']/'n3_dmax3_timeout14_scheduler_ack_priority/P25'
    interruption = None
    if index.get('extended_direct_status') == 'interrupted_after_compositional_proof':
        interruption = json.loads((direct/'interruption.json').read_text(encoding='utf-8'))
        assert interruption['result'] == index['extended_direct_status']
        assert interruption['elapsed_verifier_seconds'] == index['extended_direct_elapsed_seconds']
        assert interruption['configured_time_limit_seconds'] == 1200
        assert (direct.parent/'model.xml').read_text(encoding='utf-8') == original
        assert (direct/'query.q').read_text(encoding='utf-8').strip().endswith(index['target'])
        assert 'Formula is satisfied.' not in (direct/'stdout.log').read_text(encoding='utf-8')
        assert not (direct/'result.json').exists()
    auxiliary = []
    for run in index['auxiliary_timer_runs']:
        folder = base/run
        r = json.loads((folder/'result.json').read_text(encoding='utf-8'))
        for file, field in [('model.xml', 'model_sha256'), ('query.q', 'query_sha256'), ('runner_snapshot.py', 'runner_sha256')]:
            assert sha(folder/file) == r[field]
        raw = (folder/'stdout.log').read_text(encoding='utf-8')
        assert (r['result'] == 'maybe' and 'Formula MAY NOT be satisfied.' in raw) or (
            r['result'] == 'timeout' and r['wall_seconds'] >= r['time_limit_seconds'])
        auxiliary.append(dict(run=run, result=r['result'], wall_seconds=r['wall_seconds']))
    out = base/'analysis_E06/completion_proof.json'
    write_json(out, dict(target=index['target'], conclusion='satisfied_by_compositional_proof',
                        premises=rows, source_model_sha256=sha(ROOT/'models/08_final_version.xml'),
                        gui_model_sha256=sha(ROOT/'models/09_ack_priority.xml'),
                        coverage_argument=index['coverage_argument'],
                        scope='N=3, HB_PERIOD=20, D=1..3, ACK_TIMEOUT=14, MAX_RETRY=2, LOSSY=false, ACK priority',
                        audit='Raw verdicts, hashes, query/command identity, regenerated models, and unchanged original protocol templates checked. Coverage is justified by the written state-mapping argument, not an automatic equivalence checker.',
                        extended_direct_run=index['extended_direct_run'],
                        extended_direct_interruption=interruption, auxiliary_timer_attempts=auxiliary))
    print('E06 completion proof: both verifier premises and model-preservation audit passed.')


if __name__ == '__main__':
    main()
