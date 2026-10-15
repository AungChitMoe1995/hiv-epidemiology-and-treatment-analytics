import os
import pandas as pd

METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'metadata'))
os.makedirs(METADATA_DIR, exist_ok=True)

# 1. Source Inventory
source_inv = [
    {
        'source_name': 'UNAIDS',
        'resource_title': 'UNAIDS 2026 Epidemiological Estimates Database',
        'file_name': 'Estimates_2026_en.csv',
        'file_format': 'CSV',
        'source_url': 'https://aidsinfo.unaids.org/public/documents/Estimates_2026_en.zip',
        'time_coverage': '1990-2025',
        'geo_coverage': 'Global (218 countries/territories + 8 regional aggregates)',
        'data_type': 'Compartmental epidemiological model estimates (Spectrum/EPP)',
        'citation': 'UNAIDS (2026). Report on the Global AIDS Epidemic: Epidemiological Estimates.'
    },
    {
        'source_name': 'UNAIDS',
        'resource_title': 'HIV Estimates with Uncertainty Bounds 1990 to Present',
        'file_name': 'UNAIDS_HIV_estimates_1990_to_present.xlsx',
        'file_format': 'XLSX',
        'source_url': 'https://www.unaids.org/sites/default/files/2026-07/HIV_estimates_from_1990-to-present_1.xlsx',
        'time_coverage': '1990-2025 (Estimates); 2010-2025 (95-95-95 Cascade)',
        'geo_coverage': '184 entities including countries/territories and aggregates',
        'data_type': 'Modeled estimates with 95% uncertainty bounds',
        'citation': 'UNAIDS (2026). HIV Estimates with Uncertainty Bounds 1990-present.'
    },
    {
        'source_name': 'WHO GHO',
        'resource_title': 'Global Health Observatory HIV Data Portal',
        'file_name': 'who_gho_*.csv (deaths, art_coverage, new_infections, plhiv)',
        'file_format': 'CSV (REST OData API)',
        'source_url': 'https://ghoapi.azureedge.net/api/',
        'time_coverage': '2000-2025',
        'geo_coverage': '152 WHO Member States',
        'data_type': 'Syndicated UNAIDS Spectrum estimates with bounds',
        'citation': 'World Health Organization (2026). Global Health Observatory data repository.'
    },
    {
        'source_name': 'World Bank',
        'resource_title': 'World Development Indicators (WDI)',
        'file_name': 'wb_*.csv (gdp_current, gdp_ppp, population)',
        'file_format': 'CSV (REST API)',
        'source_url': 'https://api.worldbank.org/v2/',
        'time_coverage': '1990-2025',
        'geo_coverage': '261 countries and economies',
        'data_type': 'Macroeconomic and demographic statistical time-series',
        'citation': 'World Bank (2026). World Development Indicators database.'
    }
]
pd.DataFrame(source_inv).to_csv(os.path.join(METADATA_DIR, 'source_inventory.csv'), index=False,lineterminator='\n')

