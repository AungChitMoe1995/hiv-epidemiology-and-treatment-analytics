"""
src/cleaning/clean_and_harmonize.py
-----------------------------------
Ingests raw UNAIDS estimates, treatment cascade sheets, and World Bank socioeconomic
datasets. Performs rigorous cleaning, type parsing, inequality threshold handling,
derived indicator calculation, and country-year harmonization.

Outputs:
  - data/processed/hiv_epidemiology_master_1990_2025.csv (Full global panel)
  - data/processed/southeast_asia_hiv_panel_2010_2025.csv (SEA analytical panel)
  - data/processed/regional_global_benchmarks_1990_2025.csv (Benchmarks)
"""

import os
import sys
import logging
import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('DataCleaning')

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw'))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed'))
os.makedirs(PROCESSED_DIR, exist_ok=True)

SEA_COUNTRIES = ['MMR', 'THA', 'VNM', 'KHM', 'IDN', 'MYS', 'PHL', 'LAO', 'TLS', 'SGP', 'BRN']
BENCHMARKS = ['03M49WLD', 'UNAAP', 'UNAESA', 'UNAWCA', 'UNAMENA', 'UNAEECA', 'UNALA', 'UNACAR', 'UNAWE']

def parse_num_val(val):
    """
    Parses messy surveillance numeric strings:
    - Removes whitespace ('12 000' -> 12000.0)
    - Removes commas ('12,000' -> 12000.0)
    - Censored values (<100, >95) remain missing numerically; source, qualifier and threshold columns preserve their meaning
    - Handles million suffixes ('32.5 m' -> 32500000.0, '6.0 m' -> 6000000.0)
    - Replaces '...' (suppressed) or empty with NaN
    """
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ['...', '', 'nan', 'None', '-']:
        return np.nan
    if s.startswith(('<', '>')):
        return np.nan  # Censored bounds are not exact point estimates.
    s = s.replace(' ', '').replace(',', '')
    multiplier = 1.0
    if s.lower().endswith('m'):
        multiplier = 1_000_000.0
        s = s[:-1]
    try:
        return float(s) * multiplier
    except Exception:
        return np.nan

def clean_unaids_estimates(xlsx_path: str) -> pd.DataFrame:
    logger.info("Parsing sheet: HIV2026Estimates_ByYear ...")
    xl = pd.ExcelFile(xlsx_path)
    df_raw = xl.parse('HIV2026Estimates_ByYear', header=None).iloc[6:]
    
    # Filter rows that have a valid integer year in Col 0
    df_valid = df_raw[pd.to_numeric(df_raw[0], errors='coerce').notna()].copy()
    df_valid[0] = df_valid[0].astype(int)
    
    col_mapping = {
        0: 'year',
        1: 'iso3',
        2: 'country_name',
        3: 'adult_prevalence_pct',
        4: 'adult_prevalence_low',
        5: 'adult_prevalence_high',
        12: 'aids_deaths',
        13: 'aids_deaths_low',
        14: 'aids_deaths_high',
        15: 'child_aids_deaths',
        18: 'adult_aids_deaths',
        21: 'child_plhiv',
        24: 'women_plhiv',
        27: 'adult_plhiv',
        30: 'plhiv',
        31: 'plhiv_low',
        32: 'plhiv_high',
        33: 'adult_incidence_per1000',
        34: 'adult_incidence_low',
        35: 'adult_incidence_high',
        36: 'incidence_rate_per1000',
        37: 'incidence_rate_low',
        38: 'incidence_rate_high',
        48: 'new_infections',
        49: 'new_infections_low',
        50: 'new_infections_high'
    }
    
    df_clean = df_valid[list(col_mapping.keys())].copy()
    df_clean.rename(columns=col_mapping, inplace=True)
    df_clean['iso3'] = df_clean['iso3'].astype(str).str.strip()
    df_clean['country_name'] = df_clean['country_name'].astype(str).str.strip()
    df_clean['country_name'] = df_clean['country_name'].replace({
        'Lao People Democratic Republic': 'Lao PDR'
    })
    
    # Parse all numeric columns
    numeric_cols = [c for c in df_clean.columns if c not in ['year', 'iso3', 'country_name']]
    for c in numeric_cols:
        raw = df_clean[c].fillna('...').astype(str).str.strip()
        df_clean[c + '_source'] = raw
        df_clean[c + '_qualifier'] = raw.map(lambda v: v[0] if v.startswith(('<', '>')) else ('missing' if pd.isna(parse_num_val(v)) else '='))
        df_clean[c + '_threshold'] = raw.map(lambda v: parse_num_val(v[1:]) if v.startswith(('<', '>')) else np.nan)
        df_clean[c] = raw.map(parse_num_val)
        
    logger.info(f"Cleaned Estimates: {len(df_clean):,} records, {df_clean['iso3'].nunique()} entities, years {df_clean['year'].min()}-{df_clean['year'].max()}.")
    return df_clean

