-- ====================================================================
-- 01_create_schema.sql
-- Database Schema for HIV Epidemiological Surveillance & Treatment Analytics
-- Target: SQLite 3 / DuckDB
-- ====================================================================

-- 1. Country Dimension Table
DROP TABLE IF EXISTS dim_country;
CREATE TABLE dim_country (
    iso3 VARCHAR(3) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    un_m49 VARCHAR(10),
    region VARCHAR(50),
    income_group VARCHAR(50),
    analysis_role VARCHAR(50),
    is_southeast_asia INTEGER NOT NULL DEFAULT 0,
    is_benchmark INTEGER NOT NULL DEFAULT 0
);

-- 2. Longitudinal HIV Epidemiological Estimates Fact Table (1990-2025)
DROP TABLE IF EXISTS fact_hiv_estimates;
CREATE TABLE fact_hiv_estimates (
    iso3 VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    plhiv DOUBLE,
    plhiv_low DOUBLE,
    plhiv_high DOUBLE,
    adult_prevalence_pct DOUBLE,
    adult_prevalence_low DOUBLE,
    adult_prevalence_high DOUBLE,
    aids_deaths DOUBLE,
    aids_deaths_low DOUBLE,
    aids_deaths_high DOUBLE,
    new_infections DOUBLE,
    new_infections_low DOUBLE,
    new_infections_high DOUBLE,
    incidence_rate_per1000 DOUBLE,
    incidence_rate_low DOUBLE,
    incidence_rate_high DOUBLE,
    PRIMARY KEY (iso3, year),
    FOREIGN KEY (iso3) REFERENCES dim_country(iso3)
);

-- 3. Treatment Cascade & 95-95-95 Fact Table (2010-2025)
DROP TABLE IF EXISTS fact_treatment_cascade;
CREATE TABLE fact_treatment_cascade (
    iso3 VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    diagnosed_1st95_pct DOUBLE,
    diagnosed_1st95_low DOUBLE,
    diagnosed_1st95_high DOUBLE,
    art_coverage_pct DOUBLE,
    art_coverage_low DOUBLE,
    art_coverage_high DOUBLE,
    on_art_2nd95_pct DOUBLE,
    on_art_2nd95_low DOUBLE,
    on_art_2nd95_high DOUBLE,
    virally_suppressed_3rd95_pct DOUBLE,
    virally_suppressed_3rd95_low DOUBLE,
    virally_suppressed_3rd95_high DOUBLE,
    virally_suppressed_all_pct DOUBLE,
    treatment_gap_pct DOUBLE,
    unreached_plhiv DOUBLE,
    PRIMARY KEY (iso3, year),
    FOREIGN KEY (iso3) REFERENCES dim_country(iso3)
);

-- 4. Socioeconomic & Demographic Fact Table (1990-2025)
DROP TABLE IF EXISTS fact_socioeconomic;
CREATE TABLE fact_socioeconomic (
    iso3 VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    gdp_per_capita_usd DOUBLE,
    gdp_per_capita_ppp DOUBLE,
    population_total DOUBLE,
    PRIMARY KEY (iso3, year),
    FOREIGN KEY (iso3) REFERENCES dim_country(iso3)
);

-- 5. Master Analytical View for Surveillance & Econometric Modeling
DROP VIEW IF EXISTS v_southeast_asia_surveillance;
CREATE VIEW v_southeast_asia_surveillance AS
SELECT 
    c.iso3,
    c.country_name,
    c.region,
    c.income_group,
    c.analysis_role,
    c.is_southeast_asia,
    c.is_benchmark,
    e.year,
    e.plhiv,
    e.adult_prevalence_pct,
    e.aids_deaths,
    e.new_infections,
    e.incidence_rate_per1000,
    t.art_coverage_pct,
    t.treatment_gap_pct,
    t.unreached_plhiv,
    t.diagnosed_1st95_pct,
    t.on_art_2nd95_pct,
    t.virally_suppressed_3rd95_pct,
    t.virally_suppressed_all_pct,
    s.gdp_per_capita_usd,
    s.gdp_per_capita_ppp,
    s.population_total,
    -- Derived Population-Adjusted Rates
    CASE 
        WHEN e.plhiv > 0 THEN (e.aids_deaths / e.plhiv) * 100.0 
        ELSE NULL 
    END AS mortality_rate_in_plhiv_pct,
    CASE 
        WHEN s.population_total > 0 THEN (e.aids_deaths / s.population_total) * 100000.0 
        ELSE NULL 
    END AS aids_mortality_rate_per100k_pop,
    CASE 
        WHEN e.aids_deaths > 0 THEN e.new_infections / e.aids_deaths 
        ELSE NULL 
    END AS incidence_to_mortality_ratio
FROM dim_country c
JOIN fact_hiv_estimates e ON c.iso3 = e.iso3
LEFT JOIN fact_treatment_cascade t ON c.iso3 = t.iso3 AND e.year = t.year
LEFT JOIN fact_socioeconomic s ON c.iso3 = s.iso3 AND e.year = s.year
WHERE c.is_southeast_asia = 1 OR c.is_benchmark = 1;
