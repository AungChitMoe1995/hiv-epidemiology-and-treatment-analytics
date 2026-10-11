"""
dashboard/app.py
----------------
Interactive Streamlit Surveillance Dashboard for:
HIV Epidemiological Trends and Treatment Disparities in Southeast Asia (1990-2025).
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="HIV Surveillance & Treatment Analytics | Southeast Asia",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'hiv_surveillance.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df_long = pd.read_sql_query("SELECT * FROM v_southeast_asia_surveillance ORDER BY country_name, year", conn)
    conn.close()
    return df_long

df_master = load_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.title("🎗️ Surveillance Controls")
st.sidebar.markdown("**Focus Group:** Southeast Asia & Benchmarks")

all_countries = sorted(df_master['country_name'].unique().tolist())
default_selection = ['Myanmar', 'Thailand', 'Cambodia', 'Indonesia', 'Philippines']

selected_countries = st.sidebar.multiselect(
    "Select Countries / Benchmarks:",
    options=all_countries,
    default=[c for c in default_selection if c in all_countries]
)

year_range = st.sidebar.slider(
    "Select Analysis Period:",
    min_value=1990,
    max_value=2025,
    value=(2000, 2025),
    step=1
)

df_filtered = df_master[
    (df_master['country_name'].isin(selected_countries)) &
    (df_master['year'] >= year_range[0]) &
    (df_master['year'] <= year_range[1])
].copy()

# ----------------- HEADER & KPI BANNER -----------------
st.title("HIV Epidemiological Transitions & Treatment Disparities")
st.subheader("A Comparative Longitudinal Analysis of Myanmar, Southeast Asia, and Global Benchmarks (1990–2025)")
st.markdown("""
*Investigator:* Clinical Medical Doctor & Healthcare Data Analyst (Myanmar / Public Health Research)  
*Data Sources:* UNAIDS 2026 Epidemiological Estimates, WHO Global Health Observatory, World Bank World Development Indicators.
""")

# Top Myanmar KPIs
mmr_2025 = df_master[(df_master['iso3'] == 'MMR') & (df_master['year'] == 2025)].iloc[0]
mmr_2010 = df_master[(df_master['iso3'] == 'MMR') & (df_master['year'] == 2010)].iloc[0]

deaths_chg = ((mmr_2025['aids_deaths'] - mmr_2010['aids_deaths']) / mmr_2010['aids_deaths']) * 100
art_gain = mmr_2025['art_coverage_pct'] - mmr_2010['art_coverage_pct']

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Myanmar PLHIV (2025)", f"{mmr_2025['plhiv']:,.0f}", "+24% since 2010 (Survival Expansion)")
col2.metric("Myanmar ART Coverage", f"{mmr_2025['art_coverage_pct']:.0f}%", f"+{art_gain:.0f}% pts since 2010")
col3.metric("Annual AIDS Deaths", f"{mmr_2025['aids_deaths']:,.0f}", f"{deaths_chg:+.1f}% since 2010")
col4.metric("Annual New Infections", f"{mmr_2025['new_infections']:,.0f}", "-44.1% since 2010")
col5.metric("Treatment Gap (Untreated)", f"{mmr_2025['unreached_plhiv']:,.0f}", f"{mmr_2025['treatment_gap_pct']:.0f}% of PLHIV")

st.markdown("---")

# ----------------- NAVIGATION TABS -----------------
tabs = st.tabs([
    "📈 1. Long-Term Trends & Myanmar Focus",
    "🎯 2. Cascade & Treatment Disparities",
    "🔬 3. Econometric Lagged Modeling",
    "💰 4. Socioeconomic Wealth vs. Health",
    "📊 5. Data Explorer & SQL Console"
])

# ----------------- TAB 1: TRENDS & MYANMAR FOCUS -----------------
with tabs[0]:
    st.header("1. Longitudinal Epidemiological Trajectories (1990–2025)")
    st.markdown("""
    Explore how the scale-up of combination antiretroviral therapy (ART) drove mortality reductions while adult prevalence 
    remained stable due to the **prevalence paradox** (extending life expectancy turns an acute fatal illness into a manageable chronic disease).
    """)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        metric_choice = st.selectbox(
            "Select Primary Indicator to Plot:",
            options=[
                ('aids_deaths', 'Annual AIDS-Related Deaths (Counts)'),
                ('new_infections', 'Annual New HIV Infections (Counts)'),
                ('art_coverage_pct', 'Antiretroviral Therapy (ART) Coverage (%)'),
                ('adult_prevalence_pct', 'Adult HIV Prevalence Ages 15-49 (%)'),
                ('mortality_rate_in_plhiv_pct', 'Crude AIDS Mortality Rate in PLHIV (%)'),
                ('aids_mortality_rate_per100k_pop', 'AIDS Mortality Rate per 100k General Population')
            ],
            format_func=lambda x: x[1]
        )
        
        fig_trend = px.line(
            df_filtered,
            x='year',
            y=metric_choice[0],
            color='country_name',
            title=f"Temporal Trends: {metric_choice[1]} ({year_range[0]}–{year_range[1]})",
            markers=True
        )
        fig_trend.update_layout(hovermode='x unified', height=450)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        st.subheader("Clinical Insights: Myanmar Epidemiological Dynamics")
        st.markdown("""
        * **2010–2020 Rapid Expansion Phase:**
          Myanmar achieved an extraordinary scale-up of decentralized ART through the National AIDS Programme and partner clinics. 
          Coverage surged from **12% to 69%**, directly driving a **63.3% decline in AIDS-related deaths** (12,000 down to 4,400).
        * **2021–2022 Healthcare System Shock:**
          Amid acute political crisis and COVID-19 health system strain, ART coverage dipped to **66% in 2021**, leading to a measurable 
          **mortality rebound to 4,800 deaths in 2022 (+11.6%)**. By 2025, coverage recovered to **73%** and mortality stabilized at 4,400.
        * **The Prevalence Dynamic:**
          Adult prevalence remained at **0.9%** while total PLHIV grew from 250,000 to 310,000. People living with HIV are living decades 
          longer, demonstrating the life-saving success of continuous ART.
        """)
        
        # Myanmar specific timeline
        mmr_chart = df_master[df_master['iso3'] == 'MMR'].sort_values('year')
        fig_mmr = go.Figure()
        fig_mmr.add_trace(go.Scatter(x=mmr_chart['year'], y=mmr_chart['new_infections']/1000, name='New Infections (k)', line=dict(color='#E67E22', width=2.5)))
        fig_mmr.add_trace(go.Scatter(x=mmr_chart['year'], y=mmr_chart['aids_deaths']/1000, name='AIDS Deaths (k)', line=dict(color='#8E44AD', width=2.5)))
        fig_mmr.update_layout(title="Myanmar: Incident Infections vs. AIDS Deaths (Thousands)", height=280, margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_mmr, use_container_width=True)

# ----------------- TAB 2: CASCADE & DISPARITIES -----------------
with tabs[1]:
    st.header("2. Treatment Cascade & Regional Disparities (2025)")
    st.markdown("""
    Progress toward the UNAIDS 95-95-95 targets varies widely across Southeast Asia. 
    While regional leaders (Cambodia and Thailand) approach or surpass the targets, the Philippines and Indonesia face severe treatment gaps.
    """)
    
    col_c1, col_c2 = st.columns(2)
    
    df_2025 = df_master[(df_master['year'] == 2025) & (df_master['is_southeast_asia'] == 1)].dropna(subset=['art_coverage_pct']).sort_values('art_coverage_pct', ascending=True)
    
    with col_c1:
        fig_casc = go.Figure()
        fig_casc.add_trace(go.Bar(y=df_2025['country_name'], x=df_2025['diagnosed_1st95_pct'], name='1st 95: % Diagnosed', orientation='h', marker_color='#3498DB'))
        fig_casc.add_trace(go.Bar(y=df_2025['country_name'], x=df_2025['on_art_2nd95_pct'], name='2nd 95: % on ART', orientation='h', marker_color='#2ECC71'))
        fig_casc.add_trace(go.Bar(y=df_2025['country_name'], x=df_2025['virally_suppressed_3rd95_pct'], name='3rd 95: % Virally Suppressed', orientation='h', marker_color='#9B59B6'))
        fig_casc.add_vline(x=95, line_dash='dash', line_color='red', annotation_text='95% Target')
        fig_casc.update_layout(barmode='group', title="UNAIDS 95-95-95 Cascade Progress (2025)", height=480)
        st.plotly_chart(fig_casc, use_container_width=True)
        
    with col_c2:
        df_gap_sorted = df_2025.sort_values('unreached_plhiv', ascending=True)
        fig_gap = px.bar(
            df_gap_sorted,
            y='country_name',
            x='unreached_plhiv',
            orientation='h',
            color='treatment_gap_pct',
            color_continuous_scale='Reds',
            title="Absolute Treatment Gap: Untreated PLHIV (2025)",
            labels={'unreached_plhiv': 'Untreated PLHIV (Count)', 'treatment_gap_pct': 'Gap (%)'}
        )
        fig_gap.update_layout(height=480)
        st.plotly_chart(fig_gap, use_container_width=True)
        
    st.subheader("Regional Epidemiological Archetypes")
    arch_df = pd.read_csv(os.path.join(BASE_DIR, 'reports', 'analysis_tables', 'archetype_classification.csv'))
    st.dataframe(arch_df[['country_name', 'art_coverage_2025', 'treatment_gap_pct', 'unreached_plhiv_2025', 'epidemiological_archetype', 'clinical_rationale']], use_container_width=True)

# ----------------- TAB 3: ECONOMETRIC MODELING -----------------
with tabs[2]:
    st.header("3. Econometric Panel Regressions (Fixed Effects & Lag Structure)")
    st.markdown("""
    Evaluating the within-country causal association between ART coverage and mortality reductions. 
    By demeaning by country (fixed effects), we control for time-invariant national confounders (baseline infrastructure, geography).
    """)
    
    col_m1, col_m2 = st.columns([3, 2])
    
    with col_m1:
        # Scatterplot with regression fit
        df_panel = df_master[(df_master['year'] >= 2010) & (df_master['is_southeast_asia'] == 1)].dropna(subset=['mortality_rate_in_plhiv_pct', 'art_coverage_pct']).copy()
        df_panel['art_lag1'] = df_panel.groupby('iso3')['art_coverage_pct'].shift(1)
        
        fig_fe = px.scatter(
            df_panel.dropna(subset=['art_lag1']),
            x='art_lag1',
            y='mortality_rate_in_plhiv_pct',
            color='country_name',
            trendline='ols',
            title="1-Year Lagged ART Coverage vs. Crude AIDS Mortality Rate in PLHIV (%)",
            labels={'art_lag1': '1-Year Lagged ART Coverage (t-1, %)', 'mortality_rate_in_plhiv_pct': 'AIDS Mortality Rate in PLHIV (t, %)'}
        )
        fig_fe.update_layout(height=480)
        st.plotly_chart(fig_fe, use_container_width=True)
        
    with col_m2:
        st.subheader("Panel Regression Model Summary")
        reg_models = pd.read_csv(os.path.join(BASE_DIR, 'reports', 'analysis_tables', 'panel_regression_models.csv'))
        st.dataframe(reg_models[['model_name', 'independent_variable', 'coefficient', 'robust_std_err', 't_statistic', 'p_value', 'r_squared_within']], use_container_width=True)
        
        st.markdown("""
        **Epidemiological Interpretation:**
        * **1-Year Lagged Model (Model 2):** $\\beta = -0.0491$ ($t = -14.20, p < 0.00001, R^2_{\\text{within}} = 0.687$).
        * **Clinical Meaning:** For every **10 percentage point increase in national ART coverage** in year $t-1$, the mortality rate among people living with HIV decreases by **0.49 percentage points** in year $t$.
        * **Controlling for Economic Growth (Model 4):** Even after controlling for logarithmic GDP per capita, the protective effect of ART coverage remains highly significant ($\\beta = -0.0624, p < 0.00001$).
        """)

# ----------------- TAB 4: SOCIOECONOMIC WEALTH VS HEALTH -----------------
with tabs[3]:
    st.header("4. Macroeconomic Wealth vs. Epidemic Control (2025)")
    st.markdown("""
    Does economic wealth guarantee high ART coverage? Our analysis shows that in Southeast Asia, **wealth alone does not guarantee treatment access**.
    """)
    
    col_s1, col_s2 = st.columns([3, 2])
    with col_s1:
        df_socio = df_master[(df_master['year'] == 2025) & (df_master['is_southeast_asia'] == 1)].dropna(subset=['gdp_per_capita_ppp', 'art_coverage_pct'])
        
        fig_gdp = px.scatter(
            df_socio,
            x='gdp_per_capita_ppp',
            y='art_coverage_pct',
            size='plhiv',
            color='treatment_gap_pct',
            color_continuous_scale='Viridis_r',
            text='country_name',
            log_x=True,
            title="GDP per Capita (PPP 2021 Int$, Log Scale) vs. ART Coverage (2025)",
            labels={'gdp_per_capita_ppp': 'GDP per Capita PPP ($)', 'art_coverage_pct': 'ART Coverage (%)'}
        )
        fig_gdp.update_traces(textposition='top center')
        fig_gdp.update_layout(height=500)
        st.plotly_chart(fig_gdp, use_container_width=True)
        
    with col_s2:
        st.subheader("The Health Financing Paradox")
        st.markdown(r"""
        * **Lower-Income Overachievers:**
          **Cambodia** (GDP PPP \$7,300) and **Myanmar** (GDP PPP \$5,137) achieved **95% and 73% ART coverage**, outperforming richer neighbors.
        * **Middle-Income Underachievers:**
          **Indonesia** (GDP PPP \$15,091) and **Philippines** (GDP PPP \$10,748) lag at **48% and 41% coverage**.
        * **Key Health Policy Takeaway:**
          In concentrated epidemics, decentralized vertical disease control programs, international donor grant absorption (Global Fund), 
          and community-led harm reduction matter far more than aggregate GDP.
        """)

# ----------------- TAB 5: DATA EXPLORER & SQL CONSOLE -----------------
with tabs[4]:
    st.header("5. Data Explorer & Live SQL Query Console")
    st.markdown("Query the verified SQLite surveillance database (`hiv_surveillance.db`) in real time.")
    
    sql_input = st.text_area(
        "Enter SQL Query:",
        value="""SELECT 
    country_name, iso3, year, plhiv, aids_deaths, art_coverage_pct, treatment_gap_pct 
FROM v_southeast_asia_surveillance 
WHERE year = 2025 AND is_southeast_asia = 1 
ORDER BY art_coverage_pct DESC;""",
        height=140
    )
    
    if st.button("Execute SQL Query"):
        try:
            conn = sqlite3.connect(DB_PATH)
            query_res = pd.read_sql_query(sql_input, conn)
            conn.close()
            st.success(f"Query returned {len(query_res)} rows.")
            st.dataframe(query_res, use_container_width=True)
            
            csv = query_res.to_csv(index=False).encode('utf-8')
            st.download_button("Download Query Results (CSV)", csv, "query_results.csv", "text/csv")
        except Exception as e:
            st.error(f"SQL Error: {e}")
            
    st.subheader("Underlying Longitudinal Surveillance Dataset")
    st.dataframe(df_filtered.head(50), use_container_width=True)

st.markdown("---")
st.caption("Developed by Clinical Doctor & Health Data Analyst | Reproducible Public Health Surveillance Pipeline | October 2026")
