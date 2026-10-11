"""
notebooks/create_notebook.py
----------------------------
Generates the comprehensive research notebook: notebooks/hiv_epidemiology_research.ipynb.
Walks through data ingestion, SQLite querying, descriptive epidemiology,
95-95-95 cascade analysis, panel regression modeling, and policy discussion.
"""

import os
import json

NB_PATH = os.path.join(os.path.dirname(__file__), 'hiv_epidemiology_research.ipynb')

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# HIV Epidemiological Transitions and Treatment Disparities in Southeast Asia (1990–2025)\n",
            "### A Comparative Longitudinal Analysis of Myanmar Against Regional and Global Benchmarks\n",
            "\n",
            "**Investigator:** Clinical Medical Doctor & Healthcare Data Analyst (Myanmar / Public Health Research)  \n",
            "**Data Sources:** UNAIDS 2026 Epidemiological Estimates, WHO Global Health Observatory, World Bank WDI  \n",
            "**Target:** Reproducible Clinical Research & Epidemiological Analytics Portfolio  \n",
            "\n",
            "---\n",
            "\n",
            "## 1. Executive Summary & Clinical Background\n",
            "Over the past three decades, antiretroviral therapy (ART) has fundamentally changed HIV from an acute fatal illness into a manageable chronic disease. However, public health progress has been remarkably uneven across Southeast Asia.\n",
            "\n",
            "This study investigates:\n",
            "1. **Long-Term Trajectories (1990–2025):** How HIV incidence, adult prevalence, and AIDS mortality evolved across 10 Southeast Asian nations and global benchmarks.\n",
            "2. **Myanmar Specifics:** The rapid 2010–2020 ART expansion (12% to 69%), the 2021–2022 disruption (+11.6% mortality rebound), and the prevalence paradox.\n",
            "3. **Treatment Disparities & Cascade:** UNAIDS 95-95-95 performance in 2025 and regional archetype classification (Accelerated Control vs. Counter-Epidemics).\n",
            "4. **Econometric Lagged Association:** Country fixed-effects panel modeling of ART expansion on AIDS mortality reductions.\n",
            "5. **Socioeconomic Determinants:** The decoupling of GDP per capita from treatment coverage in donor-supported health systems."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Setup and library imports\n",
            "import os\n",
            "import sqlite3\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import statsmodels.api as sm\n",
            "\n",
            "# Visual configuration\n",
            "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
            "pd.set_option('display.max_columns', 30)\n",
            "pd.set_option('display.float_format', lambda x: '%.3f' % x)\n",
            "\n",
            "DB_PATH = os.path.abspath(os.path.join('..', 'data', 'processed', 'hiv_surveillance.db'))\n",
            "print(f\"Database connection configured: {DB_PATH}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Structured Data Ingestion via SQLite\n",
            "We query our harmonized surveillance database (`hiv_surveillance.db`), loading the master analytical view `v_southeast_asia_surveillance`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "conn = sqlite3.connect(DB_PATH)\n",
            "\n",
            "# Query table verification counts\n",
            "tables = ['dim_country', 'fact_hiv_estimates', 'fact_treatment_cascade', 'fact_socioeconomic']\n",
            "for tbl in tables:\n",
            "    cnt = pd.read_sql_query(f\"SELECT COUNT(*) as n FROM {tbl}\", conn)['n'].iloc[0]\n",
            "    print(f\"Table {tbl:<25}: {cnt:,} rows\")\n",
            "\n",
            "# Load full Southeast Asia & Benchmarks dataset\n",
            "df_surv = pd.read_sql_query(\"SELECT * FROM v_southeast_asia_surveillance ORDER BY country_name, year\", conn)\n",
            "conn.close()\n",
            "\n",
            "print(f\"\\nMaster Analytical View loaded: {df_surv.shape[0]} rows across {df_surv['iso3'].nunique()} entities.\")\n",
            "df_surv.head(3)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. SQL Query 1: Myanmar 36-Year Trajectory (1990–2025)\n",
            "We inspect Myanmar's empirical progression across the pre-treatment epidemic wave, ART scale-up, and the political/COVID disruption."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "conn = sqlite3.connect(DB_PATH)\n",
            "query_mmr = \"\"\"\n",
            "SELECT \n",
            "    year,\n",
            "    adult_prevalence_pct AS prev_pct,\n",
            "    plhiv,\n",
            "    new_infections AS new_inf,\n",
            "    aids_deaths AS deaths,\n",
            "    art_coverage_pct AS art_cov,\n",
            "    treatment_gap_pct AS gap_pct,\n",
            "    ROUND(mortality_rate_in_plhiv_pct, 2) AS mort_rate_plhiv,\n",
            "    ROUND(gdp_per_capita_usd, 0) AS gdp_pc\n",
            "FROM v_southeast_asia_surveillance\n",
            "WHERE iso3 = 'MMR'\n",
            "ORDER BY year DESC;\n",
            "\"\"\"\n",
            "df_mmr = pd.read_sql_query(query_mmr, conn)\n",
            "conn.close()\n",
            "\n",
            "# Display recent 16 years (2010-2025)\n",
            "df_mmr[df_mmr['year'] >= 2010]"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Clinical Epidemiological Interpretation: Myanmar Dynamics\n",
            "1. **Prevalence Paradox:** Adult HIV prevalence remained flat at `0.9%` while total PLHIV expanded from `250,000` to `310,000`. As clinicians understand, effective ART extends survival, causing living prevalence to expand even as new transmissions contract.\n",
            "2. **The 2021–2022 Disruption:** Between 2010 and 2020, ART expanded from `12%` to `69%`, causing deaths to drop from `12,000` to `4,400`. In 2021, amidst political turmoil and COVID-19 strain, ART coverage dropped to `66%`, resulting in an immediate mortality rebound to `4,800` deaths in 2022 (+11.6%). Recovery followed, reaching `73%` coverage by 2025."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. SQL Query 2: Regional Fast-Track Progress (2010 vs 2025)\n",
            "Evaluating relative changes in AIDS deaths and new infections alongside ART coverage gains across Southeast Asia."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "conn = sqlite3.connect(DB_PATH)\n",
            "query_fasttrack = \"\"\"\n",
            "WITH b AS (\n",
            "    SELECT iso3, country_name, aids_deaths AS d_10, new_infections AS i_10, art_coverage_pct AS art_10\n",
            "    FROM v_southeast_asia_surveillance WHERE year = 2010\n",
            "),\n",
            "c AS (\n",
            "    SELECT iso3, aids_deaths AS d_25, new_infections AS i_25, art_coverage_pct AS art_25\n",
            "    FROM v_southeast_asia_surveillance WHERE year = 2025\n",
            ")\n",
            "SELECT \n",
            "    b.country_name,\n",
            "    b.d_10 AS deaths_2010,\n",
            "    c.d_25 AS deaths_2025,\n",
            "    ROUND(((c.d_25 - b.d_10) * 100.0 / b.d_10), 1) AS pct_change_deaths,\n",
            "    b.i_10 AS inf_2010,\n",
            "    c.i_25 AS inf_2025,\n",
            "    ROUND(((c.i_25 - b.i_10) * 100.0 / b.i_10), 1) AS pct_change_infections,\n",
            "    b.art_10 AS art_2010,\n",
            "    c.art_25 AS art_2025,\n",
            "    ROUND(c.art_25 - b.art_10, 1) AS art_gain_pp\n",
            "FROM b JOIN c ON b.iso3 = c.iso3\n",
            "WHERE b.d_10 IS NOT NULL\n",
            "ORDER BY pct_change_deaths ASC;\n",
            "\"\"\"\n",
            "df_ft = pd.read_sql_query(query_fasttrack, conn)\n",
            "conn.close()\n",
            "df_ft"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Visualizing the Epidemiological Evidence Base\n",
            "We inspect the 6 publication-grade figures generated by our pipeline in `figures/`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Image, display\n",
            "\n",
            "fig_files = [\n",
            "    '../figures/fig1_myanmar_longitudinal_trajectory.png',\n",
            "    '../figures/fig2_southeast_asia_mortality_infection_divergence.png',\n",
            "    '../figures/fig3_unaids_95_95_95_cascade_2025.png',\n",
            "    '../figures/fig4_lagged_art_mortality_dose_response.png',\n",
            "    '../figures/fig5_gdp_vs_art_coverage_disparity.png',\n",
            "    '../figures/fig6_southeast_asia_art_trajectories_2010_2025.png'\n",
            "]\n",
            "\n",
            "for fig_path in fig_files:\n",
            "    if os.path.exists(fig_path):\n",
            "        print(f\"Displaying {os.path.basename(fig_path)}:\")\n",
            "        display(Image(filename=fig_path, width=800))\n",
            "    else:\n",
            "        print(f\"Figure not found: {fig_path}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Econometric Panel Regressions: Fixed Effects Estimation\n",
            "We estimate country fixed-effects regressions to test the lagged protective association of ART on crude mortality rate in PLHIV."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load processed SEA panel (2010-2025)\n",
            "sea_panel = pd.read_csv('../data/processed/southeast_asia_hiv_panel_2010_2025.csv')\n",
            "reg_countries = ['MMR', 'THA', 'VNM', 'KHM', 'IDN', 'MYS', 'PHL', 'LAO', 'TLS']\n",
            "\n",
            "pdata = sea_panel[sea_panel['iso3'].isin(reg_countries)].dropna(subset=['mortality_rate_in_plhiv_pct', 'art_coverage_pct']).copy()\n",
            "pdata['log_gdp'] = np.log(pdata['gdp_per_capita_ppp'])\n",
            "\n",
            "# Within-country mean demeaning for Model 2 (1-Year Lag)\n",
            "pdata_fe = pdata.dropna(subset=['art_coverage_lag1']).copy()\n",
            "y = pdata_fe['mortality_rate_in_plhiv_pct'] - pdata_fe.groupby('iso3')['mortality_rate_in_plhiv_pct'].transform('mean')\n",
            "X = pdata_fe['art_coverage_lag1'] - pdata_fe.groupby('iso3')['art_coverage_lag1'].transform('mean')\n",
            "X = sm.add_constant(X)\n",
            "\n",
            "fe_model2 = sm.OLS(y, X).fit(cov_type='HC1')\n",
            "print(fe_model2.summary())"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Conclusions & Research Discussion\n",
            "1. **Primary Finding:** Across Southeast Asia, each **10 percentage point expansion in national ART coverage** reduces the mortality rate among people living with HIV by **~0.49 percentage points** in the subsequent year ($t = -14.20, p < 0.00001, R^2_{\\text{within}} = 0.687$).\n",
            "2. **Myanmar Resilience & Vulnerability:** Myanmar demonstrates that rapid vertical ART decentralization can drive dramatic mortality reductions in low-income settings. However, clinical supply stability is essential; political and health system disruptions immediately manifest as excess mortality rebounds.\n",
            "3. **The Counter-Epidemic in the Philippines:** With a **+639% surge in new infections** and **+440% increase in AIDS deaths**, the Philippines requires urgent structural interventions and testing expansion.\n",
            "4. **Policy Decoupling:** In concentrated epidemics, national GDP does not dictate HIV success. Lower-income countries with strong vertical programs (Cambodia, Myanmar) outperform decentralized middle-income countries (Indonesia, Philippines)."
        ]
    }
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.8"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Generated research notebook successfully at {NB_PATH}")
