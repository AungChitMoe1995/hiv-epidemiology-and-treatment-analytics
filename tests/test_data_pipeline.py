"""
tests/test_data_pipeline.py
---------------------------
Pytest automated unit and integration tests for the HIV surveillance pipeline.
"""

import os
import sqlite3
import pandas as pd
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'hiv_surveillance.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

def test_raw_files_exist():
    """Verify essential raw files are present in data/raw."""
    assert os.path.exists(os.path.join(RAW_DIR, 'UNAIDS_HIV_estimates_1990_to_present.xlsx'))
    assert os.path.exists(os.path.join(RAW_DIR, 'wb_gdp_per_capita_current_usd.csv'))
    assert os.path.exists(os.path.join(RAW_DIR, 'who_gho_hiv_deaths.csv'))

def test_processed_master_dataset():
    """Verify processed global master CSV has expected dimensions and columns."""
    csv_path = os.path.join(PROCESSED_DIR, 'hiv_epidemiology_master_1990_2025.csv')
    assert os.path.exists(csv_path)
    df = pd.read_csv(csv_path)
    assert len(df) == 6624
    assert 'aids_deaths' in df.columns
    assert 'art_coverage_pct' in df.columns
    assert 'treatment_gap_pct' in df.columns
    assert df['year'].min() == 1990
    assert df['year'].max() == 2025

def test_southeast_asia_panel():
    """Verify high-resolution Southeast Asia panel."""
    csv_path = os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv')
    assert os.path.exists(csv_path)
    df = pd.read_csv(csv_path)
    assert len(df) == 176  # 11 countries * 16 years
    mmr = df[df['iso3'] == 'MMR']
    assert len(mmr) == 16
    assert mmr['aids_deaths'].notna().all()
    assert mmr['art_coverage_pct'].notna().all()

def test_sqlite_database_and_view():
    """Verify SQLite database integrity and analytical view."""
    assert os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check table row counts
    cur.execute("SELECT COUNT(*) FROM dim_country")
    assert cur.fetchone()[0] == 184
    
    cur.execute("SELECT COUNT(*) FROM fact_hiv_estimates")
    assert cur.fetchone()[0] == 6624
    
    cur.execute("SELECT COUNT(*) FROM fact_treatment_cascade")
    assert cur.fetchone()[0] == 2944
    
    # Query view
    cur.execute("SELECT COUNT(*) FROM v_southeast_asia_surveillance WHERE iso3 = 'MMR' AND year = 2025")
    row = cur.fetchone()
    assert row[0] == 1
    
    conn.close()

def test_epidemiological_ranges():
    """Verify percentages and counts fall within plausible epidemiological ranges."""
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    # Valid coverage between 0 and 100
    valid_art = df['art_coverage_pct'].dropna()
    assert (valid_art >= 0).all() and (valid_art <= 100).all()
    
    # Valid adult prevalence between 0 and 50%
    valid_prev = df['adult_prevalence_pct'].dropna()
    assert (valid_prev >= 0).all() and (valid_prev <= 50).all()
    
    # No negative deaths or infections
    valid_deaths = df['aids_deaths'].dropna()
    assert (valid_deaths >= 0).all()

def test_lag_computation():
    """Verify that lag calculations correctly match previous-year values within country."""
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    tha = df[df['iso3'] == 'THA'].sort_values('year').reset_index(drop=True)
    # Check lag 1
    for i in range(1, len(tha)):
        assert tha.loc[i, 'art_coverage_lag1'] == tha.loc[i-1, 'art_coverage_pct']

def test_cascade_upper_bounds_parsed():
    """Verify >95 and >98 upper-bounded cascade values are parsed accurately."""
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    khm_2025 = df[(df['iso3'] == 'KHM') & (df['year'] == 2025)].iloc[0]
    tha_2025 = df[(df['iso3'] == 'THA') & (df['year'] == 2025)].iloc[0]
    assert khm_2025['diagnosed_1st95_pct'] == 95.0
    assert khm_2025['on_art_2nd95_pct'] == 98.0
    assert khm_2025['virally_suppressed_3rd95_pct'] == 98.0
    assert tha_2025['virally_suppressed_3rd95_pct'] == 98.0

def test_global_million_suffix_parsed():
    """Verify 'm' million suffix values in Global and Asia-Pacific benchmarks are scaled to exact counts."""
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'regional_global_benchmarks_1990_2025.csv'))
    wld_2025 = df[(df['iso3'] == '03M49WLD') & (df['year'] == 2025)].iloc[0]
    ap_2025 = df[(df['iso3'] == 'UNAAP') & (df['year'] == 2025)].iloc[0]
    assert wld_2025['plhiv'] == 41000000.0
    assert wld_2025['new_infections'] == 1200000.0
    assert ap_2025['plhiv'] == 7100000.0

def test_all_6_figures_exist():
    """Verify all 6 publication-grade 300 DPI PNG figures exist and are non-empty."""
    fig_dir = os.path.join(BASE_DIR, 'figures')
    expected_figs = [
        'fig1_myanmar_longitudinal_trajectory.png',
        'fig2_southeast_asia_mortality_infection_divergence.png',
        'fig3_unaids_95_95_95_cascade_2025.png',
        'fig4_lagged_art_mortality_dose_response.png',
        'fig5_gdp_vs_art_coverage_disparity.png',
        'fig6_southeast_asia_art_trajectories_2010_2025.png'
    ]
    for fname in expected_figs:
        fpath = os.path.join(fig_dir, fname)
        assert os.path.exists(fpath), f"Missing figure: {fname}"
        assert os.path.getsize(fpath) > 100_000, f"Figure too small: {fname}"

def test_powerpoint_presentation():
    """Verify the 22-slide uncluttered widescreen PowerPoint research briefing exists in both locations."""
    from pptx import Presentation
    for pptx_path in [
        os.path.join(BASE_DIR, 'docs', 'presentation', 'hiv_epidemiology_research_briefing.pptx'),
        os.path.join(BASE_DIR, 'reports', 'hiv_epidemiology_research_briefing.pptx')
    ]:
        assert os.path.exists(pptx_path)
        prs = Presentation(pptx_path)
        assert len(prs.slides) == 22

