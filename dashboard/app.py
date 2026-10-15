"""Portfolio dashboard for the stored UNAIDS 2026 and WDI snapshot."""
from pathlib import Path
import sys,sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from research_io import load_results,sha256
st.set_page_config(page_title='HIV trends and treatment access',page_icon='🎗️',layout='wide')
r=load_results()
@st.cache_data
def load_snapshot(fingerprint):
    return pd.read_csv(ROOT/'data/processed/southeast_asia_hiv_longitudinal_1990_2025.csv')
d=load_snapshot(r['data_sha256'])
st.title('HIV trends and treatment access')
st.caption('Dr. Aung Chit Moe, MBBS · Southeast Asia, 1990–2025 · UNAIDS 2026 estimates and World Bank WDI')
st.info('Stored research snapshot, updated October 2026. National estimates support descriptive comparisons and exploratory associations. This dashboard does not establish the causes of changes.')
st.sidebar.header('Trend filters')
countries=st.sidebar.multiselect('Countries',sorted(d.country_name.unique()),default=['Myanmar','Thailand','Cambodia','Indonesia','Philippines'])
years=st.sidebar.slider('Years',1990,2025,(2000,2025))
f=d[d.country_name.isin(countries)&d.year.between(*years)]
st.sidebar.caption('Filters apply to Trends and Data explorer. Other tabs show the fixed study samples and clearly stated periods.')
tabs=st.tabs(['Trends','Treatment cascade','Model comparisons','GDP comparison','Data explorer'])
with tabs[0]:
    metric=st.selectbox('Indicator',['aids_deaths','new_infections','plhiv','adult_prevalence_pct','art_coverage_pct','mortality_rate_in_plhiv_pct'],format_func=lambda v:dict(aids_deaths='Annual AIDS deaths (estimated count)',new_infections='Annual new HIV infections (estimated count)',plhiv='People living with HIV (estimated count)',adult_prevalence_pct='Adult prevalence, ages 15–49 (%)',art_coverage_pct='ART coverage (% of all PLHIV)',mortality_rate_in_plhiv_pct='Annual AIDS deaths / PLHIV (%)')[v])
    if f.empty:st.warning('Select at least one country and a period to display a trend.')
    else:
        st.plotly_chart(px.line(f,x='year',y=metric,color='country_name',markers=True,labels={metric:'Estimate','year':'Year'}),width='stretch')
        show=[c for c in ['country_name','year',metric,metric+'_source',metric+'_low',metric+'_high'] if c in f]
        st.dataframe(f[show],hide_index=True)
    st.caption('Censored or suppressed values appear as gaps. Source text retains < and > labels. Published lower/upper columns are marginal uncertainty limits. Annual deaths / PLHIV is not an individual fatality risk.')
    m=d[d.iso3.eq('MMR')].set_index('year');a,b=m.loc[2010],m.loc[2025]
    c1,c2,c3=st.columns(3)
    c1.metric('Myanmar annual AIDS deaths, 2025',f"{b.aids_deaths:,.0f}",f"{100*(b.aids_deaths/a.aids_deaths-1):+.1f}% since 2010",delta_color='inverse')
    c2.metric('Myanmar ART coverage, 2025',f"{b.art_coverage_pct:.0f}%",f"{b.art_coverage_pct-a.art_coverage_pct:+.0f} percentage points since 2010")
    c3.metric('Myanmar PLHIV, 2025',f"{b.plhiv:,.0f}")
    st.write('Myanmar’s ART coverage and estimated deaths changed over time. These aggregate data do not identify effects of conflict, COVID-19, decentralization, or specific programmes.')
