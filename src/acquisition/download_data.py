"""
src/acquisition/download_data.py
---------------------------------
Automated, reproducible data acquisition pipeline for official HIV surveillance
and socioeconomic datasets from UNAIDS, WHO GHO, and the World Bank.

Inputs:
  - Official HTTPS endpoints for UNAIDS, WHO OData API, and World Bank WDI API.
Outputs:
  - data/raw/UNAIDS_HIV_estimates_1990_to_present.xlsx
  - data/raw/Estimates_2026_en.zip
  - data/raw/wb_*.csv (GDP, Population)
  - data/raw/who_gho_*.csv (Deaths, ART, New Infections, PLHIV)
"""

import os
import sys
import logging
import requests
import zipfile

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('DataAcquisition')

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw'))
os.makedirs(RAW_DIR, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HealthCareAnalytics/1.0'}

# 1. Endpoints Configuration
UNAIDS_XLSX_URL = 'https://www.unaids.org/sites/default/files/2026-07/HIV_estimates_from_1990-to-present_1.xlsx'
UNAIDS_ZIP_URL = 'https://aidsinfo.unaids.org/public/documents/Estimates_2026_en.zip'

WB_INDICATORS = {
    'NY.GDP.PCAP.CD': 'wb_gdp_per_capita_current_usd.csv',
    'NY.GDP.PCAP.PP.KD': 'wb_gdp_per_capita_ppp_constant2021.csv',
    'SP.POP.TOTL': 'wb_population_total.csv'
}

WHO_INDICATORS = {
    'HIV_0000000006': 'who_gho_hiv_deaths.csv',
    'HIV_ARTCOVERAGE': 'who_gho_art_coverage.csv',
    'HIV_0000000026': 'who_gho_new_infections.csv',
    'HIV_0000000001': 'who_gho_plhiv.csv'
}

def download_file(url: str, dest_path: str, timeout: int = 60) -> bool:
    """Download a file with streaming and error handling."""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        logger.info(f"File already exists: {dest_path} ({os.path.getsize(dest_path)/(1024*1024):.2f} MB). Skipping download.")
        return True
    logger.info(f"Downloading {url} -> {dest_path} ...")
    try:
        with requests.get(url, headers=HEADERS, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        logger.info(f"Successfully saved {dest_path} ({size_mb:.2f} MB)")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False

def fetch_wb_indicator(code: str, filename: str) -> bool:
    """Fetch all records for a World Bank indicator."""
    dest_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        logger.info(f"World Bank file exists: {dest_path}. Skipping.")
        return True
    url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000&date=1990:2025"
    logger.info(f"Querying World Bank API for indicator {code} ...")
    try:
        import pandas as pd
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        if len(data) > 1 and data[1]:
            rows = []
            for rec in data[1]:
                rows.append({
                    'country_id': rec.get('countryiso3code'),
                    'country_name': rec.get('country', {}).get('value'),
                    'year': rec.get('date'),
                    'value': rec.get('value')
                })
            df = pd.DataFrame(rows)
            df.to_csv(dest_path, index=False)
            logger.info(f"Saved {dest_path} ({len(df)} records).")
            return True
        else:
            logger.warning(f"Empty data received for {code}")
            return False
    except Exception as e:
        logger.error(f"Error fetching World Bank indicator {code}: {e}")
        return False

def fetch_who_indicator(code: str, filename: str) -> bool:
    """Fetch WHO GHO indicator via OData REST API."""
    dest_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        logger.info(f"WHO GHO file exists: {dest_path}. Skipping.")
        return True
    url = f"https://ghoapi.azureedge.net/api/{code}"
    logger.info(f"Querying WHO GHO API for indicator {code} ...")
    try:
        import pandas as pd
        r = requests.get(url, headers=HEADERS, timeout=45)
        r.raise_for_status()
        data = r.json().get('value', [])
        if data:
            df = pd.DataFrame(data)
            keep_cols = [c for c in ['IndicatorCode', 'SpatialDimType', 'SpatialDim', 'TimeDim', 'Dim1', 'Dim2', 'Value', 'NumericValue', 'Low', 'High', 'Comments'] if c in df.columns]
            df[keep_cols].to_csv(dest_path, index=False)
            logger.info(f"Saved {dest_path} ({len(df)} records).")
            return True
        else:
            logger.warning(f"No records returned for WHO {code}")
            return False
    except Exception as e:
        logger.error(f"Error fetching WHO indicator {code}: {e}")
        return False

def run_acquisition():
    logger.info("=== Starting Data Acquisition Pipeline ===")
    
    # 1. UNAIDS Master Files
    download_file(UNAIDS_XLSX_URL, os.path.join(RAW_DIR, 'UNAIDS_HIV_estimates_1990_to_present.xlsx'))
    download_file(UNAIDS_ZIP_URL, os.path.join(RAW_DIR, 'Estimates_2026_en.zip'))

    # 2. World Bank Socioeconomic Indicators
    for code, fname in WB_INDICATORS.items():
        fetch_wb_indicator(code, fname)

    # 3. WHO GHO Surveillance Indicators
    for code, fname in WHO_INDICATORS.items():
        fetch_who_indicator(code, fname)

    logger.info("=== Data Acquisition Pipeline Completed Successfully ===")

if __name__ == '__main__':
    run_acquisition()
