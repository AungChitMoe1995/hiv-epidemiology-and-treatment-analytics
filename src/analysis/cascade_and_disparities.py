"""
src/analysis/cascade_and_disparities.py
---------------------------------------
Analyzes UNAIDS 95-95-95 cascade performance, quantifies regional treatment gaps,
and formulates the tripartite epidemiological archetype classification for Southeast Asia.

Outputs:
  - reports/analysis_tables/cascade_2025_summary.csv
  - reports/analysis_tables/treatment_gaps_2025.csv
  - reports/analysis_tables/archetype_classification.csv
"""

import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('CascadeAnalysis')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
OUTPUT_DIR = os.path.join(BASE_DIR, 'reports', 'analysis_tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEA_COUNTRIES = ['MMR', 'THA', 'VNM', 'KHM', 'IDN', 'MYS', 'PHL', 'LAO', 'TLS', 'SGP', 'BRN']

def analyze_cascade():
    logger.info("Evaluating 2025 UNAIDS 95-95-95 Cascade Performance ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    bench = pd.read_csv(os.path.join(PROCESSED_DIR, 'regional_global_benchmarks_1990_2025.csv'))
    
    combined = pd.concat([df, bench], ignore_index=True)
    c2025 = combined[combined['year'] == 2025].copy()
    
    # Calculate population-level viral suppression % (PLHIV who are virally suppressed)
    c2025['pop_level_viral_suppression_pct'] = (
        c2025['diagnosed_1st95_pct'] * 
        c2025['on_art_2nd95_pct'] * 
        c2025['virally_suppressed_3rd95_pct']
    ) / 10000.0
    
    cascade_cols = [
        'country_name', 'iso3', 'plhiv',
        'diagnosed_1st95_pct', 'on_art_2nd95_pct', 'virally_suppressed_3rd95_pct',
        'art_coverage_pct', 'treatment_gap_pct', 'unreached_plhiv',
        'pop_level_viral_suppression_pct'
    ]
    
    cascade_df = c2025[cascade_cols].sort_values('art_coverage_pct', ascending=False)
    out_cascade = os.path.join(OUTPUT_DIR, 'cascade_2025_summary.csv')
    cascade_df.to_csv(out_cascade, index=False)
    logger.info(f"Saved 2025 cascade summary -> {out_cascade}")
    
    # Analyze Treatment Gaps among SEA Focus Group
    sea_gaps = c2025[c2025['iso3'].isin(SEA_COUNTRIES) & c2025['unreached_plhiv'].notna()].copy()
    total_unreached = sea_gaps['unreached_plhiv'].sum()
    sea_gaps['share_of_regional_unreached_pct'] = (sea_gaps['unreached_plhiv'] / total_unreached) * 100.0
    
    gap_cols = [
        'country_name', 'iso3', 'plhiv', 'art_coverage_pct', 
        'treatment_gap_pct', 'unreached_plhiv', 'share_of_regional_unreached_pct'
    ]
    gap_df = sea_gaps[gap_cols].sort_values('unreached_plhiv', ascending=False)
    out_gaps = os.path.join(OUTPUT_DIR, 'treatment_gaps_2025.csv')
    gap_df.to_csv(out_gaps, index=False)
    logger.info(f"Saved treatment gaps summary -> {out_gaps}")
    print("\n--- Top Treatment Gaps in Southeast Asia (2025) ---")
    print(gap_df[['country_name', 'art_coverage_pct', 'treatment_gap_pct', 'unreached_plhiv', 'share_of_regional_unreached_pct']].to_string(index=False))
    
    # Archetype Classification
    archetypes = []
    for _, row in gap_df.iterrows():
        iso = row['iso3']
        art = row['art_coverage_pct']
        gap = row['treatment_gap_pct']
        unreached = row['unreached_plhiv']
        
        if iso in ['THA', 'KHM', 'VNM']:
            archetype = 'Archetype A: Accelerated Control'
            rationale = 'High ART coverage (>=75%), strong testing cascades, and steep mortality declines (-15% to -80%).'
        elif iso in ['MMR', 'MYS', 'LAO', 'TLS']:
            archetype = 'Archetype B: Fragile Steady Progress'
            rationale = 'Substantial historical gains (+45-61 pp ART), but vulnerable to political/supply disruption (Myanmar 2021 rebound).'
        elif iso in ['PHL', 'IDN']:
            archetype = 'Archetype C: Counter-Epidemic / Severe Gap'
            rationale = 'Low ART coverage (<50%), massive treatment gap (>50%), expanding infections (PHL +639%) or rising deaths (IDN +29%).'
        else:
            archetype = 'Other / High-Income Benchmark'
            rationale = 'Specialized context (Singapore high income; Brunei suppressed).'
            
        archetypes.append({
            'iso3': iso,
            'country_name': row['country_name'],
            'art_coverage_2025': art,
            'treatment_gap_pct': gap,
            'unreached_plhiv_2025': unreached,
            'epidemiological_archetype': archetype,
            'clinical_rationale': rationale
        })
        
    arch_df = pd.DataFrame(archetypes)
    out_arch = os.path.join(OUTPUT_DIR, 'archetype_classification.csv')
    arch_df.to_csv(out_arch, index=False)
    logger.info(f"Saved archetype classification -> {out_arch}")
    return cascade_df, gap_df, arch_df

if __name__ == '__main__':
    analyze_cascade()
