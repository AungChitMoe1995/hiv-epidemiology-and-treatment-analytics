# HIV Epidemiological Transitions and Treatment Disparities in Southeast Asia (1990–2025): A Comparative Longitudinal Analysis of Myanmar Against Regional and Global Benchmarks

**Principal Investigator:** Clinical Medical Doctor (MBBS, Myanmar) & Healthcare Data Analyst  
**Affiliation:** Healthcare Analytics & Clinical Epidemiological Research Group  
**Date:** October 2026  
**Document Type:** Scientific Research Report & Portfolio Deliverable  

---

## Abstract

**Background:** The global expansion of combination antiretroviral therapy (ART) has transformed HIV from an acute fatal infection into a manageable chronic disease. However, progress across Southeast Asia has diverged significantly. This study investigates temporal epidemiological trajectories, UNAIDS 95-95-95 cascade performance, and the lagged impact of ART coverage on AIDS-related mortality across 11 Southeast Asian nations and regional/global benchmarks from 1990 to 2025, with an in-depth clinical evaluation of Myanmar.

**Methods:** We constructed a longitudinal panel dataset (6,624 country-year observations across 184 entities) combining official UNAIDS 2026 modeled epidemiological estimates, WHO Global Health Observatory (GHO) surveillance data, and World Bank World Development Indicators (WDI). We analyzed 36-year trajectories (1990–2025) and Fast-Track performance (2010–2025). Econometric panel regressions with country fixed effects (Within transformation) and heteroskedasticity-robust standard errors (HC1) were estimated using contemporaneous ($N = 144$), 1-year lagged ($N = 135$), and 2-year lagged ($N = 126$) specifications to evaluate the dose-response relationship between ART expansion and crude AIDS-related mortality rates in people living with HIV (PLHIV).

**Results:** Across Southeast Asia, national ART responses have created three distinct epidemiological archetypes:
1. *Archetype A (Accelerated Control):* Cambodia (95% ART, -41.2% deaths, -58.3% new infections), Thailand (82% ART, -79.5% deaths, -65.2% new infections), and Viet Nam (75% ART, -14.6% deaths, -56.4% new infections).
2. *Archetype B (Fragile Steady Progress):* Myanmar achieved a 63.3% mortality reduction between 2010 and 2025 (annual AIDS deaths falling from 12,000 to 4,400) and a 44.1% incidence reduction (17,000 to 9,500) as ART coverage expanded by +61.0 percentage points (from 12% to 73%). However, sociopolitical instability and COVID-19 disruption in 2021 caused an acute ART coverage dip from 69% to 66% (-3 percentage points), triggering an immediate 1-year lagged mortality rebound in 2022 (+11.6%, from 4,300 to 4,800 deaths) before stabilizing at 4,400 deaths in 2025. Total PLHIV in Myanmar grew from 230,000 (2006) to 310,000 (2025) while adult prevalence remained steady at 0.9%, illustrating the survival-driven "prevalence paradox."
3. *Archetype C (Severe Counter-Epidemic & Treatment Gap):* The Philippines experienced an alarming +639.1% surge in annual new infections (4,600 to 34,000) and a +440.0% increase in AIDS deaths (500 to 2,700), with ART coverage lagging at 41% (59% treatment gap). Indonesia experienced a +28.6% rise in AIDS deaths (14,000 to 18,000) alongside a persistent 52% treatment gap (291,200 untreated PLHIV). Together, Indonesia (39.0%) and the Philippines (19.8%) account for 58.8% of all 745,778 untreated PLHIV in Southeast Asia.

In fixed-effects panel modeling, 1-year lagged ART coverage was strongly protective against AIDS mortality in PLHIV ($\beta = -0.0491, t = -14.202, p < 0.00001, R^2_{\text{within}} = 0.6874, N = 135$), increasing in magnitude when controlling for log GDP per capita PPP ($\beta = -0.0624, t = -12.830, p < 0.00001, R^2_{\text{within}} = 0.7307, N = 135$). Cross-sectionally, national GDP per capita PPP was decoupled from ART coverage ($r = +0.149$), with lower-middle-income countries (Cambodia \$7,300 PPP, 95% ART; Myanmar \$5,137 PPP, 73% ART) outperforming wealthier middle-income peers (Indonesia \$15,091 PPP, 48% ART; Malaysia \$35,461 PPP, 63% ART).

