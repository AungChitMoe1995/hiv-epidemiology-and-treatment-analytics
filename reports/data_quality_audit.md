# DATA QUALITY & REPRODUCIBILITY AUDIT REPORT

**Project:** HIV Epidemiological Trends and Treatment Disparities
**Audit Status:** ALL CHECKS PASSED

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

## 5. Python vs. SQL Numerical Reconciliation

- **Python Total Myanmar Deaths (2010–2025):** 110,400
- **SQL Total Myanmar Deaths (2010–2025):** 110,400
- **Reconciliation Discrepancy:** 0.000000 (EXACT AGREEMENT)
