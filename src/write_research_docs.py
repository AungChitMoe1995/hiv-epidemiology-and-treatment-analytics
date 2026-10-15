"""Generate narrative outputs from the same calculated model and descriptive tables."""
from pathlib import Path
import pandas as pd
from research_io import ROOT,load_results
SOURCES="""- [UNAIDS data download](https://aidsinfo.unaids.org/dataset)
- [UNAIDS estimates with uncertainty bounds](https://www.unaids.org/en/resources/documents/2025/HIV_estimates_with_uncertainty_bounds_1990-present)
- [UNAIDS cascade denominators](https://www.unaids.org/en/resources/documents/2024/progress-towards-95-95-95)
- [Spectrum methods and assumptions, primary methods paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10769177/)
- [WHO HIV data](https://www.who.int/data/gho/data/themes/hiv-aids)
- [World Bank WDI](https://databank.worldbank.org/source/world-development-indicators)
"""
def write_docs():
    r=load_results();models=pd.DataFrame(r['models'])
    trend=pd.read_csv(ROOT/'reports/analysis_tables/regional_trend_summary_2010_2025.csv')
    gaps=pd.read_csv(ROOT/'reports/analysis_tables/treatment_gaps_2025.csv')
    c=pd.read_csv(ROOT/'reports/analysis_tables/cascade_2025_summary.csv')
    m=trend[trend.iso3.eq('MMR')].iloc[0];p=trend[trend.iso3.eq('PHL')].iloc[0]
    shares=gaps[gaps.iso3.isin(['IDN','PHL'])].unreached_plhiv.sum()/gaps.unreached_plhiv.sum()*100
    shown=models[['model_name','coefficient','ci_lower_95','ci_upper_95','n_observations','n_countries']]
    results=f"""## Calculated findings

- Myanmar: annual estimated AIDS deaths changed from {m.aids_deaths_2010:,.0f} in 2010 to {m.aids_deaths_2025:,.0f} in 2025 ({m.pct_change_deaths:+.1f}%). ART coverage changed from {m.art_coverage_2010:.0f}% to {m.art_coverage_2025:.0f}%.
- Philippines: annual estimated new infections changed from {p.new_infections_2010:,.0f} to {p.new_infections_2025:,.0f} ({p.pct_change_new_infections:+.1f}%). These changes do not identify their causes.
- Indonesia and the Philippines account for approximately {shares:.1f}% of the calculated treatment gap among the {len(gaps)} countries with available 2025 PLHIV and ART data. Brunei and Singapore are excluded from this denominator. Counts are approximate products of rounded estimates, not enumerated patients.
- Myanmar viral suppression among **all PLHIV** is the directly reported {c[c.iso3.eq('MMR')].virally_suppressed_all_pct.iloc[0]:.0f}%, rather than the product of rounded conditional cascade stages.

## Model comparisons

{shown.to_markdown(index=False,floatfmt='.4f')}

Coefficients describe outcome-unit differences per one percentage point of ART coverage. Most outcomes are annual AIDS deaths / estimated PLHIV ×100. The population-denominator sensitivity instead uses deaths per 100,000 population. First differences use annual changes. R-squared in the CSV is overall dummy-variable OLS R-squared, not within R-squared. Each row carries its actual countries, period, sample size, design rank and inference degrees of freedom.

Country-only versus country/year models use the same complete lag-1 sample. The GDP common-sample comparison is explicit. Other sensitivities can use different samples. The boundary scenario substitutes disclosed censor thresholds and must not be interpreted as observed data.

Standard errors cluster by country. Full country/year dummy-variable rank enters the finite-sample covariance correction. Two-sided intervals and p-values use a t reference with G−1 degrees of freedom. Only seven countries contribute to the uncensored primary sample. Few-cluster inference remains approximate, and no significance claim establishes causation.
"""
    limits='\n'.join('- '+v for v in r['limitations'])
    methods="""## Research design and definitions

Retrospective portfolio analysis of a frozen public snapshot. Research questions: how do national HIV outcomes change, how do treatment indicators differ, and how sensitive are ART–mortality associations to specification? The revised protocol documents analysis decisions made during review and is not a prospectively registered protocol.

The workbook has 6,624 entity-years for 184 entities, including regional/global aggregates. It is not 184 independent countries. Southeast Asia includes all 11 countries: Brunei, Cambodia, Indonesia, Lao PDR, Malaysia, Myanmar, Philippines, Singapore, Thailand, Timor-Leste, and Viet Nam. Outcomes span 1990–2025. Treatment comparisons span 2010–2025 (176 country-years).

**Censoring:** `<100`, `<500`, `>95`, and `>98` are bounds, not exact values. Numeric point fields remain missing, while `_source`, `_qualifier`, and `_threshold` preserve the published information. `...` remains unavailable. No suppressed or censored value is replaced in the primary models. Lags and differences require consecutive calendar years. Complete-case availability excludes Lao PDR and Timor-Leste from the uncensored mortality models, and some early Philippine values are censored. Brunei and Singapore lack reportable ART data for 2025. The resulting sample is selective.

**Cascade denominators:** first 95 = diagnosed / all PLHIV; second 95 = on ART / diagnosed; third 95 = suppressed / on ART. Population equivalents of the joint 95–95–95 target are 95%, 90.25% on ART, and 85.7375% suppressed. Comparisons of all-PLHIV ART coverage against a flat 95% line are inappropriate. Use the direct all-PLHIV suppression estimate. Products of rounded or censored conditional stages need not reproduce it.

**Treatment gaps:** estimated PLHIV × (1−ART coverage/100). This is an approximate national planning quantity. Low/high gap scenarios combine marginal PLHIV and ART limits, which lack joint covariance and therefore are not joint confidence intervals. Missing bounds remain missing.

**Sources and dependence:** UNAIDS Spectrum uses programme ART counts and assumed survival to estimate mortality. Regressions on estimated outcomes partly reproduce these assumptions. WHO disseminates the same UNAIDS source family, so matching feeds verifies snapshot consistency, not independent accuracy. Both coverage and the mortality/PLHIV ratio share an estimated denominator. It is not a person-time mortality rate or cohort fatality risk. Prevalence, incidence, deaths and survival can change together, but the aggregate series cannot isolate those mechanisms.

**Economic comparison:** GDP is same-year PPP in constant 2021 international dollars, joined by ISO3 and year. No interpolation or latest-year carry-forward occurs. Cross-sections do not measure financing or programme quality. Crosswalk income labels are static context, not historical annual classifications or model strata.
"""
    report='# HIV trends and treatment access in Southeast Asia, 1990–2025\n\nDr. Aung Chit Moe, MBBS. Revised 15 October 2026.\n\n'+methods+'\n'+results+'\n## Limitations\n\n'+limits+'\n\nThe Myanmar 2021–2022 change cannot be attributed to conflict, COVID-19, ART interruption or programme responses using these data. Country archetypes and claims that policy outweighs GDP have been removed because those mechanisms were not measured. No deaths-averted estimate is inferred from the regression.\n\n## Sources\n\n'+SOURCES
    (ROOT/'reports/research_report.md').write_text(report,encoding='utf-8',newline='\n')
    (ROOT/'docs/study_protocol.md').write_text('# Revised analysis protocol\n\n'+methods+'\n## Planned comparisons in this revision\n\nCountry FE current/lag1/lag2; country and year FE; GDP adjustment with common-sample comparison; pre-2020; omit Myanmar; first differences; population-denominator outcome; threshold substitution; leave-one-country-out. All are exploratory. Published marginal uncertainty limits are displayed for descriptive outcomes, but regression inference does not propagate estimate uncertainty.\n\n## Sources\n\n'+SOURCES,encoding='utf-8',newline='\n')
    readme="""# HIV trends and treatment access in Southeast Asia (1990–2025)

**Dr. Aung Chit Moe, MBBS · Healthcare data analytics portfolio**

[Live Streamlit dashboard](https://hiv-epidemiology-and-treatment-analytics-acm.streamlit.app/)

A reproducible descriptive study of national HIV estimates and treatment access, with exploratory panel-model comparisons. The project uses the stored UNAIDS 2026 and World Bank WDI snapshot. It does not establish programme effects or individual clinical risks.

## What this project demonstrates

Python data cleaning that preserves censoring and suppression, a SQLite star schema and seven analytical queries, transparent denominator definitions, clustered panel models with sensitivity comparisons, six 300 dpi figures, an executed notebook, and an editable 22-slide PowerPoint briefing. The dashboard offers filters, downloads, model comparisons and fixed read-only SQL examples.

## Review corrections

The earlier version substituted censor thresholds as exact values, overstated causal interpretation, used observation-robust rather than country-clustered inference, compared all-PLHIV ART against an incorrect target, and multiplied rounded cascade indicators to estimate suppression. This revision corrects those choices throughout the outputs. Original conclusions and sample sizes must not be mixed with this revision.

"""+results+"""
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

"""+limits+'\n\nSee the [research report](reports/research_report.md) for denominator definitions, selective missingness and source dependence.\n\n## Sources\n\n'+SOURCES+"\n## AI-assisted development\n\nThe author used AI assistance for code and presentation revision. Calculations and source-dependent limitations are documented for review. Authorship does not imply institutional endorsement.\n\nMIT license applies to project code. Source datasets remain subject to their providers’ terms.\n"
    (ROOT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
    (ROOT/'docs/cv_project_description.md').write_text('# CV project summary\n\nBuilt a reproducible HIV analytics portfolio for 11 Southeast Asian countries using UNAIDS 2026 and WDI snapshots. Preserved censored source values, designed SQLite queries, compared country/year panel associations with country-clustered inference and sensitivity scenarios, and published a Streamlit dashboard, six figures and 22-slide editable briefing. Primary lag-1 sample: 103 country-years, seven countries. Interpretation remains exploratory because mortality estimates incorporate ART assumptions.\n',encoding='utf-8',newline='\n')
if __name__=='__main__':write_docs()
