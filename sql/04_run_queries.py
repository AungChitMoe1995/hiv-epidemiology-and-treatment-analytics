"""
sql/04_run_queries.py
---------------------
Executes production SQL analytical queries against data/processed/hiv_surveillance.db,
displays formatted results, and exports query results to reports/sql_results/.
"""

import os
import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('SQLExecutor')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'hiv_surveillance.db')
SQL_FILE = os.path.join(BASE_DIR, 'sql', '03_analytical_queries.sql')
RESULTS_DIR = os.path.join(BASE_DIR, 'reports', 'sql_results')
os.makedirs(RESULTS_DIR, exist_ok=True)

def parse_queries(sql_content):
    """Splits SQL file into individual named queries."""
    queries = []
    current_name = None
    current_sql = []
    
    for line in sql_content.splitlines():
        if line.strip().startswith('-- QUERY'):
            if current_name and current_sql:
                queries.append((current_name, '\n'.join(current_sql).strip()))
                current_sql = []
            current_name = line.strip().replace('-- ', '')
        elif current_name:
            if not line.strip().startswith('--'):
                current_sql.append(line)
                
    if current_name and current_sql:
        queries.append((current_name, '\n'.join(current_sql).strip()))
        
    return queries

def execute_all_queries():
    logger.info(f"Opening database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    queries = parse_queries(content)
    logger.info(f"Found {len(queries)} analytical queries to execute.")
    
    for i, (name, sql) in enumerate(queries, 1):
        clean_name = name.split(':')[0].strip().replace(' ', '_').lower()
        logger.info(f"\n=======================================================")
        logger.info(f"Executing [{i}/{len(queries)}] {name}")
        logger.info(f"=======================================================")
        
        try:
            df = pd.read_sql_query(sql, conn)
            logger.info(f"Result rows: {len(df)}")
            print(df.head(10).to_string(index=False))
            if len(df) > 10:
                print(f"... [{len(df) - 10} more rows]")
                
            out_csv = os.path.join(RESULTS_DIR, f"{clean_name}.csv")
            df.to_csv(out_csv, index=False,lineterminator='\n')
            logger.info(f"Saved results -> {out_csv}")
        except Exception as e:
            raise RuntimeError(f"Error executing {name}") from e
            
    conn.close()
    logger.info("All analytical SQL queries executed successfully.")

if __name__ == '__main__':
    execute_all_queries()
