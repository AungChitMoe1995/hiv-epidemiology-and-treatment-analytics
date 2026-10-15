"""Six reproducible figures from the corrected snapshot. No causal interpretation."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
FILES=['fig1_myanmar_longitudinal_trajectory.png','fig2_southeast_asia_mortality_infection_divergence.png','fig3_unaids_95_95_95_cascade_2025.png','fig4_lagged_art_mortality_associations.png','fig5_gdp_vs_art_coverage_disparity.png','fig6_southeast_asia_art_trajectories_2010_2025.png']
def run_all():
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#18334A'})
    d=pd.read_csv(ROOT/'data/processed/southeast_asia_hiv_longitudinal_1990_2025.csv')
    tables=ROOT/'reports/analysis_tables';out=ROOT/'figures';out.mkdir(exist_ok=True)
    def save(fig,i,note):
        fig.text(.02,.015,note,fontsize=9,color='#526579')
        fig.tight_layout(rect=(0,.055,1,.96));fig.savefig(out/FILES[i],dpi=300);plt.close(fig)
    m=d[d.iso3.eq('MMR')]
    fig,ax=plt.subplots(2,1,figsize=(12,8),sharex=True)
    for c,color in [('new_infections','#087F78'),('aids_deaths','#BD5829')]:
        ax[0].plot(m.year,m[c]/1000,label=c.replace('_',' ').title(),color=color)
        ax[0].fill_between(m.year,m[c+'_low']/1000,m[c+'_high']/1000,color=color,alpha=.13)
    ax[0].set(ylabel='Annual estimated count (thousands)',title='Myanmar HIV estimates, 1990–2025');ax[0].legend()
    ax[1].plot(m.year,m.art_coverage_pct,color='#087F78',label='ART coverage')
    ax[1].set(xlabel='Year',ylabel='ART coverage (% of all PLHIV)',ylim=(0,100));ax[1].legend()
    save(fig,0,'UNAIDS 2026. Shading: published marginal 95% uncertainty limits. Changes do not identify their causes.')
    t=pd.read_csv(tables/'regional_trend_summary_2010_2025.csv');t=t[t.iso3.isin(d.iso3.unique())].sort_values('country_name')
    fig,axes=plt.subplots(1,2,figsize=(13,7),sharey=True)
    for ax,c,title in zip(axes,['pct_change_deaths','pct_change_new_infections'],['Annual AIDS deaths','Annual new infections']):
        ax.barh(t.country_name,t[c],color='#087F78');ax.axvline(0,color='gray');ax.set(xlabel='Change from 2010 to 2025 (%)',title=title)
    save(fig,1,'Rounded national estimates. Blank bars mean unavailable or censored endpoints, rather than zero change.')
    c=pd.read_csv(tables/'cascade_2025_summary.csv');c=c[c.is_southeast_asia.eq(1)].sort_values('country_name')
    fig,axes=plt.subplots(1,2,figsize=(14,7))
    for ax,col,title,target in zip(axes,['art_coverage_pct','virally_suppressed_all_pct'],['On ART among all PLHIV','Suppressed viral load among all PLHIV'],[90.25,85.7375]):
        ax.barh(c.country_name,c[col],color='#087F78');ax.axvline(target,color='#BD5829',ls='--',label=f'95–95–95 equivalent: {target:.2f}%');ax.set(xlim=(0,100),xlabel='% of all people living with HIV',title=title);ax.legend(fontsize=9)
    save(fig,2,'Direct reported population-denominator indicators. Conditional targets use different denominators: diagnosed, then treated.')
    r=pd.read_csv(tables/'panel_regression_models.csv');r=r.iloc[[1,3,4,6,7,10]]
    fig,ax=plt.subplots(figsize=(13,6))
    ax.errorbar(r.coefficient*10,np.arange(len(r)),xerr=[(r.coefficient-r.ci_lower_95)*10,(r.ci_upper_95-r.coefficient)*10],fmt='o',color='#087F78',capsize=4)
    ax.set_yticks(np.arange(len(r)),[f'{row.model_name} (N={row.n_observations}, G={row.n_countries})' for row in r.itertuples()]);ax.axvline(0,color='gray',ls='--')
    ax.set(xlabel='Difference in annual deaths / PLHIV (pp) per +10 pp ART',title='ART–mortality association varies with specification');ax.invert_yaxis()
    save(fig,3,'Exploratory associations. Approximate 95% country-clustered t intervals. UNAIDS model uncertainty is not propagated.')
    s=d[d.year.eq(2025)].dropna(subset=['gdp_per_capita_ppp','art_coverage_pct'])
    fig,ax=plt.subplots(figsize=(12,7));ax.scatter(s.gdp_per_capita_ppp,s.art_coverage_pct,s=55,color='#087F78')
    for row in s.itertuples():ax.annotate(row.country_name,(row.gdp_per_capita_ppp,row.art_coverage_pct),xytext=(5,5),textcoords='offset points',fontsize=10)
    ax.set(xscale='log',ylim=(0,105),xlim=(3000,60000),xlabel='GDP per capita, PPP (constant 2021 international $, log axis)',ylabel='ART coverage (% of all PLHIV)',title='GDP and ART coverage, available countries in 2025')
    save(fig,4,'World Bank WDI and UNAIDS 2026. Descriptive cross-section. Financing, policy and programme delivery are not measured.')
    fig,ax=plt.subplots(figsize=(13,7))
    for iso,g in d[d.year.ge(2010)].groupby('iso3'):
        if g.art_coverage_pct.notna().any():ax.plot(g.year,g.art_coverage_pct,label=g.country_name.iloc[0],lw=2)
    ax.axhline(90.25,color='gray',ls='--',label='95–95 equivalent: 90.25%')
    ax.set(xlabel='Year',ylabel='ART coverage (% of all PLHIV)',ylim=(0,100),title='ART coverage, 2010–2025');ax.legend(loc='center left',bbox_to_anchor=(1, .5),fontsize=10)
    save(fig,5,'All 11 Southeast Asian countries are in the data grid. Brunei and Singapore lack reportable ART estimates for 2025.')
    old=out/'fig4_lagged_art_mortality_dose_response.png'
    if old.exists():old.unlink()
    print('Generated six corrected figures at 300 dpi')
if __name__=='__main__':run_all()
