"""Prepare live chart/table data and invoke the Artifact Tool presentation builder.
Set ARTIFACT_TOOL_MODULE to the installed artifact_tool.mjs absolute path.
NODE defaults to node on PATH. No credentials or account data are required.
"""
from pathlib import Path
import json,os,subprocess
import pandas as pd
from research_io import ROOT,load_results

def create_deck(base_dir=ROOT):
    root=Path(base_dir);r=load_results(root)
    build=root/'.local-build';build.mkdir(exist_ok=True)
    def rows(path):
        # JSON's null preserves missing values for the authoring script.
        return json.loads(pd.read_csv(root/path).to_json(orient='records'))
    payload=dict(results=r,sea=rows('data/processed/southeast_asia_hiv_longitudinal_1990_2025.csv'),
        trends=rows('reports/analysis_tables/regional_trend_summary_2010_2025.csv'),
        cascade=rows('reports/analysis_tables/cascade_2025_summary.csv'),
        gaps=rows('reports/analysis_tables/treatment_gaps_2025.csv'))
    (build/'presentation_data.json').write_text(json.dumps(payload,allow_nan=False),encoding='utf-8')
    subprocess.run([os.environ.get('NODE','node'),str(root/'src/create_presentation.mjs')],cwd=root,check=True)
if __name__=='__main__':create_deck()
