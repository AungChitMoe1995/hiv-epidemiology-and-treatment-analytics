# HIV trends and treatment access in Southeast Asia, 1990–2025

Dr. Aung Chit Moe, MBBS. Revised 15 October 2026.

## Research design and definitions

Retrospective portfolio analysis of a frozen public snapshot. Research questions: how do national HIV outcomes change, how do treatment indicators differ, and how sensitive are ART–mortality associations to specification? The revised protocol documents analysis decisions made during review and is not a prospectively registered protocol.

The workbook has 6,624 entity-years for 184 entities, including regional/global aggregates. It is not 184 independent countries. Southeast Asia includes all 11 countries: Brunei, Cambodia, Indonesia, Lao PDR, Malaysia, Myanmar, Philippines, Singapore, Thailand, Timor-Leste, and Viet Nam. Outcomes span 1990–2025. Treatment comparisons span 2010–2025 (176 country-years).

**Censoring:** `<100`, `<500`, `>95`, and `>98` are bounds, not exact values. Numeric point fields remain missing, while `_source`, `_qualifier`, and `_threshold` preserve the published information. `...` remains unavailable. No suppressed or censored value is replaced in the primary models. Lags and differences require consecutive calendar years. Complete-case availability excludes Lao PDR and Timor-Leste from the uncensored mortality models, and some early Philippine values are censored. Brunei and Singapore lack reportable ART data for 2025. The resulting sample is selective.

**Cascade denominators:** first 95 = diagnosed / all PLHIV; second 95 = on ART / diagnosed; third 95 = suppressed / on ART. Population equivalents of the joint 95–95–95 target are 95%, 90.25% on ART, and 85.7375% suppressed. Comparisons of all-PLHIV ART coverage against a flat 95% line are inappropriate. Use the direct all-PLHIV suppression estimate. Products of rounded or censored conditional stages need not reproduce it.

**Treatment gaps:** estimated PLHIV × (1−ART coverage/100). This is an approximate national planning quantity. Low/high gap scenarios combine marginal PLHIV and ART limits, which lack joint covariance and therefore are not joint confidence intervals. Missing bounds remain missing.

**Sources and dependence:** UNAIDS Spectrum uses programme ART counts and assumed survival to estimate mortality. Regressions on estimated outcomes partly reproduce these assumptions. WHO disseminates the same UNAIDS source family, so matching feeds verifies snapshot consistency, not independent accuracy. Both coverage and the mortality/PLHIV ratio share an estimated denominator. It is not a person-time mortality rate or cohort fatality risk. Prevalence, incidence, deaths and survival can change together, but the aggregate series cannot isolate those mechanisms.

**Economic comparison:** GDP is same-year PPP in constant 2021 international dollars, joined by ISO3 and year. No interpolation or latest-year carry-forward occurs. Cross-sections do not measure financing or programme quality. Crosswalk income labels are static context, not historical annual classifications or model strata.

## Calculated findings

- Myanmar: annual estimated AIDS deaths changed from 12,000 in 2010 to 4,400 in 2025 (-63.3%). ART coverage changed from 12% to 73%.
- Philippines: annual estimated new infections changed from 4,600 to 34,000 (+639.1%). These changes do not identify their causes.
- Indonesia and the Philippines account for approximately 58.8% of the calculated treatment gap among the 9 countries with available 2025 PLHIV and ART data. Brunei and Singapore are excluded from this denominator. Counts are approximate products of rounded estimates, not enumerated patients.
- Myanmar viral suppression among **all PLHIV** is the directly reported 70%, rather than the product of rounded conditional cascade stages.

## Model comparisons

| model_name                                  |   coefficient |   ci_lower_95 |   ci_upper_95 |   n_observations |   n_countries |
|:--------------------------------------------|--------------:|--------------:|--------------:|-----------------:|--------------:|
| Country FE: current ART                     |       -0.0409 |       -0.0649 |       -0.0170 |              109 |             7 |
| Country FE: lag 1                           |       -0.0400 |       -0.0614 |       -0.0186 |              103 |             7 |
| Country FE: lag 2                           |       -0.0380 |       -0.0579 |       -0.0181 |               97 |             7 |
| Country and year FE: lag 1                  |       -0.1032 |       -0.1378 |       -0.0686 |              103 |             7 |
| Country and year FE: lag 1 + GDP            |       -0.0934 |       -0.1239 |       -0.0629 |              103 |             7 |
| Country FE: common GDP sample               |       -0.0400 |       -0.0614 |       -0.0186 |              103 |             7 |
| Country and year FE: 2011-2019              |       -0.1123 |       -0.1292 |       -0.0954 |               61 |             7 |
| Country and year FE: omit Myanmar           |       -0.1229 |       -0.1842 |       -0.0617 |               88 |             6 |
| Population denominator: country/year FE     |       -0.5906 |       -1.2044 |        0.0233 |              103 |             7 |
| First differences with country/year effects |       -0.0615 |       -0.0866 |       -0.0364 |               96 |             7 |
| Threshold substitution sensitivity          |       -0.0878 |       -0.1306 |       -0.0450 |              135 |             9 |

Coefficients describe outcome-unit differences per one percentage point of ART coverage. Most outcomes are annual AIDS deaths / estimated PLHIV ×100. The population-denominator sensitivity instead uses deaths per 100,000 population. First differences use annual changes. R-squared in the CSV is overall dummy-variable OLS R-squared, not within R-squared. Each row carries its actual countries, period, sample size, design rank and inference degrees of freedom.

Country-only versus country/year models use the same complete lag-1 sample. The GDP common-sample comparison is explicit. Other sensitivities can use different samples. The boundary scenario substitutes disclosed censor thresholds and must not be interpreted as observed data.

Standard errors cluster by country. Full country/year dummy-variable rank enters the finite-sample covariance correction. Two-sided intervals and p-values use a t reference with G−1 degrees of freedom. Only seven countries contribute to the uncensored primary sample. Few-cluster inference remains approximate, and no significance claim establishes causation.

## Limitations

- UNAIDS mortality estimates incorporate ART inputs and assumed survival. Associations partly reflect model construction.
- Both ART coverage and deaths/PLHIV use estimated PLHIV denominators. The ratio is not a cohort fatality risk.
- Annual estimates are rounded and serially related. Regression intervals do not propagate UNAIDS estimation uncertainty.
- Year effects remove shared annual shocks only. Residual confounding, reverse causality and country-specific trends remain.
- Primary analysis excludes censored values. Boundary substitution is a sensitivity scenario, not an estimate of missing values.

The Myanmar 2021–2022 change cannot be attributed to conflict, COVID-19, ART interruption or programme responses using these data. Country archetypes and claims that policy outweighs GDP have been removed because those mechanisms were not measured. No deaths-averted estimate is inferred from the regression.

## Sources

- [UNAIDS data download](https://aidsinfo.unaids.org/dataset)
- [UNAIDS estimates with uncertainty bounds](https://www.unaids.org/en/resources/documents/2025/HIV_estimates_with_uncertainty_bounds_1990-present)
- [UNAIDS cascade denominators](https://www.unaids.org/en/resources/documents/2024/progress-towards-95-95-95)
- [Spectrum methods and assumptions, primary methods paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10769177/)
- [WHO HIV data](https://www.who.int/data/gho/data/themes/hiv-aids)
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators)
