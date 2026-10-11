"""
src/visualization/generate_figures.py
-------------------------------------
Generates high-resolution, publication-grade epidemiological figures for the research report,
presentations, and portfolio deliverables.

Figures Generated:
  1. figures/fig1_myanmar_longitudinal_trajectory.png (1990-2025 with uncertainty bounds)
  2. figures/fig2_southeast_asia_mortality_infection_divergence.png (2010 vs 2025 relative changes)
  3. figures/fig3_unaids_95_95_95_cascade_2025.png (Testing, treatment, suppression & gaps)
  4. figures/fig4_lagged_art_mortality_dose_response.png (2-panel: Raw Trajectories + Within FE Fit)
  5. figures/fig5_gdp_vs_art_coverage_disparity.png (Macroeconomic wealth vs coverage)
  6. figures/fig6_southeast_asia_art_trajectories_2010_2025.png (16-year ART scale-up curves)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('FigureGenerator')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
TABLES_DIR = os.path.join(BASE_DIR, 'reports', 'analysis_tables')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['grid.color'] = '#E2E8F0'
plt.rcParams['grid.linestyle'] = '--'


def generate_figure_1():
    """Figure 1: Long-Term Epidemiological Trajectory of Myanmar (1990-2025)."""
    logger.info("Generating Figure 1: Myanmar Longitudinal Trajectory ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_longitudinal_1990_2025.csv'))
    mmr = df[df['iso3'] == 'MMR'].sort_values('year').copy()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 9.2), sharex=True)
    
    # Panel A: Prevalence and PLHIV
    color_prev = '#C0392B'   # Crimson
    color_plhiv = '#1F618D'  # Deep Navy Blue
    
    ax1.plot(mmr['year'], mmr['adult_prevalence_pct'], color=color_prev, linewidth=2.6,
             label='Adult Prevalence (Ages 15–49, %)')
    ax1.fill_between(mmr['year'], mmr['adult_prevalence_low'], mmr['adult_prevalence_high'],
                     color=color_prev, alpha=0.18, label='Prevalence 95% UI')
    ax1.set_ylabel('Adult HIV Prevalence (%)', color=color_prev, fontsize=11, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_prev, labelsize=10)
    ax1.set_ylim(0, 1.45)
    
    # Twin axis for PLHIV
    ax1_twin = ax1.twinx()
    ax1_twin.plot(mmr['year'], mmr['plhiv'] / 1000.0, color=color_plhiv, linewidth=2.6, linestyle='--',
                  label='Total PLHIV (Thousands)')
    ax1_twin.fill_between(mmr['year'], mmr['plhiv_low'] / 1000.0, mmr['plhiv_high'] / 1000.0,
                          color=color_plhiv, alpha=0.14, label='PLHIV 95% UI')
    ax1_twin.set_ylabel('People Living with HIV (Thousands)', color=color_plhiv, fontsize=11, fontweight='bold')
    ax1_twin.tick_params(axis='y', labelcolor=color_plhiv, labelsize=10)
    ax1_twin.grid(False)
    ax1_twin.set_ylim(0, 420)
    
    ax1.set_title('A. Adult HIV Prevalence vs. Expanding Living Cohort (The Survival-Driven Prevalence Paradox)',
                  fontsize=12, fontweight='bold', loc='left', pad=8)
    
    # Combined legend for Panel A
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', ncol=2, frameon=True, framealpha=0.95, fontsize=9.5)
    
    # Panel B: Incidence vs AIDS Deaths & ART Scale-up
    color_inf = '#D35400'    # Burnt Orange
    color_deaths = '#6C3483' # Royal Purple
    
    ax2.plot(mmr['year'], mmr['new_infections'] / 1000.0, color=color_inf, linewidth=2.6,
             label='New HIV Infections (Thousands)')
    ax2.fill_between(mmr['year'], mmr['new_infections_low'] / 1000.0, mmr['new_infections_high'] / 1000.0,
                     color=color_inf, alpha=0.18, label='New Infections 95% UI')
    
    ax2.plot(mmr['year'], mmr['aids_deaths'] / 1000.0, color=color_deaths, linewidth=2.6,
             label='AIDS-Related Deaths (Thousands)')
    ax2.fill_between(mmr['year'], mmr['aids_deaths_low'] / 1000.0, mmr['aids_deaths_high'] / 1000.0,
                     color=color_deaths, alpha=0.18, label='AIDS Deaths 95% UI')
    
    ax2.set_ylabel('Annual Events (Thousands)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Calendar Year', fontsize=11, fontweight='bold')
    ax2.tick_params(axis='both', labelsize=10)
    ax2.set_xlim(1990, 2025)
    ax2.set_ylim(0, 30)
    ax2.set_title('B. Annual Incident HIV Infections vs. AIDS-Related Deaths (1990–2025)',
                  fontsize=12, fontweight='bold', loc='left', pad=8)
    
    # Annotate key public health milestones
    ax2.annotate('Rapid ART Scale-Up\n(Coverage: 12% in 2010 -> 69% in 2020)',
                 xy=(2015, 7.8), xytext=(2006.5, 19.5),
                 arrowprops=dict(facecolor='#333333', arrowstyle='->', lw=1.3),
                 fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#FEF9E7', edgecolor='#F39C12', alpha=0.95))
    
    ax2.annotate('2021 ART Dip (69% -> 66%) &\n2022 Mortality Rebound (+11.6%)',
                 xy=(2022, 4.8), xytext=(2012.0, 1.6),
                 arrowprops=dict(facecolor='#C0392B', arrowstyle='->', lw=1.3),
                 fontsize=9.5, fontweight='bold', color='#78281F',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.95))
    
    ax2.legend(loc='upper right', ncol=2, frameon=True, framealpha=0.95, fontsize=9.5)
    
    fig.suptitle('FIGURE 1: 36-Year Epidemiological Trajectory of HIV in Myanmar (1990–2025)\nData Source: UNAIDS 2026 Epidemiological Estimates (Solid/Dashed Lines = Point Estimates; Shaded Bands = 95% UI)', 
                 fontsize=12.5, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = os.path.join(FIGURES_DIR, 'fig1_myanmar_longitudinal_trajectory.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 1 -> {out_path}")


def generate_figure_2():
    """Figure 2: Fast-Track Regional Divergence in Southeast Asia (2010 vs 2025)."""
    logger.info("Generating Figure 2: Regional Mortality and Infection Divergence ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    
    # Focus countries with complete non-suppressed estimates
    focus_iso = ['THA', 'MMR', 'KHM', 'MYS', 'VNM', 'LAO', 'TLS', 'IDN', 'PHL']
    d10 = df[(df['year'] == 2010) & (df['iso3'].isin(focus_iso))].set_index('iso3')
    d25 = df[(df['year'] == 2025) & (df['iso3'].isin(focus_iso))].set_index('iso3')
    
    data = []
    for iso in focus_iso:
        cname = d10.loc[iso, 'country_name']
        d_chg = (d25.loc[iso, 'aids_deaths'] - d10.loc[iso, 'aids_deaths']) / d10.loc[iso, 'aids_deaths'] * 100.0
        i_chg = (d25.loc[iso, 'new_infections'] - d10.loc[iso, 'new_infections']) / d10.loc[iso, 'new_infections'] * 100.0
        art_gain = d25.loc[iso, 'art_coverage_pct'] - d10.loc[iso, 'art_coverage_pct']
        data.append({'country': cname, 'pct_deaths': d_chg, 'pct_inf': i_chg, 'art_gain': art_gain})
        
    div_df = pd.DataFrame(data).sort_values('pct_deaths')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.2), sharey=True)
    
    y_pos = np.arange(len(div_df))
    colors_deaths = ['#1E8449' if x < 0 else ('#7F8C8D' if x == 0 else '#C0392B') for x in div_df['pct_deaths']]
    colors_inf = ['#2471A3' if x < 0 else ('#7F8C8D' if x == 0 else '#D35400') for x in div_df['pct_inf']]
    
    # Subplot 1: AIDS Deaths Change
    bars1 = ax1.barh(y_pos, div_df['pct_deaths'], color=colors_deaths, alpha=0.88, height=0.62)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(div_df['country'], fontsize=11, fontweight='bold')
    ax1.axvline(0, color='#333333', linewidth=1.1)
    ax1.axvline(-56.2, color='#2C3E50', linestyle=':', linewidth=1.3, label='Global Benchmark (-56.2%)')
    ax1.set_xlabel('% Change in AIDS-Related Deaths (2010 to 2025)', fontsize=11, fontweight='bold')
    ax1.set_title('A. Relative Change in Annual AIDS-Related Deaths\n(Green = Reduction; Red = Mortality Expansion)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    ax1.set_xlim(-155, 530)
    ax1.legend(loc='lower right', frameon=True, fontsize=9.5)
    
    for bar in bars1:
        w = bar.get_width()
        y_center = bar.get_y() + bar.get_height() / 2
        if w < 0:
            ax1.text(w - 8, y_center, f"{w:+.1f}%", va='center', ha='right', fontsize=9.5, fontweight='bold', color='#145A32')
        elif w == 0:
            ax1.text(8, y_center, "0.0%", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#555555')
        else:
            ax1.text(w + 8, y_center, f"{w:+.1f}%", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#922B21')
            
    # Subplot 2: New Infections Change
    bars2 = ax2.barh(y_pos, div_df['pct_inf'], color=colors_inf, alpha=0.88, height=0.62)
    ax2.axvline(0, color='#333333', linewidth=1.1)
    ax2.axvline(-42.9, color='#2C3E50', linestyle=':', linewidth=1.3, label='Global Benchmark (-42.9%)')
    ax2.set_xlabel('% Change in Annual New HIV Infections (2010 to 2025)', fontsize=11, fontweight='bold')
    ax2.set_title('B. Relative Change in Annual New HIV Infections\n(Blue = Reduction; Orange = Incidence Resurgence)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    ax2.set_xlim(-175, 750)
    ax2.legend(loc='lower right', frameon=True, fontsize=9.5)
    
    for bar in bars2:
        w = bar.get_width()
        y_center = bar.get_y() + bar.get_height() / 2
        if w < 0:
            ax2.text(w - 10, y_center, f"{w:+.1f}%", va='center', ha='right', fontsize=9.5, fontweight='bold', color='#1B4F72')
        elif w == 0:
            ax2.text(10, y_center, "0.0%", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#555555')
        else:
            ax2.text(w + 10, y_center, f"{w:+.1f}%", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#935116')
            
    fig.suptitle('FIGURE 2: Regional Divergence in HIV Outcomes Across Southeast Asia (2010–2025)\nContrasting Rapid Epidemic Control (Thailand, Myanmar, Cambodia) vs. Resurgence (Philippines, Indonesia)', 
                 fontsize=12.5, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, 'fig2_southeast_asia_mortality_infection_divergence.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 2 -> {out_path}")


def generate_figure_3():
    """Figure 3: Treatment Gaps and Cascade Performance in Southeast Asia (2025)."""
    logger.info("Generating Figure 3: Cascade and Treatment Gaps ...")
    casc = pd.read_csv(os.path.join(TABLES_DIR, 'cascade_2025_summary.csv'))
    
    # Focus countries
    focus_iso = ['KHM', 'THA', 'VNM', 'MMR', 'TLS', 'LAO', 'MYS', 'IDN', 'PHL']
    casc_sub = casc[casc['iso3'].isin(focus_iso)].sort_values('art_coverage_pct', ascending=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 7.6))
    
    # Subplot 1: Grouped Cascade Bars (1st, 2nd, 3rd 95)
    y_pos = np.arange(len(casc_sub))
    bar_width = 0.25
    
    ax1.barh(y_pos + bar_width, casc_sub['diagnosed_1st95_pct'], height=bar_width,
             color='#2980B9', label='1st 95: % Diagnosed among PLHIV')
    ax1.barh(y_pos, casc_sub['on_art_2nd95_pct'], height=bar_width,
             color='#27AE60', label='2nd 95: % on ART among Diagnosed')
    ax1.barh(y_pos - bar_width, casc_sub['virally_suppressed_3rd95_pct'], height=bar_width,
             color='#8E44AD', label='3rd 95: % Suppressed among on ART')
    
    ax1.axvline(95, color='#C0392B', linestyle='--', linewidth=1.6, label='95% UNAIDS Fast-Track Target')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(casc_sub['country_name'], fontsize=11, fontweight='bold')
    ax1.set_xlabel('Cascade Step Achievement (%)', fontsize=11, fontweight='bold')
    ax1.set_xlim(0, 106)
    ax1.set_title('A. Progress Toward UNAIDS 95-95-95 Cascade Targets (2025)\n(Note: Cambodia >98% on 2nd/3rd 95; Thailand >98% on 3rd 95)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=2, frameon=True, fontsize=9.5)
    
    # Subplot 2: Unreached Treatment Gap Burden (Count)
    gaps = pd.read_csv(os.path.join(TABLES_DIR, 'treatment_gaps_2025.csv')).sort_values('unreached_plhiv', ascending=True)
    y_pos2 = np.arange(len(gaps))
    
    bars_gap = ax2.barh(y_pos2, gaps['unreached_plhiv'] / 1000.0, color='#C0392B', alpha=0.88, height=0.6)
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(gaps['country_name'], fontsize=11, fontweight='bold')
    ax2.set_xlabel('Unreached PLHIV Not on ART (Thousands)', fontsize=11, fontweight='bold')
    ax2.set_title('B. Absolute Treatment Gap Burden (Untreated PLHIV, 2025)\n(Total Regional Unreached Cohort = 745,778 PLHIV)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    
    for bar, pct in zip(bars_gap, gaps['treatment_gap_pct']):
        w = bar.get_width()
        ax2.text(w + 5, bar.get_y() + bar.get_height()/2, f"{w:.1f}k ({pct:.0f}% Gap)",
                 va='center', ha='left', fontsize=9.5, fontweight='bold', color='#641E16')
        
    ax2.set_xlim(0, 365)
    
    fig.suptitle('FIGURE 3: HIV Treatment Cascade Performance and Disparity Landscape in Southeast Asia (2025)\nHighlighting Stark Service Delivery Divergences and Concentrated Unreached Burdens in Indonesia & Philippines', 
                 fontsize=12.5, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0.06, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, 'fig3_unaids_95_95_95_cascade_2025.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 3 -> {out_path}")


def generate_figure_4():
    """Figure 4: Econometric Panel Fit: Raw Trajectories vs Within Fixed-Effects Demeaned Slope."""
    logger.info("Generating Figure 4: Econometric Panel Dose-Response (2-Panel) ...")
    from matplotlib.lines import Line2D
    df_m2 = pd.read_csv(os.path.join(TABLES_DIR, 'panel_fe_demeaned_model2.csv'))
    
    focus_iso = ['THA', 'MMR', 'KHM', 'MYS', 'VNM', 'LAO', 'TLS', 'IDN', 'PHL']
    df_m2 = df_m2[df_m2['iso3'].isin(focus_iso)].sort_values(['country_name', 'year']).copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 7.0))
    palette = sns.color_palette('tab10', n_colors=len(focus_iso))
    countries = sorted(df_m2['country_name'].unique())
    color_map = dict(zip(countries, palette))
    
    # Panel A: Raw Country Trajectories (2011-2025)
    for cname in countries:
        sub = df_m2[df_m2['country_name'] == cname].sort_values('year')
        ax1.plot(sub['art_coverage_lag1'], sub['mortality_rate_in_plhiv_pct'],
                 color=color_map[cname], linewidth=1.8, alpha=0.75)
        ax1.scatter(sub['art_coverage_lag1'], sub['mortality_rate_in_plhiv_pct'],
                    color=color_map[cname], s=45, alpha=0.9, label=cname)
        # Mark 2025 endpoint with larger bordered circle
        last = sub.iloc[-1]
        ax1.scatter(last['art_coverage_lag1'], last['mortality_rate_in_plhiv_pct'],
                    color=color_map[cname], s=95, edgecolor='#111111', linewidth=1.1, zorder=5)
        
    ax1.set_title('A. Raw Country Longitudinal Trajectories (2011–2025)\n(Illustrating Baseline Heterogeneity Across National Epidemics)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    ax1.set_xlabel('1-Year Lagged ART Coverage (% of PLHIV on ART in Year t-1)', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel('AIDS Mortality Rate Among PLHIV (% in Year t)', fontsize=10.5, fontweight='bold')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 7.2)
    ax1.annotate('Philippines: Young Newly-Infected Cohort\n(Low Baseline Mortality Despite Low ART)',
                 xy=(38, 0.9), xytext=(8, 0.25),
                 arrowprops=dict(facecolor='#555555', arrowstyle='->', lw=1.1),
                 fontsize=8.8, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#F8F9F9', edgecolor='#BDC3C7', alpha=0.92))
    
    # Panel B: Country Fixed-Effects Within Transformation (Demeaned)
    for cname in countries:
        sub = df_m2[df_m2['country_name'] == cname]
        ax2.scatter(sub['art_lag1_demeaned'], sub['mortality_rate_demeaned'],
                    color=color_map[cname], s=50, alpha=0.85, label=cname)
        
    sns.regplot(
        data=df_m2,
        x='art_lag1_demeaned',
        y='mortality_rate_demeaned',
        scatter=False,
        ax=ax2,
        color='#C0392B',
        line_kws={'linewidth': 2.6, 'linestyle': '--'}
    )
    ax2.axhline(0, color='#7F8C8D', linestyle=':', linewidth=1.0)
    ax2.axvline(0, color='#7F8C8D', linestyle=':', linewidth=1.0)
    ax2.set_title('B. Within-Country Fixed-Effects Transformation (N = 135)\n(Controlling for Unobserved Time-Invariant Country Confounders)',
                  fontsize=11.5, fontweight='bold', loc='left', pad=8)
    ax2.set_xlabel('Country-Demeaned Lagged ART Coverage (Percentage Points, t-1)', fontsize=10.5, fontweight='bold')
    ax2.set_ylabel('Country-Demeaned Mortality Rate in PLHIV (Percentage Points, t)', fontsize=10.5, fontweight='bold')
    
    # Add regression summary box inside Panel B
    stats_box = (
        "Model 2: Within Fixed-Effects OLS\n"
        "• Slope (β): -0.0491 (Robust SE = 0.0035)\n"
        "• t-stat = -14.202 | p < 0.00001\n"
        "• Within R² = 0.6874 (N = 135, 9 Countries)\n"
        "• Effect: +10 pp ART -> -0.49 pp Mortality"
    )
    ax2.text(0.03, 0.05, stats_box, transform=ax2.transAxes, fontsize=9.2, fontweight='bold',
             verticalalignment='bottom', horizontalalignment='left',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF9E7', edgecolor='#F39C12', alpha=0.95))
    
    # Shared legend at bottom including explicit FE slope line handle
    handles, labels = ax2.get_legend_handles_labels()
    fe_line = Line2D([0], [0], color='#C0392B', linewidth=2.6, linestyle='--',
                     label='Within FE Slope (β = -0.0491)')
    handles.append(fe_line)
    labels.append('Within FE Slope (β = -0.0491)')
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.01),
               ncol=5, frameon=True, fontsize=9.5)
    
    fig.suptitle('FIGURE 4: Lagged Dose-Response Relationship Between ART Expansion and AIDS Mortality (2011–2025)\nPanel A: Unadjusted Longitudinal Country Paths | Panel B: Country Fixed-Effects Within-Estimator Fit',
                 fontsize=12.5, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0.08, 1, 0.94])
    out_path = os.path.join(FIGURES_DIR, 'fig4_lagged_art_mortality_dose_response.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 4 -> {out_path}")


def generate_figure_5():
    """Figure 5: Macroeconomic Wealth vs Epidemic Control (GDP vs ART Coverage)."""
    logger.info("Generating Figure 5: GDP vs ART Coverage Disparity ...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    d25 = df[df['year'] == 2025].dropna(subset=['gdp_per_capita_ppp', 'art_coverage_pct']).copy()
    
    fig, ax = plt.subplots(figsize=(11.2, 7.2))
    
    scatter = ax.scatter(
        d25['gdp_per_capita_ppp'],
        d25['art_coverage_pct'],
        s=np.maximum(d25['plhiv'] / 450.0, 90), # ensure small cohorts like TLS remain visible
        c=d25['treatment_gap_pct'],
        cmap='RdYlGn_r',
        vmin=0,
        vmax=65,
        alpha=0.9,
        edgecolors='#222222',
        linewidth=1.4,
        zorder=4
    )
    
    cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
    cbar.set_label('Treatment Gap (% of PLHIV Untreated)', fontsize=11, fontweight='bold')
    
    # Custom non-overlapping label offsets (in offset points)
    offsets = {
        'KHM': (12, -2),
        'THA': (-20, 14),
        'VNM': (16, -6),
        'MMR': (16, -2),
        'TLS': (12, -4),
        'LAO': (12, -4),
        'MYS': (-14, 14),
        'IDN': (22, 6),
        'PHL': (16, -12)
    }
    ha_map = {
        'THA': 'right',
        'MYS': 'right'
    }
    
    for _, r in d25.iterrows():
        iso = r['iso3']
        dx, dy = offsets.get(iso, (10, 6))
        ha_val = ha_map.get(iso, 'left')
        label_txt = f"{r['country_name']}\n({r['art_coverage_pct']:.0f}% ART | ${r['gdp_per_capita_ppp']:,.0f})"
        ax.annotate(
            label_txt,
            xy=(r['gdp_per_capita_ppp'], r['art_coverage_pct']),
            xytext=(dx, dy),
            textcoords='offset points',
            ha=ha_val,
            va='center',
            fontsize=9.2,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.92, edgecolor='#CCCCCC'),
            zorder=5
        )
        
    ax.axhline(80, color='#1E8449', linestyle='--', linewidth=1.5, label='80% High-Coverage Benchmark')
    ax.axhline(78, color='#2874A6', linestyle=':', linewidth=1.4, label='Global Average ART Coverage (78%)')
    ax.axvline(15000, color='#7F8C8D', linestyle=':', linewidth=1.3, label='Regional Mid-Income Reference ($15,000 PPP)')
    
    ax.set_xscale('log')
    ax.set_xlim(3200, 52000)
    ax.set_ylim(32, 103)
    
    # Clean currency formatting on log x-axis without scientific notation
    xticks = [4000, 6000, 10000, 15000, 25000, 40000]
    ax.set_xticks(xticks)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.get_xaxis().set_minor_formatter(ticker.NullFormatter())
    ax.tick_params(axis='both', labelsize=10)
    
    ax.set_title('FIGURE 5: National Macroeconomic Wealth vs. Antiretroviral Coverage in Southeast Asia (2025)\nBubble Size Scaled to Total PLHIV; Cross-Sectional r = +0.149 (Demonstrating Primacy of Health Policy Over GDP)',
                 fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('GDP per Capita, PPP (Constant 2021 International $, Log Scale)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Antiretroviral Therapy (ART) Coverage (% of PLHIV)', fontsize=11, fontweight='bold')
    ax.legend(loc='lower left', frameon=True, framealpha=0.95, fontsize=9.5)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, 'fig5_gdp_vs_art_coverage_disparity.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 5 -> {out_path}")


def generate_figure_6():
    """Figure 6: 16-Year ART Coverage Expansion Trajectories Across Southeast Asia & Benchmarks (2010-2025)."""
    logger.info("Generating Figure 6: Longitudinal ART Coverage Trajectories (2010-2025) ...")
    sea = pd.read_csv(os.path.join(PROCESSED_DIR, 'southeast_asia_hiv_panel_2010_2025.csv'))
    bench = pd.read_csv(os.path.join(PROCESSED_DIR, 'regional_global_benchmarks_1990_2025.csv'))
    bench = bench[(bench['year'] >= 2010) & (bench['iso3'].isin(['03M49WLD', 'UNAAP']))]
    
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    
    style_config = {
        'KHM': ('#1E8449', '-', 2.5, 'Cambodia (50% -> 95%)'),
        'THA': ('#2874A6', '-', 2.5, 'Thailand (27% -> 82%)'),
        'VNM': ('#117A65', '-', 2.2, 'Viet Nam (25% -> 75%)'),
        'MMR': ('#C0392B', '-', 3.4, 'Myanmar (12% -> 73%) [Focus]'),
        'TLS': ('#8E44AD', '-.', 1.8, 'Timor-Leste (6% -> 66%)'),
        'LAO': ('#D68910', '-.', 1.8, 'Lao PDR (17% -> 64%)'),
        'MYS': ('#5D6D7E', '-.', 1.8, 'Malaysia (18% -> 63%)'),
        'IDN': ('#E67E22', '--', 2.4, 'Indonesia (5% -> 48%)'),
        'PHL': ('#922B21', '--', 2.4, 'Philippines (5% -> 41%)'),
    }
    
    for iso, (color, ls, lw, lbl) in style_config.items():
        sub = sea[sea['iso3'] == iso].sort_values('year')
        ax.plot(sub['year'], sub['art_coverage_pct'], color=color, linestyle=ls, linewidth=lw,
                marker='o' if iso in ['MMR', 'KHM', 'THA', 'IDN', 'PHL'] else None,
                markersize=4.5, label=lbl, alpha=0.92)
        
    # Add Global benchmark
    g_sub = bench[bench['iso3'] == '03M49WLD'].sort_values('year')
    ax.plot(g_sub['year'], g_sub['art_coverage_pct'], color='#111111', linestyle=':', linewidth=2.4,
            label='Global Benchmark (24% -> 78%)')
    
    ax.axhline(95, color='#27AE60', linestyle='--', linewidth=1.2, alpha=0.7)
    ax.text(2010.2, 96.2, 'UNAIDS Fast-Track Target (~90–95% Population ART Coverage)', fontsize=9.2, fontweight='bold', color='#1E8449')
    
    ax.annotate('Myanmar 2021 Crisis:\nART Dip 69% -> 66% (-3 pp)\n(Preceded 2022 Deaths Rebound)',
                xy=(2021, 66), xytext=(2016.8, 79),
                arrowprops=dict(facecolor='#C0392B', arrowstyle='->', lw=1.3),
                fontsize=9.2, fontweight='bold', color='#78281F',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.95))
    
    ax.set_xlim(2010, 2025.3)
    ax.set_ylim(0, 102)
    ax.set_xticks(range(2010, 2026, 1))
    ax.set_xlabel('Calendar Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Antiretroviral Therapy Coverage (% of All PLHIV)', fontsize=11, fontweight='bold')
    ax.set_title('FIGURE 6: 16-Year Antiretroviral Therapy (ART) Scale-Up Trajectories Across Southeast Asia (2010–2025)\nIllustrating the Three Regional Archetypes: Accelerated Control, Fragile Progress (Myanmar), and Severe Lag',
                 fontsize=12, fontweight='bold', pad=12)
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', frameon=True, fontsize=9.5)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, 'fig6_southeast_asia_art_trajectories_2010_2025.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved Figure 6 -> {out_path}")


def run_all():
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    generate_figure_5()
    generate_figure_6()
    logger.info("All 6 research figures generated successfully in figures/.")


if __name__ == '__main__':
    run_all()
