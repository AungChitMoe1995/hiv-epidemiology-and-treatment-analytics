# Data quality audit

58 checks passed. 6,624 entity-years across 184 entities (countries/territories and aggregates).

Southeast Asia: all 11 countries, 396 country-years, 176 rows from 2010 to 2025.

## Source consistency

9,814 uncensored country-year-indicator overlaps agree with the stored WHO feeds. This checks snapshot consistency only. WHO disseminates UNAIDS estimates and is not independent outcome validation. Unmatched rows and source hashes appear in the CSV and audit JSON. The bulk ZIP is an archived supplemental source, not a second independent validation dataset.

## Missing and censored values in 2025

| iso3   | country_name      | aids_deaths_source   | art_coverage_pct_source   | virally_suppressed_all_pct_source   |
|:-------|:------------------|:---------------------|:--------------------------|:------------------------------------|
| BRN    | Brunei Darussalam | ...                  | ...                       | ...                                 |
| IDN    | Indonesia         | 18 000               | 48                        | 45                                  |
| KHM    | Cambodia          | 1000                 | 95                        | 93                                  |
| LAO    | Lao PDR           | <500                 | 64                        | 63                                  |
| MMR    | Myanmar           | 4400                 | 73                        | 70                                  |
| MYS    | Malaysia          | 2000                 | 63                        | 55                                  |
| PHL    | Philippines       | 2700                 | 41                        | 40                                  |
| SGP    | Singapore         | <100                 | ...                       | ...                                 |
| THA    | Thailand          | 8400                 | 82                        | 81                                  |
| TLS    | Timor-Leste       | <100                 | 66                        | 46                                  |
| VNM    | Viet Nam          | 4100                 | 75                        | 72                                  |

Censored values retain source text, threshold, and qualifier. Numeric point fields are missing for censored/suppressed values. No zero, midpoint, or threshold is substituted in the primary analysis.

## Audit checks

- Unique entity-year keys
- Complete 1990-2025 grid
- 11 Southeast Asian country grids
- Censor handling: adult_prevalence_pct
- Censor handling: adult_prevalence_low
- Censor handling: adult_prevalence_high
- Censor handling: aids_deaths
- Censor handling: aids_deaths_low
- Censor handling: aids_deaths_high
- Censor handling: child_aids_deaths
- Censor handling: adult_aids_deaths
- Censor handling: child_plhiv
- Censor handling: women_plhiv
- Censor handling: adult_plhiv
- Censor handling: plhiv
- Censor handling: plhiv_low
- Censor handling: plhiv_high
- Censor handling: adult_incidence_per1000
- Censor handling: adult_incidence_low
- Censor handling: adult_incidence_high
- Censor handling: incidence_rate_per1000
- Censor handling: incidence_rate_low
- Censor handling: incidence_rate_high
- Censor handling: new_infections
- Censor handling: new_infections_low
- Censor handling: new_infections_high
- Censor handling: diagnosed_1st95_pct
- Censor handling: diagnosed_1st95_low
- Censor handling: diagnosed_1st95_high
- Censor handling: art_coverage_pct
- Censor handling: art_coverage_low
- Censor handling: art_coverage_high
- Censor handling: on_art_2nd95_pct
- Censor handling: on_art_2nd95_low
- Censor handling: on_art_2nd95_high
- Censor handling: virally_suppressed_all_pct
- Censor handling: virally_suppressed_all_low
- Censor handling: virally_suppressed_all_high
- Censor handling: virally_suppressed_3rd95_pct
- Censor handling: virally_suppressed_3rd95_low
- Censor handling: virally_suppressed_3rd95_high
- Percentage range: art_coverage_pct
- Percentage range: diagnosed_1st95_pct
- Percentage range: on_art_2nd95_pct
- Percentage range: virally_suppressed_all_pct
- Percentage range: virally_suppressed_3rd95_pct
- Nonnegative: plhiv
- Ordered marginal limits: plhiv
- Nonnegative: aids_deaths
- Ordered marginal limits: aids_deaths
- Nonnegative: new_infections
- Ordered marginal limits: new_infections
- SQLite integrity
- No foreign key violations
- SQL/CSV parity: aids_deaths
- SQL/CSV parity: art_coverage_pct
- SQL/CSV parity: unreached_plhiv
- Four WHO feeds reconciled
