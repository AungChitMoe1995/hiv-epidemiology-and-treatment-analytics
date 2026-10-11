# RESEARCH STUDY PROTOCOL

**Project Title:**  
**HIV Epidemiological Transitions and Treatment Disparities in Southeast Asia (1990–2025): A Comparative Longitudinal Analysis of Myanmar Against Regional and Global Benchmarks**

**Investigator:**  
Healthcare Analytics & Epidemiological Research Team (Lead: Clinical Doctor & Healthcare Data Analyst, Myanmar)  

**Date:** October 2026  
**Protocol Version:** 1.0 (Approved for Implementation)  

---

## 1. Background & Epidemiological Rationale

The global HIV response over the past three decades represents one of the most significant public health campaigns in modern medicine. The scale-up of combination antiretroviral therapy (ART) has transformed HIV infection from a rapidly fatal condition into a manageable chronic disease. 

In Southeast Asia, home to over 680 million people, national HIV epidemics have historically been concentrated among key populations, including people who inject drugs (PWID), female sex workers (FSW), men who have sex with men (MSM), and transgender individuals. However, national responses across the region have diverged sharply:
- **Thailand and Cambodia** implemented early, aggressive harm reduction, structural interventions, and universal ART coverage, achieving dramatic declines in incidence and AIDS mortality.
- **Myanmar** achieved remarkable gains between 2010 and 2020 through rapid decentralization of ART services, scaling coverage from 12% to 69% and reducing AIDS-related mortality by over 60%. However, socio-political disruption and the COVID-19 pandemic post-2020 introduced acute health-system stresses that altered mortality trajectories.
- **The Philippines** is experiencing one of the fastest-growing HIV epidemics globally, with a sharp expansion in new infections and an escalating treatment gap.
- **Indonesia** continues to face a large burden with persistent treatment gaps and high AIDS-related mortality.

Understanding how ART coverage expansion interacts with AIDS mortality across these diverse health systems, and how macroeconomic status influences treatment success, is vital for guiding public health policy and resource allocation.

---

## 2. Research Questions & Hypotheses

### Primary Research Question:
- **RQ1:** How has the expansion of antiretroviral therapy (ART) coverage between 2010 and 2025 influenced AIDS-related mortality across Southeast Asian health systems, and what is the magnitude and lag structure of this protective association?
  - *Hypothesis 1:* Increases in national ART coverage are associated with subsequent reductions in population-level AIDS mortality with a 1-year and 2-year lag, but the rate of mortality reduction plateaus when ART coverage exceeds 80%.

### Secondary Research Questions:
- **RQ2 (Temporal Epidemiological Trajectories):** How have HIV incidence, adult prevalence, and AIDS-related mortality evolved from 1990 to 2025 in Myanmar compared to neighboring Southeast Asian nations and Asia-Pacific/Global benchmarks?
  - *Hypothesis 2:* Myanmar exhibits an initial epidemic peak in the early 2000s followed by sustained decline, with adult prevalence stabilizing as life expectancy among people living with HIV (PLHIV) expands under ART.
- **RQ3 (Treatment Disparities & Cascade Gaps):** Where do persistent treatment gaps remain along the UNAIDS 95-95-95 cascade across Southeast Asia, and which countries represent regional leaders versus lagging outliers?
  - *Hypothesis 3:* Regional disparity has widened; Cambodia and Thailand exceed or approach the 95-95-95 targets, whereas the Philippines and Indonesia suffer substantial treatment gaps exceeding 50%.
- **RQ4 (Socioeconomic Determinants):** Is national economic wealth (GDP per capita) associated with higher ART coverage and lower HIV mortality in Southeast Asia?
  - *Hypothesis 4:* In Southeast Asia, GDP per capita does not correlate strongly with ART coverage, as external donor financing (Global Fund, PEPFAR) and focused programmatic leadership enabled lower-income countries (Cambodia, Myanmar) to outperform middle-income decentralized systems.

---

## 3. Study Design & Unit of Analysis

- **Study Design:** Longitudinal, ecological comparative panel study combining long-term macro-epidemiological time-series analysis with high-resolution panel econometric modeling.
- **Unit of Analysis:** Country-year observation $(i, t)$, where $i \in \{\text{Country}\}$ and $t \in \{\text{Year}\}$.
- **Geographic Scope:**
  - **Core Study Group (Southeast Asia, 10 nations):** Myanmar (`MMR`), Thailand (`THA`), Viet Nam (`VNM`), Cambodia (`KHM`), Indonesia (`IDN`), Malaysia (`MYS`), Philippines (`PHL`), Lao PDR (`LAO`), Timor-Leste (`TLS`), Singapore (`SGP`).
  - **Regional Benchmark:** Asia and the Pacific (`UNAAP`).
  - **Global Benchmark:** Global Total (`03M49WLD`).
- **Temporal Windows:**
  - **1990–2025 (36 years):** Long-term epidemiological trends (incidence, prevalence, mortality, PLHIV).
  - **2010–2025 (16 years):** High-resolution treatment cascade (95-95-95 metrics, ART coverage, treatment gap) and econometric panel modeling.

---

## 4. Data Sources & Variables

### A. Authoritative Sources:
1. **UNAIDS 2026 Epidemiological Estimates:** Primary source for HIV burden, incidence, prevalence, AIDS mortality, and 95-95-95 treatment cascade data. Derived from Spectrum/EPP compartmental epidemiological models.
2. **WHO Global Health Observatory (GHO):** Validation source for UNAIDS syndication.
3. **World Bank World Development Indicators (WDI):** Macroeconomic indicators (GDP per capita in current US$ and PPP constant 2021 international $) and total population.

