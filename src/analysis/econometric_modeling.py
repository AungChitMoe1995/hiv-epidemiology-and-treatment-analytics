"""Exploratory country/year panel associations. Country-clustered t inference."""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
ELIGIBLE = ['MMR','THA','VNM','KHM','IDN','MYS','PHL','LAO','TLS']
Y = 'mortality_rate_in_plhiv_pct'

def estimate(data, name, x='art_coverage_lag1', year_effects=False, gdp=False, outcome=Y):
    cols = [outcome,x,'iso3','year'] + (['log_gdp_pc_ppp'] if gdp else [])
    d=data.dropna(subset=cols).copy()
    formula=f'{outcome} ~ {x} + C(iso3)' + (' + C(year)' if year_effects else '') + (' + log_gdp_pc_ppp' if gdp else '')
    fit=smf.ols(formula,d).fit(cov_type='cluster',cov_kwds={'groups':d.iso3,'use_correction':True,'df_correction':True},use_t=True)
    ci=fit.conf_int().loc[x]
    return dict(model_name=name,dependent_variable=outcome,independent_variable=x,coefficient=float(fit.params[x]),
        robust_std_err=float(fit.bse[x]),t_statistic=float(fit.tvalues[x]),p_value=float(fit.pvalues[x]),
        ci_lower_95=float(ci.iloc[0]),ci_upper_95=float(ci.iloc[1]),r_squared=float(fit.rsquared),
        n_observations=int(fit.nobs),n_countries=int(d.iso3.nunique()),inference_df=int(d.iso3.nunique()-1),
        first_year=int(d.year.min()),last_year=int(d.year.max()),year_effects=year_effects,
        countries=','.join(sorted(d.iso3.unique())),design_rank=int(np.linalg.matrix_rank(fit.model.exog)))

def run_econometric_analysis():
    panel=pd.read_csv(ROOT/'data/processed/southeast_asia_hiv_panel_2010_2025.csv')
    panel=panel[panel.iso3.isin(ELIGIBLE)].sort_values(['iso3','year']).copy()
    panel['log_gdp_pc_ppp']=np.log(panel.gdp_per_capita_ppp.where(panel.gdp_per_capita_ppp.gt(0)))
    specs=[('Country FE: current ART','art_coverage_pct',False,False),
           ('Country FE: lag 1','art_coverage_lag1',False,False),
           ('Country FE: lag 2','art_coverage_lag2',False,False),
           ('Country and year FE: lag 1','art_coverage_lag1',True,False),
           ('Country and year FE: lag 1 + GDP','art_coverage_lag1',True,True)]
    rows=[estimate(panel,n,x,t,g) for n,x,t,g in specs]
    common=panel.dropna(subset=[Y,'art_coverage_lag1','log_gdp_pc_ppp'])
    rows.append(estimate(common,'Country FE: common GDP sample'))
    rows.append(estimate(panel[panel.year.le(2019)],'Country and year FE: 2011-2019',year_effects=True))
    rows.append(estimate(panel[panel.iso3.ne('MMR')],'Country and year FE: omit Myanmar',year_effects=True))
    rows.append(estimate(panel,'Population denominator: country/year FE',year_effects=True,outcome='aids_mortality_rate_per100k_pop'))
    # Differences require consecutive calendar years and complete values at both endpoints.
    for col in [Y,'art_coverage_lag1']:
        panel['d_'+col]=panel.groupby('iso3')[col].diff().where(panel.groupby('iso3').year.diff().eq(1))
    rows.append(estimate(panel,'First differences with country/year effects',x='d_art_coverage_lag1',outcome='d_'+Y,year_effects=True))
    loco=[estimate(panel[panel.iso3.ne(iso)],'Omit '+iso,year_effects=True) for iso in sorted(common.iso3.unique())]
    # Boundary sensitivity deliberately substitutes disclosed censor thresholds. These are not observations.
    bounded=panel.copy()
    for c in ['aids_deaths','plhiv','art_coverage_pct']:
        bounded[c]=bounded[c].fillna(bounded[c+'_threshold'])
    bounded[Y]=100*bounded.aids_deaths/bounded.plhiv
    bounded['art_coverage_lag1']=bounded.groupby('iso3').art_coverage_pct.shift(1).where(bounded.groupby('iso3').year.diff().eq(1))
    rows.append(estimate(bounded,'Threshold substitution sensitivity',year_effects=True))
    tables=ROOT/'reports/analysis_tables';tables.mkdir(parents=True,exist_ok=True)
    out=pd.DataFrame(rows);out.to_csv(tables/'panel_regression_models.csv',index=False,lineterminator='\n')
    pd.DataFrame(loco).to_csv(tables/'leave_one_country_out.csv',index=False,lineterminator='\n')
    panel[[Y,'art_coverage_pct','art_coverage_lag1','gdp_per_capita_ppp']].corr().to_csv(tables/'correlation_matrix.csv',lineterminator='\n')
    plot=panel.dropna(subset=[Y,'art_coverage_lag1']).copy()
    plot['mortality_rate_demeaned']=plot[Y]-plot.groupby('iso3')[Y].transform('mean')
    plot['art_lag1_demeaned']=plot.art_coverage_lag1-plot.groupby('iso3').art_coverage_lag1.transform('mean')
    plot.to_csv(tables/'panel_fe_demeaned_model2.csv',index=False,lineterminator='\n')
    result={'analysis':'Exploratory ecological associations, UNAIDS 2026 snapshot',
      'data_sha256':hashlib.sha256((ROOT/'data/processed/southeast_asia_hiv_panel_2010_2025.csv').read_bytes()).hexdigest(),
      'models':rows,'leave_one_country_out':loco,
      'inference':'Country-clustered standard errors, full dummy design rank correction, t reference with G-1 degrees of freedom. Few clusters make intervals approximate.',
      'limitations':['UNAIDS mortality estimates incorporate ART inputs and assumed survival. Associations partly reflect model construction.',
       'Both ART coverage and deaths/PLHIV use estimated PLHIV denominators. The ratio is not a cohort fatality risk.',
       'Annual estimates are rounded and serially related. Regression intervals do not propagate UNAIDS estimation uncertainty.',
       'Year effects remove shared annual shocks only. Residual confounding, reverse causality and country-specific trends remain.',
       'Primary analysis excludes censored values. Boundary substitution is a sensitivity scenario, not an estimate of missing values.']}
    (ROOT/'reports/results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    print(out[['model_name','coefficient','ci_lower_95','ci_upper_95','n_observations','n_countries']].to_string(index=False))
    return out

if __name__=='__main__': run_econometric_analysis()
