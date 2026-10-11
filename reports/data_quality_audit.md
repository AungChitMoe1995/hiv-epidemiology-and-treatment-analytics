# DATA QUALITY & CROSS-SOURCE REPRODUCIBILITY AUDIT REPORT

**Project:** HIV Epidemiological Transitions and Treatment Disparities in Southeast Asia (1990–2025)
**Audit Status:** ALL INTERNAL & CROSS-SOURCE CHECKS PASSED

## 1. Table Dimensions & Row Verification

| Table Name | Verified Row Count | Status |
| :--- | :---: | :--- |
| `dim_country` | 184 | Verified |
| `fact_hiv_estimates` | 6,624 | Verified |
| `fact_treatment_cascade` | 2,944 | Verified |
| `fact_socioeconomic` | 6,624 | Verified |

## 2. Relational & Key Integrity

- **Primary Key Duplicates on (iso3, year):** 0 detected (PASSED)
- **Foreign Key Orphans:** 0 detected (PASSED)

## 3. Epidemiological Range Checks

- **Invalid ART Coverage (< 0% or > 100%):** 0 (PASSED)
- **Invalid Prevalence (< 0% or > 100%):** 0 (PASSED)
- **Negative Epidemiological Counts:** 0 (PASSED)

## 4. Southeast Asia Focus Group Completeness (2010–2025)

- **Total Country-Year Observations:** 176
- **Missing AIDS Deaths:** 16 (All 16 observations from Brunei Darussalam due to official UNAIDS suppression)
- **Missing ART Coverage:** 17 (16 from Brunei Darussalam + 1 from Singapore 2010)
- **Missing GDP per Capita:** 0 (0.0%)

## 5. Python vs. SQLite Internal Numerical Reconciliation

- **Python Total Myanmar Deaths (2010–2025):** 110,400
- **SQL Total Myanmar Deaths (2010–2025):** 110,400
- **Internal Reconciliation Discrepancy:** 0.000000 (EXACT AGREEMENT)

## 6. Cross-Source Validation: WHO Global Health Observatory vs. UNAIDS 2026

All four raw WHO GHO OData CSV feeds in `data/raw/who_gho_*.csv` were programmatically joined by `(iso3, year)` against `hiv_epidemiology_master_1990_2025.csv` across **13,191 country-year-indicator observations** (exported to `reports/analysis_tables/who_unaids_cross_validation.csv`):

| WHO Raw File | WHO Indicator Code | UNAIDS Variable | WHO Raw Rows | Matched Country-Years | Exact 1:1 Matches | Match Rate | Max Abs Diff | Pearson $r$ |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `who_gho_art_coverage.csv` | `HIV_ARTCOVERAGE` | `art_coverage_pct` | 3,848 | 2,265 | 2,265 | **100.00%** | 0.0 | 1.000000 |
| `who_gho_hiv_deaths.csv` | `HIV_0000000006` | `aids_deaths` | 3,788 | 3,606 | 3,606 | **100.00%** | 0.0 | 1.000000 |
| `who_gho_new_infections.csv` | `HIV_0000000026` | `new_infections` | 3,792 | 3,610 | 3,610 | **100.00%** | 0.0 | 1.000000 |
| `who_gho_plhiv.csv` | `HIV_0000000001` | `plhiv` | 3,892 | 3,710 | 3,710 | **100.00%** | 0.0 | 1.000000 |

## 7. Bulk Archive Verification: `Estimates_2026_en.zip` vs. Master Dataset

- **Archive File:** `data/raw/Estimates_2026_en.zip` (22.11 MiB / 23.19 MB compressed)
- **Embedded CSV:** `Estimates_2026_en.csv` (331.91 MiB / 348.03 MB uncompressed; **2,197,290 rows**)

| Myanmar (MMR) 2025 Indicator | Master Dataset Value | Bulk CSV `Formatted` | Bulk CSV Unrounded `Data value` | Status |
| :--- | :---: | :---: | :---: | :--- |
| `aids_deaths` | 4,400.0 | 4,400.0 | 4,426.30 | **EXACT MATCH** |
| `plhiv` | 310,000.0 | 310,000.0 | 306,216.91 | **EXACT MATCH** |
| `new_infections` | 9,500.0 | 9,500.0 | 9,512.47 | **EXACT MATCH** |
| `art_coverage_pct` | 73.0 | 73.0 | 72.58 | **EXACT MATCH** |
