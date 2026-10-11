"""
src/analysis/econometric_modeling.py
------------------------------------
Conducts econometric panel regressions with country fixed effects (Within transformation)
to estimate the lagged protective association of ART coverage expansion on AIDS-related
mortality across Southeast Asia (2010-2025).

Outputs:
  - reports/analysis_tables/panel_regression_models.csv
  - reports/analysis_tables/correlation_matrix.csv
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('EconometricModeling')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
OUTPUT_DIR = os.path.join(BASE_DIR, 'reports', 'analysis_tables')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Focus group excluding Brunei (suppressed)
SEA_REGRESSION_COUNTRIES = ['MMR', 'THA', 'VNM', 'KHM', 'IDN', 'MYS', 'PHL', 'LAO', 'TLS']

def run_econometric_analysis():
    logger.info("Loading Southeast Asia panel dataset (2010-2025) ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    
    # Filter to regression countries with valid mortality rates
    panel = df[df['iso3'].isin(SEA_REGRESSION_COUNTRIES)].copy()
    panel = panel.dropna(subset=['mortality_rate_in_plhiv_pct', 'art_coverage_pct']).sort_values(['iso3', 'year']).reset_index(drop=True)
    
    # Calculate log GDP
    panel['log_gdp_pc_ppp'] = np.log(panel['gdp_per_capita_ppp'])
    
    # 1. Correlation Matrix
    corr_cols = [
        'art_coverage_pct', 'art_coverage_lag1', 'art_coverage_lag2',
        'mortality_rate_in_plhiv_pct', 'aids_mortality_rate_per100k_pop',
        'aids_deaths', 'gdp_per_capita_ppp'
    ]
    corr_matrix = panel[corr_cols].corr().round(3)
    out_corr = os.path.join(OUTPUT_DIR, 'correlation_matrix.csv')
    corr_matrix.to_csv(out_corr)
    logger.info(f"Saved correlation matrix -> {out_corr}")
    print("\n--- Correlation Matrix (N = {}) ---".format(len(panel)))
    print(corr_matrix.to_string())
    
    # Helper for Fixed Effects (Within estimator / Mean-demeaning)
    def estimate_fe_model(data, y_col, x_cols, model_name):
        df_sub = data.dropna(subset=[y_col] + x_cols).copy()
        
        # Demean by country
        y_demeaned = df_sub[y_col] - df_sub.groupby('iso3')[y_col].transform('mean')
        
        X_demeaned = pd.DataFrame()
        for x in x_cols:
            X_demeaned[x] = df_sub[x] - df_sub.groupby('iso3')[x].transform('mean')
            
        X_demeaned = sm.add_constant(X_demeaned)
        ols_res = sm.OLS(y_demeaned, X_demeaned).fit(cov_type='HC1') # Robust SE
        
        results = []
        for x in x_cols:
            results.append({
                'model_name': model_name,
                'dependent_variable': y_col,
                'independent_variable': x,
                'coefficient': round(ols_res.params[x], 4),
                'robust_std_err': round(ols_res.bse[x], 4),
                't_statistic': round(ols_res.tvalues[x], 3),
                'p_value': round(ols_res.pvalues[x], 5),
                'ci_lower_95': round(ols_res.conf_int().loc[x, 0], 4),
                'ci_upper_95': round(ols_res.conf_int().loc[x, 1], 4),
                'r_squared_within': round(ols_res.rsquared, 4),
                'n_observations': int(ols_res.nobs),
                'n_countries': int(df_sub['iso3'].nunique())
            })
        return results, ols_res

    # 2. Run 4 Regression Specifications
    logger.info("Fitting Fixed Effects Panel Regressions ...")
    all_results = []
    
    # Model 1: Contemporaneous ART
    res1, m1 = estimate_fe_model(panel, 'mortality_rate_in_plhiv_pct', ['art_coverage_pct'], 'Model 1: Contemporaneous ART')
    all_results.extend(res1)
    
    # Model 2: 1-Year Lagged ART
    res2, m2 = estimate_fe_model(panel, 'mortality_rate_in_plhiv_pct', ['art_coverage_lag1'], 'Model 2: 1-Year Lagged ART')
    all_results.extend(res2)
    
    # Model 3: 2-Year Lagged ART
    res3, m3 = estimate_fe_model(panel, 'mortality_rate_in_plhiv_pct', ['art_coverage_lag2'], 'Model 3: 2-Year Lagged ART')
    all_results.extend(res3)
    
    # Model 4: 1-Year Lagged ART + Log GDP per capita
    res4, m4 = estimate_fe_model(panel, 'mortality_rate_in_plhiv_pct', ['art_coverage_lag1', 'log_gdp_pc_ppp'], 'Model 4: Lagged ART + Macroeconomic Control')
    all_results.extend(res4)
    
    results_df = pd.DataFrame(all_results)
    out_models = os.path.join(OUTPUT_DIR, 'panel_regression_models.csv')
    results_df.to_csv(out_models, index=False)
    logger.info(f"Saved regression models table -> {out_models}")
    
    # Save demeaned dataset for Model 2 visualization
    df_m2 = panel.dropna(subset=['mortality_rate_in_plhiv_pct', 'art_coverage_lag1']).copy()
    df_m2['mortality_rate_demeaned'] = df_m2['mortality_rate_in_plhiv_pct'] - df_m2.groupby('iso3')['mortality_rate_in_plhiv_pct'].transform('mean')
    df_m2['art_lag1_demeaned'] = df_m2['art_coverage_lag1'] - df_m2.groupby('iso3')['art_coverage_lag1'].transform('mean')
    out_demeaned = os.path.join(OUTPUT_DIR, 'panel_fe_demeaned_model2.csv')
    df_m2.to_csv(out_demeaned, index=False)
    
    print("\n--- Fixed Effects Regression Results (DV: Mortality Rate in PLHIV %) ---")
    print(results_df[['model_name', 'independent_variable', 'coefficient', 'robust_std_err', 't_statistic', 'p_value', 'r_squared_within', 'n_observations']].to_string(index=False))
    
    m2_beta = res2[0]['coefficient']
    m2_p = res2[0]['p_value']
    # Clinical and Epidemiological Interpretation Note
    logger.info("\nSummary of Epidemiological Interpretation:")
    logger.info(f"In Model 2 (1-Year Lag), beta = {m2_beta:.4f} (p = {m2_p:.5f}, N = {res2[0]['n_observations']}).")
    logger.info("Interpretation: For every 10 percentage point increase in national ART coverage in year (t-1),")
    logger.info(f"the mortality rate among people living with HIV decreases by ~{abs(m2_beta)*10:.2f} percentage points in year (t).")
    
    return results_df, corr_matrix

if __name__ == '__main__':
    run_econometric_analysis()
