"""Fail-fast audit of keys, ranges, censoring, SQL parity and source consistency."""
from pathlib import Path
import hashlib,json,sqlite3
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]

def run_who_unaids_cross_validation(master):
    rows=[]
    for file,col in [('art_coverage','art_coverage_pct'),('hiv_deaths','aids_deaths'),('new_infections','new_infections'),('plhiv','plhiv')]:
        w=pd.read_csv(ROOT/f'data/raw/who_gho_{file}.csv')
        w=w[w.SpatialDimType.eq('COUNTRY')].dropna(subset=['NumericValue'])
        assert not w.duplicated(['SpatialDim','TimeDim']).any(), 'WHO strata must be resolved before joining'
        m=master[['iso3','year',col]].dropna(subset=[col])
        j=m.merge(w,left_on=['iso3','year'],right_on=['SpatialDim','TimeDim'],validate='one_to_one')
        diff=(j[col]-j.NumericValue).abs()
        assert len(j)>0 and diff.max()==0, f'WHO/UNAIDS snapshot disagreement: {col}'
        rows.append(dict(indicator=col,matched_country_years=len(j),exact_matches=int(diff.eq(0).sum()),max_absolute_difference=float(diff.max()),
            unaids_numeric_rows=len(m),who_country_numeric_rows=len(w),unaids_unmatched_numeric_rows=len(m)-len(j)))
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/'reports/analysis_tables/who_unaids_cross_validation.csv',index=False,lineterminator='\n')
    return out

def run_audit():
    master=pd.read_csv(ROOT/'data/processed/hiv_epidemiology_master_1990_2025.csv')
    sea=master[master.is_southeast_asia.eq(1)]
    checks=[]
    def check(name,passed):
        assert passed,name
        checks.append(name)
    check('Unique entity-year keys',not master.duplicated(['iso3','year']).any())
    check('Complete 1990-2025 grid',master.groupby('iso3').year.nunique().eq(36).all())
    check('11 Southeast Asian country grids',sea.iso3.nunique()==11 and len(sea)==396)
    qualifiers=[c for c in master if c.endswith('_qualifier')]
    censored={}
    for q in qualifiers:
        c=q[:-10];mask=master[q].isin(['<','>'])
        censored[c]=int(mask.sum())
        check('Censor handling: '+c,master.loc[mask,c].isna().all() and master.loc[mask,c+'_threshold'].notna().all())
    for c in ['art_coverage_pct','diagnosed_1st95_pct','on_art_2nd95_pct','virally_suppressed_all_pct','virally_suppressed_3rd95_pct']:
        check('Percentage range: '+c,master[c].dropna().between(0,100).all())
    for c in ['plhiv','aids_deaths','new_infections']:
        check('Nonnegative: '+c,master[c].dropna().ge(0).all())
        m=master[[c,c+'_low',c+'_high']].dropna()
        check('Ordered marginal limits: '+c,(m[c+'_low'].le(m[c])&m[c].le(m[c+'_high'])).all())
    with sqlite3.connect((ROOT/'data/processed/hiv_surveillance.db').as_uri()+'?mode=ro',uri=True) as con:
        check('SQLite integrity',con.execute('pragma integrity_check').fetchone()[0]=='ok')
        check('No foreign key violations',not con.execute('pragma foreign_key_check').fetchall())
        sql=pd.read_sql_query('select iso3,year,aids_deaths,art_coverage_pct,unreached_plhiv from v_southeast_asia_surveillance',con)
    j=sql.merge(master,on=['iso3','year'],suffixes=('_sql','_csv'),validate='one_to_one')
    for c in ['aids_deaths','art_coverage_pct','unreached_plhiv']:
        check('SQL/CSV parity: '+c,np.allclose(j[c+'_sql'],j[c+'_csv'],equal_nan=True))
    who=run_who_unaids_cross_validation(master)
    check('Four WHO feeds reconciled',len(who)==4)
    missing=sea[sea.year.eq(2025)][['iso3','country_name','aids_deaths_source','art_coverage_pct_source','virally_suppressed_all_pct_source']]
    audit=dict(passed_checks=len(checks),checks=checks,rows=len(master),entities=master.iso3.nunique(),sea_countries=11,
        who_matched=int(who.matched_country_years.sum()),censored_cells=censored,
        source_files={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data/raw').glob('*')) if p.is_file()})
    (ROOT/'reports/audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8',newline='\n')
    text=f"# Data quality audit\n\n{len(checks)} checks passed. {len(master):,} entity-years across {master.iso3.nunique()} entities (countries/territories and aggregates).\n\nSoutheast Asia: all 11 countries, 396 country-years, 176 rows from 2010 to 2025.\n\n## Source consistency\n\n{int(who.matched_country_years.sum()):,} uncensored country-year-indicator overlaps agree with the stored WHO feeds. This checks snapshot consistency only. WHO disseminates UNAIDS estimates and is not independent outcome validation. Unmatched rows and source hashes appear in the CSV and audit JSON. The bulk ZIP is an archived supplemental source, not a second independent validation dataset.\n\n## Missing and censored values in 2025\n\n{missing.to_markdown(index=False)}\n\nCensored values retain source text, threshold, and qualifier. Numeric point fields are missing for censored/suppressed values. No zero, midpoint, or threshold is substituted in the primary analysis.\n\n## Audit checks\n\n"+'\n'.join('- '+c for c in checks)+'\n'
    (ROOT/'reports/data_quality_audit.md').write_text(text,encoding='utf-8',newline='\n')
    print(f"Audit passed: {len(checks)} checks; WHO matched uncensored observations: {audit['who_matched']:,}")
    return audit
if __name__=='__main__':run_audit()
