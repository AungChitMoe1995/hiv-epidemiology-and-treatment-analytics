"""Reported cascade indicators and approximate treatment gaps, with denominators explicit."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
def analyze_cascade():
    sea=pd.read_csv(ROOT/'data/processed/southeast_asia_hiv_panel_2010_2025.csv')
    bench=pd.read_csv(ROOT/'data/processed/regional_global_benchmarks_1990_2025.csv')
    d=pd.concat([sea,bench]).query('year==2025').copy()
    d['pop_level_viral_suppression_pct']=d.virally_suppressed_all_pct
    d['cascade_product_for_comparison_pct']=d.diagnosed_1st95_pct*d.on_art_2nd95_pct*d.virally_suppressed_3rd95_pct/10000
    # Rectangular combinations of marginal limits are scenarios, not joint confidence limits.
    d['gap_scenario_low']=d.plhiv_low*(1-d.art_coverage_high/100)
    d['gap_scenario_high']=d.plhiv_high*(1-d.art_coverage_low/100)
    out=ROOT/'reports/analysis_tables'
    d.to_csv(out/'cascade_2025_summary.csv',index=False,lineterminator='\n')
    gaps=d[d.is_southeast_asia.eq(1)&d.unreached_plhiv.notna()].copy()
    gaps['share_of_available_country_gap_pct']=gaps.unreached_plhiv/gaps.unreached_plhiv.sum()*100
    gaps.sort_values('unreached_plhiv',ascending=False).to_csv(out/'treatment_gaps_2025.csv',index=False,lineterminator='\n')
    # Retain a descriptive country snapshot, replacing unsupported clinical archetypes.
    d[d.is_southeast_asia.eq(1)][['iso3','country_name','art_coverage_pct','treatment_gap_pct','unreached_plhiv']].to_csv(out/'country_treatment_snapshot_2025.csv',index=False,lineterminator='\n')
    legacy=out/'archetype_classification.csv'
    if legacy.exists(): legacy.unlink()
    return d,gaps
if __name__=='__main__': analyze_cascade()
