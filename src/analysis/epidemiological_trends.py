"""
src/analysis/epidemiological_trends.py
--------------------------------------
Analyzes temporal trajectories (1990-2025) and Fast-Track changes (2010-2025)
in HIV incidence, prevalence, mortality, and ART coverage across Southeast Asia.

Outputs:
  - reports/analysis_tables/myanmar_trajectory_summary.csv
  - reports/analysis_tables/regional_trend_summary_2010_2025.csv
"""

import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('EpiTrends')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
OUTPUT_DIR = os.path.join(BASE_DIR, 'reports', 'analysis_tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_myanmar_trends():
    logger.info("Analyzing Myanmar longitudinal trajectory (1990-2025) ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_longitudinal_1990_2025.csv'))
    mmr = df[df['iso3'] == 'MMR'].sort_values('year').copy()
    
    summary_cols = [
        'year', 'plhiv', 'adult_prevalence_pct', 'new_infections', 
        'incidence_rate_per1000', 'aids_deaths', 'art_coverage_pct', 
        'treatment_gap_pct', 'unreached_plhiv', 'mortality_rate_in_plhiv_pct',
        'aids_mortality_rate_per100k_pop', 'gdp_per_capita_usd'
    ]
    mmr_summary = mmr[summary_cols].copy()
    
    # Calculate year-over-year changes post-2010
    mmr_summary['deaths_yoy_change'] = mmr_summary['aids_deaths'].diff()
    mmr_summary['art_yoy_gain_pp'] = mmr_summary['art_coverage_pct'].diff()
    
    out_path = os.path.join(OUTPUT_DIR, 'myanmar_trajectory_summary.csv')
    mmr_summary.to_csv(out_path, index=False)
    logger.info(f"Saved Myanmar trajectory summary -> {out_path}")
    return mmr_summary

def analyze_regional_changes():
    logger.info("Analyzing 2010 vs 2025 regional milestone changes ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    bench = pd.read_csv(os.path.join(PROCESSED_DIR, 'regional_global_benchmarks_1990_2025.csv'))
    bench = bench[bench['year'] >= 2010]
    
    combined = pd.concat([df, bench], ignore_index=True)
    
    d2010 = combined[combined['year'] == 2010].set_index('iso3')
    d2025 = combined[combined['year'] == 2025].set_index('iso3')
    
    records = []
    for iso3 in d2010.index.unique():
        if iso3 in d2025.index:
            r10 = d2010.loc[iso3]
            r25 = d2025.loc[iso3]
            
            cname = r10['country_name']
            deaths_10 = r10['aids_deaths']
            deaths_25 = r25['aids_deaths']
            inf_10 = r10['new_infections']
            inf_25 = r25['new_infections']
            art_10 = r10['art_coverage_pct']
            art_25 = r25['art_coverage_pct']
            plhiv_10 = r10['plhiv']
            plhiv_25 = r25['plhiv']
            
            pct_change_deaths = ((deaths_25 - deaths_10) / deaths_10 * 100.0) if pd.notna(deaths_10) and deaths_10 > 0 else np.nan
            pct_change_inf = ((inf_25 - inf_10) / inf_10 * 100.0) if pd.notna(inf_10) and inf_10 > 0 else np.nan
            art_gain_pp = (art_25 - art_10) if pd.notna(art_10) and pd.notna(art_25) else np.nan
            
            records.append({
                'iso3': iso3,
                'country_name': cname,
                'plhiv_2010': plhiv_10,
                'plhiv_2025': plhiv_25,
                'aids_deaths_2010': deaths_10,
                'aids_deaths_2025': deaths_25,
                'pct_change_deaths': round(pct_change_deaths, 1),
                'new_infections_2010': inf_10,
                'new_infections_2025': inf_25,
                'pct_change_new_infections': round(pct_change_inf, 1),
                'art_coverage_2010': art_10,
                'art_coverage_2025': art_25,
                'art_gain_percentage_points': round(art_gain_pp, 1)
            })
            
    summary_df = pd.DataFrame(records).sort_values('pct_change_deaths')
    out_path = os.path.join(OUTPUT_DIR, 'regional_trend_summary_2010_2025.csv')
    summary_df.to_csv(out_path, index=False)
    logger.info(f"Saved regional trend summary -> {out_path}")
    print(summary_df[['country_name', 'pct_change_deaths', 'pct_change_new_infections', 'art_gain_percentage_points']].to_string(index=False))
    return summary_df

if __name__ == '__main__':
    analyze_myanmar_trends()
    analyze_regional_changes()
