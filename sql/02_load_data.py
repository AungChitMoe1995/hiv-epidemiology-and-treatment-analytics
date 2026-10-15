"""
sql/02_load_data.py
-------------------
Loads cleaned longitudinal surveillance datasets into SQLite database:
data/processed/hiv_surveillance.db.
"""

import os
import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('DBLoader')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'hiv_surveillance.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'sql', '01_create_schema.sql')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
METADATA_DIR = os.path.join(BASE_DIR, 'data', 'metadata')

def load_database():
    logger.info(f"Connecting to database at {DB_PATH} ...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Execute DDL Schema
    logger.info("Executing DDL schema ...")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    
    # 2. Populate dim_country
    logger.info("Loading dim_country ...")
    master_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'hiv_epidemiology_master_1990_2025.csv'))
    crosswalk_df = pd.read_csv(os.path.join(METADATA_DIR, 'country_crosswalk.csv'))
    
    # Get all unique entities from master
    entities = master_df[['iso3', 'country_name', 'is_southeast_asia', 'is_benchmark']].drop_duplicates().copy()
    dim_df = pd.merge(entities, crosswalk_df[['iso3', 'un_m49', 'region', 'income_group', 'analysis_role']], on='iso3', how='left')
    dim_df['region'] = dim_df['region'].fillna('Other')
    dim_df['income_group'] = dim_df['income_group'].fillna('Unclassified')
    dim_df['analysis_role'] = dim_df['analysis_role'].fillna('Global Country')
    
    dim_df.to_sql('dim_country', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(dim_df)} records into dim_country.")
    
    # 3. Populate fact_hiv_estimates
    logger.info("Loading fact_hiv_estimates ...")
    est_cols = [
        'iso3', 'year', 'plhiv', 'plhiv_low', 'plhiv_high',
        'adult_prevalence_pct', 'adult_prevalence_low', 'adult_prevalence_high',
        'aids_deaths', 'aids_deaths_low', 'aids_deaths_high',
        'new_infections', 'new_infections_low', 'new_infections_high',
        'incidence_rate_per1000', 'incidence_rate_low', 'incidence_rate_high'
    ]
    fact_est = master_df[est_cols].drop_duplicates(subset=['iso3', 'year'])
    fact_est.to_sql('fact_hiv_estimates', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(fact_est)} records into fact_hiv_estimates.")
    
    # 4. Populate fact_treatment_cascade
    logger.info("Loading fact_treatment_cascade ...")
    casc_cols = [
        'iso3', 'year', 'diagnosed_1st95_pct', 'diagnosed_1st95_low', 'diagnosed_1st95_high',
        'art_coverage_pct', 'art_coverage_low', 'art_coverage_high',
        'on_art_2nd95_pct', 'on_art_2nd95_low', 'on_art_2nd95_high',
        'virally_suppressed_3rd95_pct', 'virally_suppressed_3rd95_low', 'virally_suppressed_3rd95_high',
        'virally_suppressed_all_pct', 'treatment_gap_pct', 'unreached_plhiv'
    ]
    # Filter where treatment data exists (year >= 2010)
    fact_casc = master_df[master_df['year'] >= 2010][casc_cols].drop_duplicates(subset=['iso3', 'year'])
    fact_casc.to_sql('fact_treatment_cascade', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(fact_casc)} records into fact_treatment_cascade.")
    
    # 5. Populate fact_socioeconomic
    logger.info("Loading fact_socioeconomic ...")
    socio_cols = ['iso3', 'year', 'gdp_per_capita_usd', 'gdp_per_capita_ppp', 'population_total']
    fact_socio = master_df[socio_cols].drop_duplicates(subset=['iso3', 'year'])
    fact_socio.to_sql('fact_socioeconomic', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(fact_socio)} records into fact_socioeconomic.")
    
    # 6. Verify table counts
    logger.info("--- Database Verification Counts ---")
    for tbl in ['dim_country', 'fact_hiv_estimates', 'fact_treatment_cascade', 'fact_socioeconomic']:
        count = cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        logger.info(f"  Table {tbl}: {count:,} rows")
        
    view_count = cursor.execute("SELECT COUNT(*) FROM v_southeast_asia_surveillance").fetchone()[0]
    logger.info(f"  View v_southeast_asia_surveillance: {view_count:,} rows")
    
    conn.close()
    logger.info("Database loaded and committed successfully.")

if __name__ == '__main__':
    load_database()
