"""Rebuild stored-snapshot analytics; explicitly opt in to presentation authoring."""
from pathlib import Path
import argparse,os,subprocess,sys,json,zipfile
from research_io import ROOT,load_results,write_manifest

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--presentation',action='store_true',help='Rebuild the editable deck using ARTIFACT_TOOL_MODULE')
    args=parser.parse_args()
    os.chdir(ROOT)
    runtime=ROOT/'.jupyter-runtime';(runtime/'ipython').mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.update(PYTHONIOENCODING='utf-8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',JUPYTER_RUNTIME_DIR=str(runtime),IPYTHONDIR=str(runtime/'ipython'))
    scripts=['src/cleaning/generate_metadata.py','src/cleaning/clean_and_harmonize.py','sql/02_load_data.py','sql/04_run_queries.py','src/validation/data_audit.py','src/analysis/epidemiological_trends.py','src/analysis/cascade_and_disparities.py','src/analysis/econometric_modeling.py','src/visualization/generate_figures.py','src/write_research_docs.py','notebooks/create_notebook.py']
    if args.presentation:scripts.append('src/create_presentation.py')
    for script in scripts:subprocess.run([sys.executable,str(ROOT/script)],env=env,check=True)
    r=load_results()
    with zipfile.ZipFile(ROOT/'docs/presentation/hiv_epidemiology_research_briefing.pptx') as deck:
        notes=''.join(deck.read(n).decode('utf-8-sig') for n in deck.namelist() if '/notesSlide' in n and n.endswith('.xml'))
        if r['data_sha256'] not in notes:raise ValueError('Presentation belongs to a different snapshot. Rebuild it with --presentation and review before publishing.')
    write_manifest();print('Pipeline complete. All generated artifacts use the current snapshot.')
if __name__=='__main__':main()
