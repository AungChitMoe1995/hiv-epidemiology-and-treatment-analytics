-- ====================================================================
-- 03_analytical_queries.sql
-- Production Analytical SQL Queries for Epidemiological Research
-- Evaluates HIV Trends, Treatment Gaps, Cascade Performance & Disparities
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: MYANMAR LONGITUDINAL TRAJECTORY (1990-2025)
-- Evaluates Myanmar's complete 36-year epidemiological progression,
-- highlighting the peak, the 2010-2020 ART expansion, and post-2020 disruption.
-- --------------------------------------------------------------------
SELECT 
    year,
    adult_prevalence_pct AS adult_prev_pct,
    plhiv AS total_plhiv,
    new_infections AS annual_new_infections,
    aids_deaths AS annual_aids_deaths,
    art_coverage_pct AS art_coverage_pct,
    treatment_gap_pct AS treatment_gap_pct,
    unreached_plhiv AS unreached_plhiv,
    ROUND(mortality_rate_in_plhiv_pct, 2) AS mortality_per_100_plhiv_pct,
    ROUND(aids_mortality_rate_per100k_pop, 2) AS aids_deaths_per_100k_pop,
    ROUND(gdp_per_capita_usd, 0) AS gdp_pc_usd
FROM v_southeast_asia_surveillance
WHERE iso3 = 'MMR'
ORDER BY year ASC;


-- --------------------------------------------------------------------
-- QUERY 2: SOUTHEAST ASIA MILESTONE COMPARISON (2010 vs 2015 vs 2020 vs 2025)
-- Multi-year cross-sectional comparison across all 11 SEA countries and benchmarks.
-- --------------------------------------------------------------------
SELECT 
    country_name,
    iso3,
    year,
    plhiv,
    new_infections,
    aids_deaths,
    art_coverage_pct,
    treatment_gap_pct,
    ROUND(mortality_rate_in_plhiv_pct, 2) AS mort_rate_in_plhiv_pct
FROM v_southeast_asia_surveillance
WHERE year IN (2010, 2015, 2020, 2025)
  AND (is_southeast_asia = 1 OR iso3 IN ('UNAAP', '03M49WLD'))
ORDER BY country_name ASC, year ASC;


-- --------------------------------------------------------------------
-- QUERY 3: 2010-2025 RELATIVE CHANGES & FAST-TRACK PERFORMANCE
-- Calculates absolute and percentage change in AIDS deaths and new infections,
-- alongside percentage point gains in ART coverage from 2010 to 2025.
-- --------------------------------------------------------------------
WITH base_2010 AS (
    SELECT 
        iso3, country_name, analysis_role,
        aids_deaths AS deaths_2010,
        new_infections AS inf_2010,
        art_coverage_pct AS art_2010,
        plhiv AS plhiv_2010
    FROM v_southeast_asia_surveillance
    WHERE year = 2010
),
current_2025 AS (
    SELECT 
        iso3,
        aids_deaths AS deaths_2025,
        new_infections AS inf_2025,
        art_coverage_pct AS art_2025,
        plhiv AS plhiv_2025
    FROM v_southeast_asia_surveillance
    WHERE year = 2025
)
SELECT 
    b.country_name,
    b.iso3,
    b.analysis_role,
    b.deaths_2010,
    c.deaths_2025,
    ROUND(((c.deaths_2025 - b.deaths_2010) * 100.0 / NULLIF(b.deaths_2010, 0)), 1) AS pct_change_deaths,
    b.inf_2010,
    c.inf_2025,
    ROUND(((c.inf_2025 - b.inf_2010) * 100.0 / NULLIF(b.inf_2010, 0)), 1) AS pct_change_new_infections,
    b.art_2010,
    c.art_2025,
    ROUND(c.art_2025 - b.art_2010, 1) AS art_gain_percentage_points
FROM base_2010 b
JOIN current_2025 c ON b.iso3 = c.iso3
WHERE b.deaths_2010 IS NOT NULL
ORDER BY pct_change_deaths ASC;


