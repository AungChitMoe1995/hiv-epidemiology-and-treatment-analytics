# HIV trends and treatment access in Southeast Asia (1990–2025)

**Dr. Aung Chit Moe, MBBS · Healthcare data analytics portfolio**

[Live Streamlit dashboard](https://hiv-epidemiology-and-treatment-analytics-acm.streamlit.app/)

A reproducible descriptive study of national HIV estimates and treatment access, with exploratory panel-model comparisons. The project uses the stored UNAIDS 2026 and World Bank WDI snapshot. It does not establish programme effects or individual clinical risks.

## What this project demonstrates

Python data cleaning that preserves censoring and suppression, a SQLite star schema and seven analytical queries, transparent denominator definitions, clustered panel models with sensitivity comparisons, six 300 dpi figures, an executed notebook, and an editable 22-slide PowerPoint briefing. The dashboard offers filters, downloads, model comparisons and fixed read-only SQL examples.

## Review corrections

The earlier version substituted censor thresholds as exact values, overstated causal interpretation, used observation-robust rather than country-clustered inference, compared all-PLHIV ART against an incorrect target, and multiplied rounded cascade indicators to estimate suppression. This revision corrects those choices throughout the outputs. Original conclusions and sample sizes must not be mixed with this revision.

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

## Coverage and source checks

All 11 Southeast Asian country grids are retained, including Brunei and Singapore even when estimates are unavailable. Global aggregates serve as benchmarks and never enter country regressions. The full workbook contains 184 entities, not 184 countries. The uncensored lag-1 primary sample has 103 observations across seven countries; the disclosed threshold-substitution scenario has 135 across nine.

The four stored WHO feeds agree on 9,814 uncensored overlapping country-year-indicator values. The previous 13,191 count included threshold substitutions. Agreement is source consistency, not independent validation. Raw-file hashes and checks appear in `reports/audit.json`.

## Reproduce the stored snapshot

Python 3.12. From the repository root:

```bash
python -m pip install -r requirements.txt
python src/run_pipeline.py
python src/research_io.py
python -m streamlit run dashboard/app.py
```

The pipeline reads stored inputs and rebuilds metadata, processed CSVs, SQLite, queries, audit, models, figures, reports and the notebook. It preserves the reviewed deck when its snapshot fingerprint matches. Add `--presentation` to rebuild the deck with the optional bundled authoring runtime. It does not silently download a newer estimate vintage. Acquisition is a separate explicit operation (`python src/acquisition/download_data.py`); changing inputs requires a full rebuild and review. The optional presentation builder requires the bundled Artifact Tool JavaScript runtime. See `docs/presentation_build.md`.

CI installs the pinned requirements, checks artifact hashes and runs the fail-fast data audit and existing regression checks. The snapshot manifest guards against mixing stale reports with changed inputs. CSV outputs use LF endings for portable hashes.

## Outputs

- `reports/research_report.md`: full interpretation and limitations
- `reports/results.json`: machine-readable model results and sample definitions
- `reports/data_quality_audit.md`, `reports/audit.json`: integrity checks and source fingerprints
- `reports/analysis_tables/`: cascade, gaps, trends, models and leave-one-country-out results
- `reports/sql_results/`: seven database query outputs
- `data/processed/`: source-labelled CSVs and `hiv_surveillance.db`
- `figures/`: six figures with units, censoring notes and uncertainty qualifications
- `notebooks/hiv_epidemiology_research.ipynb`: executed analytical walkthrough
- `docs/presentation/hiv_epidemiology_research_briefing.pptx`: 22-slide briefing

## Limitations

- UNAIDS mortality estimates incorporate ART inputs and assumed survival. Associations partly reflect model construction.
- Both ART coverage and deaths/PLHIV use estimated PLHIV denominators. The ratio is not a cohort fatality risk.
- Annual estimates are rounded and serially related. Regression intervals do not propagate UNAIDS estimation uncertainty.
- Year effects remove shared annual shocks only. Residual confounding, reverse causality and country-specific trends remain.
- Primary analysis excludes censored values. Boundary substitution is a sensitivity scenario, not an estimate of missing values.

See the [research report](reports/research_report.md) for denominator definitions, selective missingness and source dependence.

## Sources

- [UNAIDS data download](https://aidsinfo.unaids.org/dataset)
- [UNAIDS estimates with uncertainty bounds](https://www.unaids.org/en/resources/documents/2025/HIV_estimates_with_uncertainty_bounds_1990-present)
- [UNAIDS cascade denominators](https://www.unaids.org/en/resources/documents/2024/progress-towards-95-95-95)
- [Spectrum methods and assumptions, primary methods paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10769177/)
- [WHO HIV data](https://www.who.int/data/gho/data/themes/hiv-aids)
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators)

## AI-assisted development

The author used AI assistance for code and presentation revision. Calculations and source-dependent limitations are documented for review. Authorship does not imply institutional endorsement.

MIT license applies to project code. Source datasets remain subject to their providers’ terms.