# 2. Data Dictionary
data_dict = [
    {'variable_name': 'iso3', 'entity_type': 'Identifier', 'data_type': 'VARCHAR(3)', 'unit': 'ISO-3166-1 alpha-3', 'definition': 'Standard 3-letter country code', 'source': 'ISO/UNAIDS'},
    {'variable_name': 'country_name', 'entity_type': 'Identifier', 'data_type': 'VARCHAR(100)', 'unit': 'Text', 'definition': 'Official country or territory name', 'source': 'UNAIDS'},
    {'variable_name': 'year', 'entity_type': 'Temporal', 'data_type': 'INTEGER', 'unit': 'Calendar Year', 'definition': 'Observation year (1990-2025)', 'source': 'UNAIDS/WB'},
    {'variable_name': 'plhiv', 'entity_type': 'Outcome', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Estimated total people of all ages living with HIV', 'source': 'UNAIDS'},
    {'variable_name': 'plhiv_low', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Lower bound of 95% uncertainty interval for PLHIV', 'source': 'UNAIDS'},
    {'variable_name': 'plhiv_high', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Upper bound of 95% uncertainty interval for PLHIV', 'source': 'UNAIDS'},
    {'variable_name': 'adult_prevalence_pct', 'entity_type': 'Outcome', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Estimated HIV prevalence among adults aged 15-49', 'source': 'UNAIDS'},
    {'variable_name': 'adult_prevalence_low', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Lower bound of 95% uncertainty interval for adult prevalence', 'source': 'UNAIDS'},
    {'variable_name': 'adult_prevalence_high', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Upper bound of 95% uncertainty interval for adult prevalence', 'source': 'UNAIDS'},
    {'variable_name': 'aids_deaths', 'entity_type': 'Primary Outcome', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Estimated annual deaths directly attributed to AIDS', 'source': 'UNAIDS'},
    {'variable_name': 'aids_deaths_low', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Lower bound of 95% uncertainty interval for AIDS deaths', 'source': 'UNAIDS'},
    {'variable_name': 'aids_deaths_high', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Upper bound of 95% uncertainty interval for AIDS deaths', 'source': 'UNAIDS'},
    {'variable_name': 'new_infections', 'entity_type': 'Secondary Outcome', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Estimated annual newly acquired HIV infections (all ages)', 'source': 'UNAIDS'},
    {'variable_name': 'new_infections_low', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Lower bound of 95% uncertainty interval for new infections', 'source': 'UNAIDS'},
    {'variable_name': 'new_infections_high', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Upper bound of 95% uncertainty interval for new infections', 'source': 'UNAIDS'},
    {'variable_name': 'incidence_rate_per1000', 'entity_type': 'Outcome', 'data_type': 'DOUBLE', 'unit': 'Rate per 1000', 'definition': 'HIV incidence per 1000 uninfected population', 'source': 'UNAIDS'},
    {'variable_name': 'art_coverage_pct', 'entity_type': 'Primary Exposure', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Percentage of people living with HIV on antiretroviral therapy', 'source': 'UNAIDS'},
    {'variable_name': 'art_coverage_low', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Lower bound of 95% uncertainty interval for ART coverage', 'source': 'UNAIDS'},
    {'variable_name': 'art_coverage_high', 'entity_type': 'Uncertainty', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Upper bound of 95% uncertainty interval for ART coverage', 'source': 'UNAIDS'},
    {'variable_name': 'diagnosed_1st95_pct', 'entity_type': 'Cascade Metric', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Percentage of PLHIV who know their status (1st 95 target)', 'source': 'UNAIDS'},
    {'variable_name': 'on_art_2nd95_pct', 'entity_type': 'Cascade Metric', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Percentage of diagnosed PLHIV on ART (2nd 95 target)', 'source': 'UNAIDS'},
    {'variable_name': 'virally_suppressed_3rd95_pct', 'entity_type': 'Cascade Metric', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': 'Percentage of people on ART with suppressed viral load (3rd 95 target)', 'source': 'UNAIDS'},
    {'variable_name': 'treatment_gap_pct', 'entity_type': 'Derived Exposure', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': '100% - art_coverage_pct', 'source': 'Derived'},
    {'variable_name': 'unreached_plhiv', 'entity_type': 'Derived Exposure', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'plhiv * (1 - art_coverage_pct / 100)', 'source': 'Derived'},
    {'variable_name': 'mortality_rate_in_plhiv_pct', 'entity_type': 'Derived Outcome', 'data_type': 'DOUBLE', 'unit': 'Percentage (%)', 'definition': '(aids_deaths / plhiv) * 100', 'source': 'Derived'},
    {'variable_name': 'aids_mortality_rate_per100k_pop', 'entity_type': 'Derived Outcome', 'data_type': 'DOUBLE', 'unit': 'Rate per 100,000', 'definition': '(aids_deaths / population_total) * 100,000', 'source': 'Derived'},
    {'variable_name': 'gdp_per_capita_usd', 'entity_type': 'Covariate', 'data_type': 'DOUBLE', 'unit': 'Current US$', 'definition': 'Gross Domestic Product per capita in current US$', 'source': 'World Bank (NY.GDP.PCAP.CD)'},
    {'variable_name': 'gdp_per_capita_ppp', 'entity_type': 'Covariate', 'data_type': 'DOUBLE', 'unit': 'Constant 2021 Int$', 'definition': 'GDP per capita PPP in constant 2021 international $', 'source': 'World Bank (NY.GDP.PCAP.PP.KD)'},
    {'variable_name': 'population_total', 'entity_type': 'Demographic', 'data_type': 'DOUBLE', 'unit': 'Count', 'definition': 'Total midyear national population', 'source': 'World Bank (SP.POP.TOTL)'}
]
pd.DataFrame(data_dict).to_csv(os.path.join(METADATA_DIR, 'data_dictionary.csv'), index=False,lineterminator='\n')

# 3. Country Crosswalk
country_crosswalk = [
    {'iso3': 'MMR', 'country_name': 'Myanmar', 'un_m49': '104', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Core Target'},
    {'iso3': 'THA', 'country_name': 'Thailand', 'un_m49': '764', 'region': 'Southeast Asia', 'income_group': 'Upper middle income', 'analysis_role': 'Regional Leader'},
    {'iso3': 'VNM', 'country_name': 'Viet Nam', 'un_m49': '704', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Harm Reduction Success'},
    {'iso3': 'KHM', 'country_name': 'Cambodia', 'un_m49': '116', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Cascade Benchmark (95% ART)'},
    {'iso3': 'IDN', 'country_name': 'Indonesia', 'un_m49': '360', 'region': 'Southeast Asia', 'income_group': 'Upper middle income', 'analysis_role': 'High Burden / Treatment Gap'},
    {'iso3': 'MYS', 'country_name': 'Malaysia', 'un_m49': '458', 'region': 'Southeast Asia', 'income_group': 'Upper middle income', 'analysis_role': 'Concentrated Epidemic'},
    {'iso3': 'PHL', 'country_name': 'Philippines', 'un_m49': '608', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Counter-Epidemic Outbreak'},
    {'iso3': 'LAO', 'country_name': 'Lao PDR', 'un_m49': '418', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Low-Burden Comparator'},
    {'iso3': 'TLS', 'country_name': 'Timor-Leste', 'un_m49': '626', 'region': 'Southeast Asia', 'income_group': 'Lower middle income', 'analysis_role': 'Small Island Comparator'},
    {'iso3': 'SGP', 'country_name': 'Singapore', 'un_m49': '702', 'region': 'Southeast Asia', 'income_group': 'High income', 'analysis_role': 'High-Income Benchmark'},
    {'iso3': 'BRN', 'country_name': 'Brunei Darussalam', 'un_m49': '096', 'region': 'Southeast Asia', 'income_group': 'High income', 'analysis_role': 'Suppressed (Descriptive only)'},
    {'iso3': 'UNAAP', 'country_name': 'Asia and the Pacific', 'un_m49': 'N/A', 'region': 'Regional Aggregate', 'income_group': 'Aggregate', 'analysis_role': 'Regional Benchmark'},
    {'iso3': '03M49WLD', 'country_name': 'Global Total', 'un_m49': '001', 'region': 'Global Aggregate', 'income_group': 'Aggregate', 'analysis_role': 'Global Benchmark'}
]
pd.DataFrame(country_crosswalk).to_csv(os.path.join(METADATA_DIR, 'country_crosswalk.csv'), index=False,lineterminator='\n')

print("Generated metadata files successfully in data/metadata/.")

# Clarify derived fields and preserve censoring semantics in the generated dictionary.
dictionary_path=os.path.join(METADATA_DIR,'data_dictionary.csv')
dictionary=pd.read_csv(dictionary_path)
dictionary.loc[dictionary.variable_name.eq('mortality_rate_in_plhiv_pct'),'definition']='Annual estimated AIDS deaths / estimated PLHIV *100. Descriptive ratio, not cohort fatality risk.'
extra=pd.DataFrame([dict(variable_name='*_source',definition='Original UNAIDS text, including <, > and suppression markers'),dict(variable_name='*_qualifier',definition='= exact rounded estimate; < or > censored; missing unavailable'),dict(variable_name='*_threshold',definition='Published censoring boundary only. Numeric point estimate remains missing.'),dict(variable_name='virally_suppressed_all_pct',definition='Direct UNAIDS estimate: suppressed viral load among all PLHIV, not a product of rounded conditional stages')])
pd.concat([dictionary,extra],ignore_index=True).to_csv(dictionary_path,index=False,lineterminator='\n')
p=os.path.join(METADATA_DIR,'country_crosswalk.csv');c=pd.read_csv(p)
c.loc[c.iso3.isin(['MMR','THA','VNM','KHM','IDN','MYS','PHL','LAO','TLS','SGP','BRN']),'analysis_role']='Southeast Asia focus country'
c.to_csv(p,index=False,lineterminator='\n')
