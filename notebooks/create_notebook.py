"""Create and execute the six-cell research walkthrough against stored outputs."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
def create_notebook():
    nb=nbformat.v4.new_notebook()
    nb.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    codes=[
      "from pathlib import Path\nimport sys, json\nimport pandas as pd\nfrom IPython.display import display, Image\nROOT=Path.cwd()\nsys.path.insert(0,str(ROOT/'src'))\nfrom research_io import load_results\nr=load_results()\nd=pd.read_csv(ROOT/'data/processed/southeast_asia_hiv_longitudinal_1990_2025.csv')\nprint('Southeast Asia countries:',d.iso3.nunique(),'country-years:',len(d))",
      "display(pd.read_csv(ROOT/'reports/analysis_tables/regional_trend_summary_2010_2025.csv'))",
      "c=pd.read_csv(ROOT/'reports/analysis_tables/cascade_2025_summary.csv')\ndisplay(c[c.is_southeast_asia.eq(1)][['country_name','diagnosed_1st95_pct_source','on_art_2nd95_pct_source','virally_suppressed_3rd95_pct_source','virally_suppressed_all_pct_source']])",
      "display(pd.DataFrame(r['models'])[['model_name','coefficient','ci_lower_95','ci_upper_95','n_observations','n_countries']])\nprint(r['inference'])",
      "display(pd.DataFrame(r['leave_one_country_out'])[['model_name','coefficient','ci_lower_95','ci_upper_95','n_observations']])\nfor note in r['limitations']: print(note)",
      "import sqlite3\nwith sqlite3.connect((ROOT/'data/processed/hiv_surveillance.db').as_uri()+'?mode=ro',uri=True) as con:\n    display(pd.read_sql_query(\"select year,plhiv,aids_deaths,art_coverage_pct from v_southeast_asia_surveillance where iso3='MMR' and year>=2010\",con))\ndisplay(Image(filename=str(ROOT/'figures/fig4_lagged_art_mortality_associations.png'),width=1000))"
    ]
    headers=['Snapshot and lineage','Descriptive changes','Cascade denominators and censoring','Exploratory model comparisons','Sensitivity and limitations','SQLite reconciliation and figure']
    nb.cells=[nbformat.v4.new_markdown_cell('# HIV trends and treatment access\n\nDr. Aung Chit Moe, MBBS. UNAIDS 2026 and WDI stored snapshot. National ecological associations do not establish clinical or programme effects. Sources and complete methods: ../reports/research_report.md. Censored values remain missing numerically and retain source labels.')]
    for title,code in zip(headers,codes):nb.cells.extend([nbformat.v4.new_markdown_cell('## '+title),nbformat.v4.new_code_cell(code)])
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
    (ROOT/'notebooks/hiv_epidemiology_research.ipynb').write_text(nbformat.writes(nb),encoding='utf-8',newline='\n')
    print('Executed and saved all six notebook cells')
if __name__=='__main__':create_notebook()
