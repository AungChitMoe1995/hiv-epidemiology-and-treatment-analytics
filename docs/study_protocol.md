# Revised analysis protocol

## Research design and definitions

Retrospective portfolio analysis of a frozen public snapshot. Research questions: how do national HIV outcomes change, how do treatment indicators differ, and how sensitive are ART–mortality associations to specification? The revised protocol documents analysis decisions made during review and is not a prospectively registered protocol.

The workbook has 6,624 entity-years for 184 entities, including regional/global aggregates. It is not 184 independent countries. Southeast Asia includes all 11 countries: Brunei, Cambodia, Indonesia, Lao PDR, Malaysia, Myanmar, Philippines, Singapore, Thailand, Timor-Leste, and Viet Nam. Outcomes span 1990–2025. Treatment comparisons span 2010–2025 (176 country-years).

**Censoring:** `<100`, `<500`, `>95`, and `>98` are bounds, not exact values. Numeric point fields remain missing, while `_source`, `_qualifier`, and `_threshold` preserve the published information. `...` remains unavailable. No suppressed or censored value is replaced in the primary models. Lags and differences require consecutive calendar years. Complete-case availability excludes Lao PDR and Timor-Leste from the uncensored mortality models, and some early Philippine values are censored. Brunei and Singapore lack reportable ART data for 2025. The resulting sample is selective.

**Cascade denominators:** first 95 = diagnosed / all PLHIV; second 95 = on ART / diagnosed; third 95 = suppressed / on ART. Population equivalents of the joint 95–95–95 target are 95%, 90.25% on ART, and 85.7375% suppressed. Comparisons of all-PLHIV ART coverage against a flat 95% line are inappropriate. Use the direct all-PLHIV suppression estimate. Products of rounded or censored conditional stages need not reproduce it.

**Treatment gaps:** estimated PLHIV × (1−ART coverage/100). This is an approximate national planning quantity. Low/high gap scenarios combine marginal PLHIV and ART limits, which lack joint covariance and therefore are not joint confidence intervals. Missing bounds remain missing.

**Sources and dependence:** UNAIDS Spectrum uses programme ART counts and assumed survival to estimate mortality. Regressions on estimated outcomes partly reproduce these assumptions. WHO disseminates the same UNAIDS source family, so matching feeds verifies snapshot consistency, not independent accuracy. Both coverage and the mortality/PLHIV ratio share an estimated denominator. It is not a person-time mortality rate or cohort fatality risk. Prevalence, incidence, deaths and survival can change together, but the aggregate series cannot isolate those mechanisms.

**Economic comparison:** GDP is same-year PPP in constant 2021 international dollars, joined by ISO3 and year. No interpolation or latest-year carry-forward occurs. Cross-sections do not measure financing or programme quality. Crosswalk income labels are static context, not historical annual classifications or model strata.

## Planned comparisons in this revision

Country FE current/lag1/lag2; country and year FE; GDP adjustment with common-sample comparison; pre-2020; omit Myanmar; first differences; population-denominator outcome; threshold substitution; leave-one-country-out. All are exploratory. Published marginal uncertainty limits are displayed for descriptive outcomes, but regression inference does not propagate estimate uncertainty.

## Sources

- [UNAIDS data download](https://aidsinfo.unaids.org/dataset)
- [UNAIDS estimates with uncertainty bounds](https://www.unaids.org/en/resources/documents/2025/HIV_estimates_with_uncertainty_bounds_1990-present)
- [UNAIDS cascade denominators](https://www.unaids.org/en/resources/documents/2024/progress-towards-95-95-95)
- [Spectrum methods and assumptions, primary methods paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10769177/)
- [WHO HIV data](https://www.who.int/data/gho/data/themes/hiv-aids)
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators)