-- --------------------------------------------------------------------
-- QUERY 4: UNAIDS 95-95-95 CASCADE PERFORMANCE (2025 SNAPSHOT)
-- Evaluates testing, treatment, and viral suppression cascaded metrics.
-- --------------------------------------------------------------------
SELECT 
    country_name,
    iso3,
    plhiv,
    diagnosed_1st95_pct AS pct_diagnosed_1st95,
    on_art_2nd95_pct AS pct_on_art_of_diagnosed_2nd95,
    virally_suppressed_3rd95_pct AS pct_suppressed_of_on_art_3rd95,
    art_coverage_pct AS overall_art_coverage_pct,
    virally_suppressed_all_pct AS pop_level_viral_suppression_pct
FROM v_southeast_asia_surveillance
WHERE year = 2025
  AND (is_southeast_asia = 1 OR iso3 IN ('UNAAP', '03M49WLD'))
ORDER BY overall_art_coverage_pct DESC;


-- --------------------------------------------------------------------
-- QUERY 5: REGIONAL TREATMENT GAPS & UNREACHED PLHIV BURDEN (2025)
-- Quantifies the absolute volume of untreated individuals living with HIV.
-- --------------------------------------------------------------------
SELECT 
    country_name,
    iso3,
    income_group,
    plhiv AS total_plhiv_2025,
    art_coverage_pct,
    treatment_gap_pct,
    ROUND(unreached_plhiv, 0) AS unreached_plhiv_count,
    ROUND((unreached_plhiv * 100.0 / SUM(unreached_plhiv) OVER()), 1) AS share_of_regional_unreached_pct
FROM v_southeast_asia_surveillance
WHERE year = 2025
  AND is_southeast_asia = 1
  AND unreached_plhiv IS NOT NULL
ORDER BY unreached_plhiv_count DESC;


-- --------------------------------------------------------------------
-- QUERY 6: SOCIOECONOMIC WEALTH VS. ART COVERAGE & MORTALITY (2025)
-- Describes same-year national GDP and ART coverage.
-- --------------------------------------------------------------------
SELECT 
    country_name,
    iso3,
    income_group,
    ROUND(gdp_per_capita_ppp, 0) AS gdp_pc_ppp_2021int_usd,
    ROUND(gdp_per_capita_usd, 0) AS gdp_pc_current_usd,
    art_coverage_pct,
    treatment_gap_pct,
    ROUND(mortality_rate_in_plhiv_pct, 2) AS mortality_rate_in_plhiv_pct,
    ROUND(aids_mortality_rate_per100k_pop, 2) AS mortality_per_100k_pop
FROM v_southeast_asia_surveillance
WHERE year = 2025
  AND is_southeast_asia = 1
  AND art_coverage_pct IS NOT NULL
ORDER BY gdp_pc_ppp_2021int_usd DESC;


-- --------------------------------------------------------------------
-- QUERY 7: LAGGED ART ASSOCIATION ON AIDS-RELATED MORTALITY (PANEL STRUCTURE)
-- Constructs 1-year and 2-year lagged ART coverage to analyze subsequent mortality.
-- --------------------------------------------------------------------
SELECT 
    v.country_name,
    v.iso3,
    v.year,
    v.art_coverage_pct AS art_cov_contemporaneous,
    LAG(v.art_coverage_pct, 1) OVER (PARTITION BY v.iso3 ORDER BY v.year) AS art_cov_lag1,
    LAG(v.art_coverage_pct, 2) OVER (PARTITION BY v.iso3 ORDER BY v.year) AS art_cov_lag2,
    v.aids_deaths,
    ROUND(v.mortality_rate_in_plhiv_pct, 2) AS mortality_rate_in_plhiv_pct,
    ROUND(v.aids_mortality_rate_per100k_pop, 2) AS mortality_per_100k_pop
FROM v_southeast_asia_surveillance v
WHERE v.is_southeast_asia = 1
  AND v.year >= 2010
ORDER BY v.iso3 ASC, v.year ASC;