def clean_unaids_cascade(xlsx_path: str) -> pd.DataFrame:
    logger.info("Parsing sheet: HIV-Test-&-Treat_ByYear ...")
    xl = pd.ExcelFile(xlsx_path)
    df_raw = xl.parse('HIV-Test-&-Treat_ByYear', header=None).iloc[6:]
    
    df_valid = df_raw[pd.to_numeric(df_raw[0], errors='coerce').notna()].copy()
    df_valid[0] = df_valid[0].astype(int)
    
    col_mapping = {
        0: 'year',
        1: 'iso3',
        3: 'diagnosed_1st95_pct',
        4: 'diagnosed_1st95_low',
        5: 'diagnosed_1st95_high',
        18: 'art_coverage_pct',
        19: 'art_coverage_low',
        20: 'art_coverage_high',
        33: 'on_art_2nd95_pct',
        34: 'on_art_2nd95_low',
        35: 'on_art_2nd95_high',
        48: 'virally_suppressed_all_pct',
        49: 'virally_suppressed_all_low',
        50: 'virally_suppressed_all_high',
        63: 'virally_suppressed_3rd95_pct',
        64: 'virally_suppressed_3rd95_low',
        65: 'virally_suppressed_3rd95_high'
    }
    
    df_clean = df_valid[list(col_mapping.keys())].copy()
    df_clean.rename(columns=col_mapping, inplace=True)
    df_clean['iso3'] = df_clean['iso3'].astype(str).str.strip()
    
    numeric_cols = [c for c in df_clean.columns if c not in ['year', 'iso3']]
    for c in numeric_cols:
        raw = df_clean[c].fillna('...').astype(str).str.strip()
        df_clean[c + '_source'] = raw
        df_clean[c + '_qualifier'] = raw.map(lambda v: v[0] if v.startswith(('<', '>')) else ('missing' if pd.isna(parse_num_val(v)) else '='))
        df_clean[c + '_threshold'] = raw.map(lambda v: parse_num_val(v[1:]) if v.startswith(('<', '>')) else np.nan)
        df_clean[c] = raw.map(parse_num_val)
        
    logger.info(f"Cleaned Cascade: {len(df_clean):,} records, {df_clean['iso3'].nunique()} entities, years {df_clean['year'].min()}-{df_clean['year'].max()}.")
    return df_clean

def load_world_bank_data() -> pd.DataFrame:
    logger.info("Loading World Bank WDI datasets ...")
    gdp_curr_path = os.path.join(RAW_DIR, 'wb_gdp_per_capita_current_usd.csv')
    gdp_ppp_path = os.path.join(RAW_DIR, 'wb_gdp_per_capita_ppp_constant2021.csv')
    pop_path = os.path.join(RAW_DIR, 'wb_population_total.csv')
    
    df_gdp_c = pd.read_csv(gdp_curr_path)
    df_gdp_p = pd.read_csv(gdp_ppp_path)
    df_pop = pd.read_csv(pop_path)
    
    # Filter valid country codes
    df_gdp_c = df_gdp_c[df_gdp_c['country_id'].notna()][['country_id', 'year', 'value']].rename(columns={'country_id': 'iso3', 'value': 'gdp_per_capita_usd'})
    df_gdp_p = df_gdp_p[df_gdp_p['country_id'].notna()][['country_id', 'year', 'value']].rename(columns={'country_id': 'iso3', 'value': 'gdp_per_capita_ppp'})
    df_pop = df_pop[df_pop['country_id'].notna()][['country_id', 'year', 'value']].rename(columns={'country_id': 'iso3', 'value': 'population_total'})
    
    df_wb = pd.merge(df_gdp_c, df_gdp_p, on=['iso3', 'year'], how='outer')
    df_wb = pd.merge(df_wb, df_pop, on=['iso3', 'year'], how='outer')
    df_wb['year'] = df_wb['year'].astype(int)
    
    logger.info(f"Combined World Bank panel: {len(df_wb):,} records, {df_wb['iso3'].nunique()} countries.")
    return df_wb