with tabs[1]:
    st.header('Treatment cascade, 2025')
    c=pd.read_csv(ROOT/'reports/analysis_tables/cascade_2025_summary.csv');c=c[c.is_southeast_asia.eq(1)]
    st.write('The first 95 uses all PLHIV as denominator. The second uses diagnosed PLHIV. The third uses people on ART. Their population equivalents are 95%, 90.25% on ART, and 85.74% virally suppressed.')
    fields=['diagnosed_1st95_pct','on_art_2nd95_pct','virally_suppressed_3rd95_pct']
    view=c[['country_name']+[v+'_source' for v in fields]+['art_coverage_pct_source','virally_suppressed_all_pct_source']].copy()
    view.columns=['Country','Diagnosed / all PLHIV (%)','ART / diagnosed (%)','Suppressed / on ART (%)','ART / all PLHIV (%)','Suppressed / all PLHIV (%)']
    st.dataframe(view,hide_index=True)
    chart=c.melt(id_vars='country_name',value_vars=['art_coverage_pct','virally_suppressed_all_pct'],var_name='Indicator',value_name='Percent of all PLHIV')
    fig=px.bar(chart,x='country_name',y='Percent of all PLHIV',color='Indicator',barmode='group');fig.update_yaxes(range=[0,100]);st.plotly_chart(fig,width='stretch')
    gaps=pd.read_csv(ROOT/'reports/analysis_tables/treatment_gaps_2025.csv')
    st.subheader('Approximate number of PLHIV not on ART')
    st.plotly_chart(px.bar(gaps,x='country_name',y='unreached_plhiv',labels={'unreached_plhiv':'Approximate count','country_name':'Country'}),width='stretch')
    st.caption(f'PLHIV × (1 − ART coverage/100), based on rounded estimates. Available {len(gaps)} countries only. Brunei and Singapore are unavailable. Shares exclude these countries and are not complete regional totals. Marginal-bound scenarios in the download are not joint confidence intervals.')
    st.download_button('Download cascade and source labels',c.to_csv(index=False).encode(),'hiv_cascade_2025.csv','text/csv')
with tabs[2]:
    st.header('Exploratory ART–mortality associations, 2010–2025')
    models=pd.DataFrame(r['models'])
    selected=st.selectbox('Model specification',models.model_name)
    model=models[models.model_name.eq(selected)].iloc[0]
    st.metric('ART coefficient',f'{model.coefficient:.4f}')
    st.write(f"95% approximate interval [{model.ci_lower_95:.4f}, {model.ci_upper_95:.4f}]. N={model.n_observations} country-years, {model.n_countries} countries. {model.first_year}–{model.last_year}.")
    st.write('Units: outcome units per one percentage point of the ART regressor. Differenced models use annual changes. The population-denominator model uses deaths per 100,000 population. Other models use annual deaths / PLHIV ×100.')
    st.dataframe(models[['model_name','coefficient','robust_std_err','ci_lower_95','ci_upper_95','p_value','n_observations','n_countries']],hide_index=True)
    st.write(r['inference'])
    for note in r['limitations']:st.write('• '+note)
    loco=pd.DataFrame(r['leave_one_country_out']);st.subheader('Leave-one-country-out comparison');st.dataframe(loco[['model_name','coefficient','ci_lower_95','ci_upper_95','n_observations','n_countries']],hide_index=True)
    st.download_button('Download model results',models.to_csv(index=False).encode(),'hiv_model_comparisons.csv','text/csv')
with tabs[3]:
    st.header('National GDP and ART coverage, 2025')
    g=d[d.year.eq(2025)].dropna(subset=['gdp_per_capita_ppp','art_coverage_pct'])
    st.plotly_chart(px.scatter(g,x='gdp_per_capita_ppp',y='art_coverage_pct',hover_name='country_name',text='iso3',log_x=True,labels={'gdp_per_capita_ppp':'GDP per capita PPP, constant 2021 international $ (log axis)','art_coverage_pct':'ART / all PLHIV (%)'}),width='stretch')
    st.caption(f'Available same-year estimates: {len(g)} countries. Programme spending, financing, stigma, access barriers and delivery quality are not measured. This comparison cannot rank their importance against GDP.')
with tabs[4]:
    st.header('Data explorer')
    st.dataframe(f,hide_index=True)
    st.download_button('Download filtered data',f.to_csv(index=False).encode(),'hiv_filtered_snapshot.csv','text/csv')
    examples={'2025 treatment coverage':"SELECT country_name,iso3,year,art_coverage_pct,virally_suppressed_all_pct FROM v_southeast_asia_surveillance WHERE year=2025 AND is_southeast_asia=1 ORDER BY country_name",'Myanmar annual estimates':"SELECT year,plhiv,aids_deaths,new_infections,art_coverage_pct FROM v_southeast_asia_surveillance WHERE iso3='MMR' ORDER BY year"}
    selection=st.selectbox('Read-only SQL example',list(examples));st.code(examples[selection],language='sql')
    if st.button('Run SQL example'):
        with sqlite3.connect((ROOT/'data/processed/hiv_surveillance.db').as_uri()+'?mode=ro',uri=True) as con:
            result=pd.read_sql_query(examples[selection],con)
        st.dataframe(result,hide_index=True)
        st.download_button('Download SQL results',result.to_csv(index=False).encode(),'hiv_sql_example.csv','text/csv')
    st.caption('SQL numeric fields omit censored values. CSV downloads preserve source labels and qualifiers. No patient-level records are present.')
st.caption('Sources: UNAIDS 2026, WHO GHO consistency extracts, World Bank WDI. Source hashes, methods and limitations are available in the repository.')