**Conclusions:** Scaling ART coverage confers substantial, quantifiable survival gains at the population level, but uninterrupted supply chain and clinical service stability are vital. In concentrated epidemics, sustained vertical programming, harm reduction, and external donor execution supersede aggregate macroeconomic wealth in driving HIV epidemic control.

---

## 1. Introduction & Epidemiological Context

Over the last four decades, the global HIV pandemic has claimed over 40 million lives. The advent and worldwide scale-up of combination antiretroviral therapy (ART) under the UNAIDS 90-90-90 and 95-95-95 frameworks have averted tens of millions of deaths and fundamentally altered population-level disease dynamics. Globally, between 2010 and 2025, annual AIDS-related deaths declined by 56.2% (from 1,300,000 to 570,000) and annual new HIV infections fell by 42.9% (from 2,100,000 to 1,200,000) as global ART coverage rose from 24% to 78%.

In Southeast Asia, HIV epidemics are predominantly concentrated among key populations: people who inject drugs (PWID), female sex workers (FSW), men who have sex with men (MSM), and transgender women. Despite geographic proximity, regional health systems have achieved starkly different trajectories:
- **Cambodia, Thailand, and Viet Nam** pioneered aggressive prevention, harm reduction, and universal ART integration, achieving high treatment coverage (75%–95%).
- **Myanmar**, despite severe historical fiscal constraints, mounted a major decentralized scale-up of ART between 2010 and 2020 through the National AIDS Programme (NAP) and international donor partnerships (The Global Fund, PEPFAR). However, compounded political disruption and the COVID-19 pandemic in 2021–2022 tested the resilience of HIV care delivery.
- **The Philippines and Indonesia** face severe upstream testing and linkage bottlenecks, decentralized service fragmentation, and expanding mortality burdens.

---

## 2. Research Questions & Pre-Specified Hypotheses

1. **Primary Question (RQ1 — Lagged Mortality Impact):** What is the magnitude and lag structure of the association between national ART coverage expansion and subsequent reductions in population-level AIDS mortality across Southeast Asian health systems (2010–2025)?
2. **Longitudinal Trajectory (RQ2 — Myanmar Focus):** How have HIV incidence, adult prevalence, total PLHIV, and AIDS-related mortality evolved from 1990 to 2025 in Myanmar compared to regional neighbors and global benchmarks?
3. **Care Continuum Disparities (RQ3 — 95-95-95 Cascade):** Where do persistent diagnosis, linkage, and viral suppression bottlenecks remain along the UNAIDS 95-95-95 cascade in 2025, and how do regional archetypes diverge?
4. **Macroeconomic Determinants (RQ4 — Health Financing Paradox):** Does national macroeconomic wealth (GDP per capita PPP) linearly correlate with ART coverage and mortality reductions across Southeast Asia?

---

## 3. Data & Methodology

### 3.1 Authenticated Data Sources
We integrated three authoritative, open-access public health and economic repositories:
1. **UNAIDS 2026 Epidemiological Estimates Database (`Estimates_2026_en.csv` & `UNAIDS_HIV_estimates_1990_to_present.xlsx`):** Modeled national and regional estimates generated via Spectrum/EPP software. Provides 1990–2025 time-series for prevalence, incidence, mortality, and PLHIV (`HIV2026Estimates_ByYear`, 6,228 rows), and 2010–2025 time-series for the 95-95-95 testing, treatment, and viral suppression cascade (`HIV-Test-&-Treat_ByYear`, 2,944 rows), complete with 95% uncertainty intervals (Low / High bounds).
2. **WHO Global Health Observatory (GHO):** REST OData API feeds (`HIV_0000000006`, `HIV_ARTCOVERAGE`, `HIV_0000000026`, `HIV_0000000001`; 15,320 records) used to independently verify numerical concordance with UNAIDS.
3. **World Bank World Development Indicators (WDI):** Annual GDP per capita in current US\$ (`NY.GDP.PCAP.CD`), PPP constant 2021 international \$ (`NY.GDP.PCAP.PP.KD`), and total population (`SP.POP.TOTL`; 28,728 combined country-year records).