### B. Analytical Variables:
- **Primary Outcomes:**
  - `aids_deaths`: Estimated annual deaths from HIV/AIDS (Count).
  - `aids_mortality_rate_plhiv`: Cause-specific mortality rate per 100 people living with HIV:
    $$\text{Mortality Rate}_{\text{PLHIV}} = \left(\frac{\text{AIDS Deaths}}{\text{PLHIV}}\right) \times 100$$
  - `aids_mortality_rate_pop`: AIDS mortality rate per 100,000 general population.
- **Secondary Outcomes:**
  - `new_infections`: Annual new HIV infections (Count).
  - `hiv_incidence_rate`: New HIV infections per 1,000 uninfected population.
  - `adult_prevalence_pct`: HIV prevalence among adults aged 15–49 (%).
  - `plhiv_count`: Estimated total people living with HIV (Count).
- **Primary Exposures:**
  - `art_coverage_pct`: Proportion of PLHIV receiving antiretroviral therapy (%).
  - `treatment_gap_pct`: $100\% - \text{art\_coverage\_pct}$.
  - `unreached_plhiv`: Absolute count of PLHIV not receiving ART ($\text{PLHIV} \times [1 - \text{ART Coverage}]$).
  - `art_coverage_lag1`: 1-year lagged ART coverage ($t - 1$).
  - `art_coverage_lag2`: 2-year lagged ART coverage ($t - 2$).
- **Covariates:**
  - `gdp_per_capita_usd`: Current US$ per capita.
  - `gdp_per_capita_ppp`: Constant 2021 international $ per capita.
  - `population_total`: Total national population.

---

## 5. Inclusion, Exclusion, and Handling of Missing Data

1. **Inclusion Criteria:** All Southeast Asian countries with published official epidemiological estimates from 1990 to 2025.
2. **Exclusion Criteria:**
   - Brunei Darussalam (`BRN`): UNAIDS officially suppresses (`...`) estimates of PLHIV, deaths, and incidence due to low case counts making compartmental modeling unidentifiable. Retained in descriptive documentation but excluded from regression modeling.
3. **Missing Data & Suppressed Value Coding:**
   - Values encoded as `...` are treated as unobserved/suppressed, not zero.
   - Bounded values (e.g., `<100`, `<500`, `>95`, `>98`) and million-scaled strings (`m`) are parsed using deterministic boundary thresholds with sensitivity testing.
   - No silent interpolation or synthetic imputation is applied.
4. **Separation of Aggregates:** Regional codes (`UNAAP`) and global totals (`03M49WLD`) are maintained in separate benchmark tables to avoid double-counting.

---

## 6. Statistical & Analytical Plan

1. **Phase 1: Descriptive Epidemiology & Trajectory Profiling:**
   - Temporal trajectories of incidence, prevalence, mortality, and PLHIV from 1990 to 2025.
   - Uncertainty intervals (95% lower and upper bounds) plotted as shaded confidence envelopes.
   - Absolute and relative percent change between 2010 and 2025:
     $$\Delta\% = \left(\frac{Y_{2025} - Y_{2010}}{Y_{2010}}\right) \times 100$$
2. **Phase 2: Treatment Cascade & Disparity Analysis:**
   - Evaluation of progress toward UNAIDS 95-95-95 targets (2010–2025).
   - Quantification of national treatment gaps and regional burden concentration.
   - Classification into three regional epidemiological archetypes:
     * *Archetype A (Accelerated Control):* Thailand, Cambodia, Viet Nam.
     * *Archetype B (Fragile Steady Progress):* Myanmar, Malaysia, Lao PDR.
     * *Archetype C (Severe Counter-Epidemic):* Philippines, Indonesia.
3. **Phase 3: Econometric Panel Regression (Fixed Effects):**
   - Modeling the within-country association between ART coverage and AIDS mortality:
     $$\text{Mortality Rate}_{it} = \alpha_i + \beta_1 \text{ART Coverage}_{i, t-k} + \gamma \ln(\text{GDP}_{it}) + \epsilon_{it}$$
     where $\alpha_i$ is country fixed effects, eliminating time-invariant confounding (e.g., geography, baseline healthcare infrastructure).
   - Evaluation of contemporaneous ($k=0$), 1-year lag ($k=1$), and 2-year lag ($k=2$) specifications.
4. **Phase 4: Socioeconomic & Health Financing Cross-Sectional Analysis:**
   - Correlation and scatter analysis of national wealth versus treatment coverage to test whether economic development alone explains ART success.

---

## 7. Methodological Boundaries & Limitations

1. **Ecological Fallacy:** As an ecological country-level analysis, findings reflect population-level trends and cannot establish individual-level clinical causality or treatment adherence.
2. **Model-Based Data:** UNAIDS estimates are generated by Spectrum/EPP epidemiological models calibrated with surveillance and survey data, rather than complete vital statistics death registries.
3. **Uncertainty Propagation:** 95% uncertainty intervals are widest in countries with limited surveillance infrastructure and narrowest in high-surveillance settings (e.g., Thailand).
4. **Confounding by External Aid:** National GDP per capita does not account for external health financing (e.g., Global Fund, PEPFAR), which accounts for a substantial fraction of HIV programming in Myanmar and Cambodia.

---