def execute_pipeline():
    logger.info("=== Starting Data Cleaning and Harmonization Pipeline ===")
    xlsx_path = os.path.join(RAW_DIR, 'UNAIDS_HIV_estimates_1990_to_present.xlsx')
    
    # 1. Clean UNAIDS sheets
    df_estimates = clean_unaids_estimates(xlsx_path)
    df_cascade = clean_unaids_cascade(xlsx_path)
    
    # 2. Merge UNAIDS sheets
    df_unaids = pd.merge(df_estimates, df_cascade, on=['iso3', 'year'], how='left')
    logger.info(f"Merged UNAIDS dataset: {len(df_unaids):,} records.")
    
    # 3. Merge with World Bank
    df_wb = load_world_bank_data()
    df_master = pd.merge(df_unaids, df_wb, on=['iso3', 'year'], how='left')
    logger.info(f"Integrated Master dataset: {len(df_master):,} records.")
    
    # 4. Compute Derived Epidemiological Variables
    logger.info("Computing derived epidemiological indicators ...")
    # Treatment gap (%)
    df_master['treatment_gap_pct'] = 100.0 - df_master['art_coverage_pct']
    # Unreached PLHIV count
    df_master['unreached_plhiv'] = df_master['plhiv'] * (df_master['treatment_gap_pct'] / 100.0)
    # AIDS mortality rate per 100 PLHIV (%)
    df_master['mortality_rate_in_plhiv_pct'] = np.where(
        df_master['plhiv'] > 0,
        (df_master['aids_deaths'] / df_master['plhiv']) * 100.0,
        np.nan
    )
    # AIDS mortality rate per 100,000 population
    df_master['aids_mortality_rate_per100k_pop'] = np.where(
        df_master['population_total'] > 0,
        (df_master['aids_deaths'] / df_master['population_total']) * 100000.0,
        np.nan
    )
    # Incidence to Mortality Ratio
    df_master['incidence_to_mortality_ratio'] = np.where(
        df_master['aids_deaths'] > 0,
        df_master['new_infections'] / df_master['aids_deaths'],
        np.nan
    )
    
    # Lags for econometric modeling (within country, sorted by year)
    df_master = df_master.sort_values(['iso3', 'year']).reset_index(drop=True)
    df_master['art_coverage_lag1'] = df_master.groupby('iso3')['art_coverage_pct'].shift(1)
    df_master['art_coverage_lag2'] = df_master.groupby('iso3')['art_coverage_pct'].shift(2)
    df_master['aids_deaths_lag1'] = df_master.groupby('iso3')['aids_deaths'].shift(1)
    
    for lag in [1, 2]:
        previous_year = df_master.groupby('iso3')['year'].shift(lag)
        df_master.loc[df_master['year'].sub(previous_year).ne(lag), f'art_coverage_lag{lag}'] = np.nan

    # Regional Classification
    df_master['is_southeast_asia'] = df_master['iso3'].isin(SEA_COUNTRIES).astype(int)
    df_master['is_benchmark'] = df_master['iso3'].isin(BENCHMARKS).astype(int)
    
    # 5. Partition Datasets
    # Master Global Dataset (all entities)
    master_out = os.path.join(PROCESSED_DIR, 'hiv_epidemiology_master_1990_2025.csv')
    df_master.to_csv(master_out, index=False, lineterminator='\n')
    logger.info(f"Saved Global Master dataset -> {master_out} ({len(df_master):,} rows).")
    
    # Southeast Asia High-Resolution Panel (2010-2025)
    sea_panel = df_master[
        (df_master['iso3'].isin(SEA_COUNTRIES)) & 
        (df_master['year'] >= 2010)
    ].copy()
    sea_out = os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv')
    sea_panel.to_csv(sea_out, index=False, lineterminator='\n')
    logger.info(f"Saved Southeast Asia Panel -> {sea_out} ({len(sea_panel):,} rows).")
    
    # Southeast Asia Long-Term Panel (1990-2025)
    sea_long = df_master[df_master['iso3'].isin(SEA_COUNTRIES)].copy()
    sea_long_out = os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_longitudinal_1990_2025.csv')
    sea_long.to_csv(sea_long_out, index=False, lineterminator='\n')
    logger.info(f"Saved Southeast Asia Long-Term Panel -> {sea_long_out} ({len(sea_long):,} rows).")
    
    # Benchmarks (1990-2025)
    bench_panel = df_master[df_master['iso3'].isin(BENCHMARKS)].copy()
    bench_out = os.path.join(PROCESSED_DIR, 'regional_global_benchmarks_1990_2025.csv')
    bench_panel.to_csv(bench_out, index=False, lineterminator='\n')
    logger.info(f"Saved Benchmarks -> {bench_out} ({len(bench_panel):,} rows).")
    
    logger.info("=== Data Cleaning & Harmonization Completed Successfully ===")

if __name__ == '__main__':
    execute_pipeline()
