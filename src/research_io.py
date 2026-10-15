"""Shared snapshot loading and integrity guards for all published outputs."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha256(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_results(root=ROOT):
    root=Path(root);r=json.loads((root/'reports/results.json').read_text(encoding='utf-8'))
    if sha256(root/'data/processed/southeast_asia_hiv_panel_2010_2025.csv')!=r['data_sha256']:
        raise ValueError('Analysis is stale. Rebuild the pipeline before publishing.')
    return r

def write_manifest():
    paths=[]
    for folder in ['data/raw','data/processed','data/metadata','reports/analysis_tables','reports/sql_results','figures','docs/presentation','notebooks']:
        paths.extend(p for p in (ROOT/folder).glob('*') if p.is_file() and p.suffix not in ['.py','.ndjson'])
    paths.extend(ROOT/p for p in ['README.md','reports/research_report.md','reports/data_quality_audit.md','reports/results.json','reports/audit.json','docs/study_protocol.md'])
    manifest={p.relative_to(ROOT).as_posix():sha256(p) for p in sorted(paths)}
    (ROOT/'reports/artifact_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    return manifest

def verify_manifest():
    manifest=json.loads((ROOT/'reports/artifact_manifest.json').read_text(encoding='utf-8'))
    bad=[p for p,h in manifest.items() if not (ROOT/p).exists() or sha256(ROOT/p)!=h]
    if bad:raise ValueError('Stale or modified artifacts: '+', '.join(bad))
    load_results()
    print(f'Verified {len(manifest)} artifact and input hashes')
if __name__=='__main__':verify_manifest()