### 3.2 Censoring, Scale Parsing & Suppression Rules
- **Bounded Surveillance Strings:** Official UNAIDS surveillance sheets report low counts/rates with `<` prefixes (e.g., `<100`, `<500`, `<0.1`) and upper cascade achievements with `>` prefixes (e.g., `>95`, `>98` for Cambodia and Thailand's 2nd and 3rd 95s). Our ETL parser (`src/cleaning/clean_and_harmonize.py`) systematically parses these at their numeric boundary threshold while preserving raw provenance.
- **Million-Scale Aggregates:** Global (`03M49WLD`) and regional (`UNAAP`) aggregates expressed with `'m'` suffixes (e.g., `'32.5 m'`, `'6.0 m'`, `'1.3 m'`) are programmatically scaled by $10^6$.
- **Zero Synthetic Imputation:** Suppressed microstate records (`'...'` in Brunei Darussalam and suppressed cascade cells in Singapore) are retained as `NaN` / `NULL` and never synthetically interpolated.

### 3.3 Key Indicators & Mathematical Definitions
- **Adult HIV Prevalence (%):** Percentage of adults aged 15–49 living with HIV.
- **Crude AIDS-Related Mortality Rate in PLHIV (%):**
  $$\text{Mortality Rate}_{\text{PLHIV}, it} = \left(\frac{\text{AIDS Deaths}_{it}}{\text{PLHIV}_{it}}\right) \times 100$$
- **AIDS Mortality Rate per 100,000 Total Population:**
  $$\text{Mortality Rate}_{\text{Pop}, it} = \left(\frac{\text{AIDS Deaths}_{it}}{\text{Population}_{it}}\right) \times 100,000$$
- **Treatment Gap (%):** $100.0 - \text{ART Coverage}_{it}$
- **Unreached PLHIV Count:** $\text{PLHIV}_{it} \times \left(\frac{\text{Treatment Gap}_{it}}{100.0}\right)$
- **Population-Level Viral Suppression (% of all PLHIV):**
  $$\text{Viral Suppression}_{\text{Pop}, it} = \frac{\text{1st 95}_{it} \times \text{2nd 95}_{it} \times \text{3rd 95}_{it}}{10,000}$$

### 3.4 Econometric Panel Regressions (Within Estimator)
To account for non-independent repeated country-year observations and eliminate time-invariant national confounding (such as baseline age-cohort structure, island geography, and health-system history), we estimated country fixed-effects models using the Within transformation:

$$y_{it} - \bar{y}_i = \beta_1 (x_{i, t-k} - \bar{x}_i) + \gamma (\ln(\text{GDP}_{it}) - \overline{\ln(\text{GDP})}_i) + (u_{it} - \bar{u}_i)$$

where $y_{it}$ is the crude AIDS mortality rate in PLHIV (%), $x_{i, t-k}$ is national ART coverage (%) at lag $k \in \{0, 1, 2\}$, and standard errors are estimated using White's heteroskedasticity-robust covariance matrix (`HC1`).

---

## 4. Empirical Findings

### 4.1 Long-Term Trajectories & The Myanmar Experience (1990–2025)
Myanmar's HIV epidemic expanded rapidly during the 1990s among PWID and sex workers, with annual new HIV infections peaking at **27,000 in 2000** (adult incidence rate 0.59 per 1,000) and annual AIDS-related deaths peaking at **13,000 in 2006** (5.65% annual mortality among PLHIV).

| Year | Total PLHIV | Adult Prev (%) | New Infections | Incidence / 1,000 | AIDS Deaths | ART Coverage (%) | Unreached PLHIV | Mortality / 100 PLHIV (%) | GDP per Capita (US\$) |
|---|---|---|---|---|---|---|---|---|---|
| **1990** | 28,000 | 0.1% | 15,000 | 0.38 | 500 | N/A | N/A | 1.79% | \$53 |
| **1995** | 96,000 | 0.4% | 16,000 | 0.37 | 2,700 | N/A | N/A | 2.81% | \$124 |
| **2000** | 170,000 | 0.7% | 27,000 (Peak) | 0.59 | 7,400 | N/A | N/A | 4.35% | \$197 |
| **2006** | 230,000 | 0.9% | 20,000 | 0.43 | 13,000 (Peak) | N/A | N/A | 5.65% | \$303 |
| **2010** | 250,000 | 0.9% | 17,000 | 0.34 | 12,000 | 12.0% | 220,000 | 4.80% | \$1,011 |
| **2015** | 270,000 | 0.9% | 14,000 | 0.28 | 7,800 | 40.0% | 162,000 | 2.89% | \$1,167 |
| **2020** | 290,000 | 0.9% | 10,000 | 0.20 | 4,400 | 69.0% | 89,900 | 1.52% | \$1,490 |
| **2021** | 290,000 | 0.9% | 11,000 | 0.21 | 4,300 | 66.0% (-3 pp) | 98,600 | 1.48% | \$1,243 |
| **2022** | 300,000 | 0.9% | 11,000 | 0.20 | 4,800 (+11.6%) | 70.0% | 90,000 | 1.60% | \$1,158 |
| **2024** | 300,000 | 0.9% | 9,900 | 0.18 | 4,400 | 72.0% | 84,000 | 1.47% | \$1,359 |
| **2025** | 310,000 | 0.9% | 9,500 | 0.17 | 4,400 | 73.0% | 83,700 | 1.42% | \$1,489 |

*(See [`figures/fig1_myanmar_longitudinal_trajectory.png`](../figures/fig1_myanmar_longitudinal_trajectory.png) and [`reports/analysis_tables/myanmar_trajectory_summary.csv`](analysis_tables/myanmar_trajectory_summary.csv))*

**Key Clinical & Epidemiological Insights:**
1. **The Survival-Driven Prevalence Paradox:** Between 2006 and 2025, Myanmar's adult HIV prevalence remained flat at **0.9%**, while the total number of people living with HIV increased from **230,000 to 310,000 (+34.8%)** even as annual new infections fell by **52.5% (20,000 to 9,500)**. Because prevalence reflects both inflow (incidence) and outflow (mortality), scaling ART from 12% to 73% dramatically prolonged patient survival, expanding the living cohort.
2. **The 2021–2022 Crisis & Lagged Mortality Rebound:** In 2021, compounded political instability and COVID-19 service disruptions caused Myanmar's national ART coverage to drop from **69.0% to 66.0% (-3.0 percentage points)**, expanding the untreated cohort from 89,900 to 98,600 PLHIV. Consistent with our 1-year biological lag model, annual AIDS-related deaths rebounded by **+11.6% in 2022 (rising from 4,300 to 4,800 deaths)**, before multi-month dispensing (MMD) and NGO/community clinic adaptations restored coverage to **73.0%** (4,400 deaths) by 2025.

---

### 4.2 Fast-Track Regional Divergence: Three Epidemiological Archetypes (2010–2025)
Between 2010 and 2025, Southeast Asian health systems diverged into three distinct trajectories:

| Country / Benchmark | ISO3 | PLHIV (2025) | AIDS Deaths 2010 | AIDS Deaths 2025 | Deaths Change (%) | New Inf 2010 | New Inf 2025 | New Inf Change (%) | ART 2010 → 2025 (Gain) |
|---|---|---|---|---|---|---|---|---|---|
| **Thailand** | `THA` | 620,000 | 41,000 | 8,400 | **-79.5%** | 21,000 | 7,300 | **-65.2%** | 27% → 82% (+55 pp) |
| **Myanmar** | `MMR` | 310,000 | 12,000 | 4,400 | **-63.3%** | 17,000 | 9,500 | **-44.1%** | 12% → 73% (+61 pp) |
| **Cambodia** | `KHM` | 76,000 | 1,700 | 1,000 | **-41.2%** | 2,300 | 960 | **-58.3%** | 50% → 95% (+45 pp) |
| **Malaysia** | `MYS` | 85,000 | 3,400 | 2,000 | **-41.2%** | 6,100 | 2,900 | **-52.5%** | 18% → 63% (+45 pp) |
| **Viet Nam** | `VNM` | 270,000 | 4,800 | 4,100 | **-14.6%** | 14,000 | 6,100 | **-56.4%** | 25% → 75% (+50 pp) |
| **Timor-Leste** | `TLS` | 2,200 | 100 | 100 | **0.0%** | 200 | 200 | **0.0%** | 6% → 66% (+60 pp) |
| **Lao PDR** | `LAO` | 23,000 | 500 | 500 | **0.0%** | 1,200 | 1,300 | **+8.3%** | 17% → 64% (+47 pp) |
| **Singapore** | `SGP` | 7,800 | 100 | 100 | **0.0%** | 500 | 200 | **-60.0%** | 55% → N/A (Suppressed) |
| **Indonesia** | `IDN` | 560,000 | 14,000 | 18,000 | **+28.6%** | 48,000 | 21,000 | **-56.2%** | 5% → 48% (+43 pp) |
| **Philippines** | `PHL` | 250,000 | 500 | 2,700 | **+440.0%** | 4,600 | 34,000 | **+639.1%** | 5% → 41% (+36 pp) |
| *Asia & Pacific (Ref)* | `UNAAP` | 7,100,000 | 300,000 | 120,000 | *-60.0%* | 350,000 | 280,000 | *-20.0%* | 15% → 72% (+57 pp) |
| *Global (Ref)* | `03M49WLD` | 41,000,000 | 1,300,000 | 570,000 | *-56.2%* | 2,100,000 | 1,200,000 | *-42.9%* | 24% → 78% (+54 pp) |

*(See [`figures/fig2_southeast_asia_mortality_infection_divergence.png`](../figures/fig2_southeast_asia_mortality_infection_divergence.png) and [`figures/fig6_southeast_asia_art_trajectories_2010_2025.png`](../figures/fig6_southeast_asia_art_trajectories_2010_2025.png))*

- **Archetype A (Accelerated Epidemic Control — Cambodia, Thailand, Viet Nam):** High ART coverage ($\ge 75\%$), strong testing cascades, and sustained reductions in both new HIV infections (-56% to -65%) and AIDS mortality (-15% to -80%).
- **Archetype B (Fragile Steady Progress — Myanmar, Timor-Leste, Lao PDR, Malaysia):** Substantial cumulative ART gains (+45 to +61 percentage points), with Myanmar outperforming both the Asia-Pacific (-60.0%) and Global (-56.2%) mortality reduction benchmarks despite severe 2021–2022 system stress.
- **Archetype C (Counter-Epidemic / Severe Treatment Gap — Philippines, Indonesia):** Low ART coverage (<50%) and >50% treatment gaps. The Philippines faces the fastest-growing HIV epidemic in the region (+639.1% new infections, +440.0% AIDS deaths), while Indonesia experiences rising AIDS deaths (+28.6%) as large untreated cohorts progress to late-stage disease.

---

### 4.3 UNAIDS 95-95-95 Cascade & Regional Burden Concentration (2025)

| Country / Benchmark | 1st 95 (% Diagnosed) | 2nd 95 (% on ART of Diagnosed) | 3rd 95 (% Suppressed on ART) | Overall ART Coverage (%) | Treatment Gap (%) | Unreached PLHIV (2025) | Share of SEA Unreached (%) | Pop Viral Suppression (%) |
|---|---|---|---|---|---|---|---|---|
| **Cambodia** | 95.0% | >98.0% | >98.0% | **95.0%** | 5.0% | 3,800 | 0.5% | 91.2% |
| **Thailand** | 90.0% | 92.0% | >98.0% | **82.0%** | 18.0% | 111,600 | 15.0% | 81.1% |
| **Viet Nam** | 94.0% | 79.0% | 96.0% | **75.0%** | 25.0% | 67,500 | 9.1% | 71.3% |
| **Myanmar** | 84.0% | 86.0% | 96.0% | **73.0%** | 27.0% | 83,700 | 11.2% | 69.4% |
| **Timor-Leste** | 89.0% | 74.0% | 70.0% | **66.0%** | 34.0% | 748 | 0.1% | 46.1% |
| **Lao PDR** | 75.0% | 86.0% | 97.0% | **64.0%** | 36.0% | 8,280 | 1.1% | 62.6% |
| **Malaysia** | 66.0% | 95.0% | 88.0% | **63.0%** | 37.0% | 31,450 | 4.2% | 55.2% |
| **Indonesia** | 67.0% | 72.0% | 95.0% | **48.0%** | 52.0% | 291,200 | **39.0%** | 45.8% |
| **Philippines** | 62.0% | 66.0% | 97.0% | **41.0%** | 59.0% | 147,500 | **19.8%** | 39.7% |
| *Global (Ref)* | *88.0%* | *89.0%* | *95.0%* | *78.0%* | *22.0%* | *9,020,000* | — | *74.4%* |
| *Asia-Pacific (Ref)* | *81.0%* | *88.0%* | *96.0%* | *72.0%* | *28.0%* | *1,988,000* | — | *68.4%* |

*(See [`figures/fig3_unaids_95_95_95_cascade_2025.png`](../figures/fig3_unaids_95_95_95_cascade_2025.png))*

**Clinical Bottleneck Analysis:**
- **Potent Regimen Efficacy (3rd 95):** Across almost all Southeast Asian nations (except Timor-Leste at 70% and Malaysia at 88%), viral suppression among patients retained on ART exceeds **95%** (reaching 96% in Myanmar and Viet Nam, 97% in Lao PDR and the Philippines, and >98% in Cambodia and Thailand), reflecting the high virological efficacy of Tenofovir/Lamivudine/Dolutegravir (TLD) regimens.
- **Upstream Diagnosis & Linkage Failure (1st & 2nd 95):** The regional treatment gap of **745,778 unreached PLHIV** is driven by late diagnosis and post-diagnosis linkage attrition in **Indonesia (291,200 unreached; 39.0%)** and **the Philippines (147,500 unreached; 19.8%)**, which together hold **58.8%** of all untreated PLHIV in Southeast Asia.

---

### 4.4 Econometric Fixed-Effects Panel Modeling (2010–2025)
To estimate the within-country protective effect of ART expansion on crude AIDS mortality rates among PLHIV across the 9 active regression countries (`MMR, THA, VNM, KHM, IDN, MYS, PHL, LAO, TLS`), we estimated four fixed-effects specifications:

| Model Specification (Within Fixed Effects) | Independent Variable | Coefficient ($\beta$) | Robust SE (HC1) | $t$-Statistic | $p$-Value | 95% CI | Within $R^2$ | Observations ($N$) |
|---|---|---|---|---|---|---|---|---|
| **Model 1:** Contemporaneous ART (2010–2025) | `art_coverage_pct` ($t$) | **-0.0514** | 0.0036 | -14.344 | $< 0.00001$ | [-0.0585, -0.0443] | 0.6868 | 144 (9 countries) |
| **Model 2:** 1-Year Lagged ART (2011–2025) | `art_coverage_lag1` ($t-1$) | **-0.0491** | 0.0035 | -14.202 | $< 0.00001$ | [-0.0559, -0.0422] | 0.6874 | 135 (9 countries) |
| **Model 3:** 2-Year Lagged ART (2012–2025) | `art_coverage_lag2` ($t-2$) | **-0.0462** | 0.0035 | -13.302 | $< 0.00001$ | [-0.0531, -0.0393] | 0.6674 | 126 (9 countries) |
| **Model 4:** Lagged ART + Macro Control (2011–2025) | `art_coverage_lag1` ($t-1$) | **-0.0624** | 0.0049 | -12.830 | $< 0.00001$ | [-0.0721, -0.0528] | 0.7307 | 135 (9 countries) |
| **Model 4:** Lagged ART + Macro Control (2011–2025) | `log_gdp_pc_ppp` ($t$) | **+1.8376** | 0.5688 | +3.231 | $0.00123$ | [+0.7124, +2.9628] | 0.7307 | 135 (9 countries) |

*(See [`figures/fig4_lagged_art_mortality_dose_response.png`](../figures/fig4_lagged_art_mortality_dose_response.png) and [`reports/analysis_tables/panel_regression_models.csv`](analysis_tables/panel_regression_models.csv))*

**Methodological & Clinical Interpretation:**
1. **Why Within-Country Fixed Effects Are Essential:** In an unadjusted pooled scatter (Figure 4, Panel A), the Philippines sits at the bottom-left (~0.9%–2.1% mortality despite 5%–41% ART coverage) because its outbreak is newly acquired among young cohorts who have not yet progressed to late-stage AIDS death. Within-country demeaning (Figure 4, Panel B) eliminates baseline cohort-age and geographic confounders, isolating the true longitudinal survival effect ($\beta = -0.0491, p < 0.00001$).
2. **Dose-Response Magnitude:** Every **+10 percentage point increase in national ART coverage in year $t-1$ reduces the crude AIDS mortality rate among PLHIV by 0.49 percentage points in year $t$** (or **0.62 percentage points** holding log GDP per capita PPP constant). In Myanmar's cohort of 310,000 PLHIV, a +10 percentage point increase in ART coverage averts approximately **1,520 AIDS deaths per year**.

---

### 4.5 Socioeconomic Disparity Analysis: The Health Financing Decoupling
Cross-sectional correlation between national GDP per capita (PPP, constant 2021 international \$) and ART coverage is weak ($r = +0.149$):
- **Low-Income Overachievers:** **Cambodia** (\$7,300 PPP) achieved **95% ART coverage**, and **Myanmar** (\$5,137 PPP) achieved **73% ART coverage**, outperforming the Asia-Pacific regional benchmark (72%).
- **Middle-Income Laggards:** **Indonesia** (\$15,091 PPP) achieved only **48% ART coverage**, and **the Philippines** (\$10,748 PPP) achieved **41% ART coverage**.
- **Upper-Middle-Income Divergence:** **Thailand** (\$22,432 PPP) integrated universal HIV care into its domestic Universal Coverage Scheme (**82% ART**), whereas **Malaysia** (\$35,461 PPP) lags in 1st-95 diagnosis (66%), capping overall ART coverage at **63%**.

*(See [`figures/fig5_gdp_vs_art_coverage_disparity.png`](../figures/fig5_gdp_vs_art_coverage_disparity.png))*

---

## 5. Discussion & Actionable Policy Recommendations

1. **Myanmar (Archetype B — Conflict-Resilient Service Delivery):** Myanmar's 2021–2022 mortality rebound demonstrates that antiretroviral therapy is fragile to supply-chain interruptions. Sustaining Myanmar's gains requires institutionalizing **6-month Multi-Month Dispensing (MMD)** of TLD regimens, expanding mobile NGO and peer-led community ART delivery in conflict-affected regions (Kachin, Shan, Sagaing), and deploying portable patient records for displaced PLHIV.
2. **Philippines & Indonesia (Archetype C — Emergency Testing & Linkage):** Addressing the 438,700 untreated PLHIV across both nations requires removing adolescent age-of-consent testing barriers in the Philippines, scaling up community-based HIV self-testing and PrEP for young MSM, and enforcing **Same-Day ART Initiation** upon diagnosis in Indonesia's decentralized clinics.
3. **Cambodia, Thailand & Viet Nam (Archetype A — Last-Mile Elimination):** Transitioning donor-supported key-population services into sustainable domestic Universal Health Coverage (UHC) budgets and deploying long-acting injectable PrEP (Cabotegravir-LA) will secure epidemic elimination by 2030.

---

## 6. Methodological Boundaries & Study Limitations

1. **Spectrum / EPP Modeled Estimates:** National HIV indicators are generated by UNAIDS Spectrum compartmental models calibrated to sentinel surveillance and surveys rather than complete vital registration death certificates. Because historical ART patient counts are structural inputs into Spectrum survival curves, regression coefficients reflect both empirical mortality declines and demographic model parameterization.
2. **Ecological Fallacy Boundary:** Our unit of observation is the national country-year ($N = 144$). Findings quantify population-level health-system performance and cannot be extrapolated to individual patient hazard ratios without patient-level clinical cohort data.
3. **Censoring & Microstate Suppression:** Bounded surveillance strings (`<100`, `<500`, `>98%`) are parsed at their numeric threshold, and suppressed microstate cells (`'...'` in Brunei Darussalam and Singapore's cascade) are excluded from regression modeling without synthetic imputation.
4. **Sub-National Heterogeneity:** National aggregates for Myanmar mask sub-national divergence between urban centers (Yangon, Mandalay) and conflict-affected border states.

---

## 7. Conclusions

Antiretroviral therapy expansion has transformed HIV survival across Southeast Asia, enabling Myanmar to reduce annual AIDS deaths by 63.3% between 2010 and 2025 despite severe economic and political headwinds. However, Myanmar's 2022 mortality rebound and the severe treatment gaps in Indonesia and the Philippines prove that biomedical efficacy must be matched by resilient health-system delivery, stigma-free testing, and sustained financing.
