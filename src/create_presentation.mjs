import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const modulePath=process.env.ARTIFACT_TOOL_MODULE;
if(!modulePath)throw new Error('Set ARTIFACT_TOOL_MODULE to the installed @oai/artifact-tool/dist/artifact_tool.mjs path.');
const {Presentation,PresentationFile}=await import(pathToFileURL(modulePath).href);
const root=process.cwd(),build=path.join(root,'.local-build');
const d=JSON.parse(await fs.readFile(path.join(build,'presentation_data.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const navy='#172B4D',teal='#0D6E66',muted='#475569';
function text(s,copy,x,y,w,h,size=25,color=navy,bold=false){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=copy;t.text.style={typeface:'Aptos',fontSize:size,color,bold,wrap:true};return t;
}
function slide(title){
 const s=p.slides.add();s.background.fill='#FFFFFF';text(s,title,64,37,1152,82,34,navy,true);
 text(s,`HIV estimates and treatment access · UNAIDS 2026 / WDI · ${p.slides.items.length}/22`,64,678,1152,25,13,muted);
 s.speakerNotes.text='Sources: reports/results.json and reports/analysis_tables. Data SHA256 '+d.results.data_sha256+'\nhttps://aidsinfo.unaids.org/dataset\nhttps://www.unaids.org/en/resources/documents/2024/progress-towards-95-95-95\nhttps://pmc.ncbi.nlm.nih.gov/articles/PMC10769177/\nhttps://databank.worldbank.org/source/world-development-indicators\nAll associations are exploratory ecological comparisons of national estimates.';
 return s;
}
function body(s,lines){text(s,lines.join('\n\n'),78,158,1115,442,27);}
function caption(s,copy){text(s,copy,78,603,1120,63,18,muted);}
function table(s,heads,rows,widths){
 const values=[heads,...rows].map(r=>r.map(String));
 const t=s.tables.add({rows:values.length,columns:heads.length,left:75,top:157,width:1130,height:420,values,columnWidths:widths});
 for(let i=0;i<values.length;i++)for(let j=0;j<heads.length;j++){
  const c=t.getCell(i,j);c.fill=i===0?navy:(i%2?'#F0F5F7':'#FFFFFF');
  c.text.style={typeface:'Aptos',fontSize:19,color:i===0?'#FFFFFF':navy,bold:i===0};
 }
 return t;
}
const colors=[teal,'#B91C1C','#3730A3','#B45309','#2874A6','#7A4379','#567B37','#546979','#9B7241'];
function chart(s,kind,categories,series,xtitle,ytitle,opts={}){
 const result=s.charts.add(kind,{position:{left:76,top:142,width:1128,height:448},categories,
  series:series.map((x,i)=>({...x,fill:colors[i%colors.length],line:{fill:colors[i%colors.length],width:2},marker:{symbol:kind==='scatter'?'circle':'none',size:5,fill:colors[i%colors.length]}})),
  hasLegend:series.length>1,legend:{position:'bottom',textStyle:{fontSize:15}},
  titlePlacement:'none',displayBlanksAs:'gap',
  xAxis:{title:xtitle,textStyle:{fontSize:14},tickLabelPosition:'low',...opts.xAxis},yAxis:{title:ytitle,textStyle:{fontSize:14},numberFormatCode:'0.0',majorGridlines:{fill:'#DBE4EA',width:1},...opts.yAxis},
  lineOptions:{smooth:false},barOptions:{direction:'column',grouping:'clustered'},scatterOptions:{style:'marker'}});
 for(const style of [result.legend?.textStyle,result.dataLabels?.textStyle,result.xAxis?.textStyle,result.yAxis?.textStyle,result.xAxis?.title?.textStyle,result.yAxis?.title?.textStyle])if(style)style.typeface='Aptos';
 return result;
}
const mm=d.sea.filter(x=>x.iso3==='MMR'),m10=mm.find(x=>x.year===2010),m25=mm.find(x=>x.year===2025);
const models=d.results.models;let s;
s=slide('HIV trends and treatment access');text(s,'Southeast Asia, 1990–2025',78,179,1125,100,46,navy,true);text(s,'National estimates and exploratory panel associations',78,310,1125,85,30,teal);text(s,'Dr. Aung Chit Moe, MBBS\nHealthcare data analytics portfolio',78,485,1125,100,25,muted);
s=slide('Research questions');body(s,['How did estimated HIV outcomes change over time?','Where do diagnosis, ART access and viral suppression differ?','How sensitive are ART–mortality associations to the model?','Retrospective analysis of a stored snapshot. The revised protocol documents decisions made during review.']);
s=slide('Data coverage');table(s,['Dataset','Entities / countries','Rows'],[['Workbook outcome grid','184 entities','6,624'],['Southeast Asia, 1990–2025','11 countries','396'],['Treatment period, 2010–2025','11 countries','176'],['Uncensored lag-1 model','7 countries','103']],[580,300,250]);caption(s,'The workbook includes countries, territories and aggregates. Aggregate benchmarks never enter country regressions.');
s=slide('Source dependence affects interpretation');body(s,['UNAIDS Spectrum uses ART programme inputs and assumed survival to estimate mortality.','A regression of mortality estimates on ART partly reflects model construction.','WHO disseminates the same source family. Exact matches establish snapshot consistency.','Shared estimated PLHIV denominators can also contribute to ART–mortality associations.']);
s=slide('Censored values retain their meaning');table(s,['Published source','Primary numeric field','Preserved information'],[['<100','Missing','Upper threshold: 100'],['>98','Missing','Lower threshold: 98'],['...','Missing','Unavailable source label'],['4400','4,400','Rounded estimate']],[260,380,490]);caption(s,'No suppressed or censored value is replaced in primary models. A separate sensitivity substitutes disclosed thresholds.');
s=slide('Myanmar annual HIV estimates');chart(s,'line',mm.filter(x=>x.aids_deaths!==null&&x.new_infections!==null).map(x=>String(x.year)),[{name:'Annual new infections',values:mm.filter(x=>x.aids_deaths!==null&&x.new_infections!==null).map(x=>x.new_infections)},{name:'Annual AIDS deaths',values:mm.filter(x=>x.aids_deaths!==null&&x.new_infections!==null).map(x=>x.aids_deaths)}],'Year','Estimated annual count');caption(s,'Censored years are omitted. The standalone figure also displays published marginal uncertainty limits.');
s=slide('Myanmar changes since 2010');body(s,[`Estimated annual AIDS deaths: ${m10.aids_deaths.toLocaleString()} to ${m25.aids_deaths.toLocaleString()} (${(100*(m25.aids_deaths/m10.aids_deaths-1)).toFixed(1)}%).`,`ART coverage: ${m10.art_coverage_pct}% to ${m25.art_coverage_pct}% of all PLHIV.`,`Estimated PLHIV: ${m10.plhiv.toLocaleString()} to ${m25.plhiv.toLocaleString()}.`,'Prevalence and case counts reflect several processes. These data do not isolate survival, prevention or programme effects.']);
s=slide('Myanmar milestones');table(s,['Year','PLHIV','Annual AIDS deaths','ART / all PLHIV'],mm.filter(x=>[2010,2015,2020,2021,2022,2025].includes(x.year)).map(x=>[x.year,x.plhiv.toLocaleString(),x.aids_deaths.toLocaleString(),x.art_coverage_pct+'%']),[180,320,330,300]);caption(s,'The 2021–2022 sequence does not identify effects of conflict, COVID-19, treatment interruption or programme responses.');
const trend=d.trends.filter(x=>d.sea.some(z=>z.iso3===x.iso3)&&x.pct_change_deaths!==null);
s=slide('Changes in annual AIDS deaths');chart(s,'bar',trend.map(x=>x.country_name),[{name:'2010 to 2025 change',values:trend.map(x=>x.pct_change_deaths)}],'Country','Change in annual deaths (%)');caption(s,'Only countries with numeric endpoints appear. Censored endpoints cannot establish zero change.');
const inf=d.trends.filter(x=>d.sea.some(z=>z.iso3===x.iso3)&&x.pct_change_new_infections!==null);
s=slide('Changes in annual new infections');chart(s,'bar',inf.map(x=>x.country_name),[{name:'2010 to 2025 change',values:inf.map(x=>x.pct_change_new_infections)}],'Country','Change in annual infections (%)');caption(s,'Percentage increases can be large from a small baseline. These trends do not measure stigma, prevention delivery or programme quality.');
s=slide('ART coverage over time');const years=Array.from({length:16},(_,i)=>2010+i);chart(s,'line',years.map(String),['MMR','KHM','THA','VNM','IDN','PHL'].map(iso=>({name:d.sea.find(x=>x.iso3===iso).country_name,values:years.map(y=>d.sea.find(x=>x.iso3===iso&&x.year===y).art_coverage_pct)})),'Year','ART / all PLHIV (%)',{yAxis:{min:0,max:100}});caption(s,'Six countries displayed for readability. All 11 country grids remain in the downloadable dataset.');
s=slide('The 95–95–95 denominators');table(s,['Indicator','Denominator','Target'],[['Know HIV status','All PLHIV','95%'],['Receive ART','Diagnosed PLHIV','95%'],['Suppressed viral load','People on ART','95%'],['Receive ART, population equivalent','All PLHIV','90.25%'],['Suppressed, population equivalent','All PLHIV','85.7375%']],[520,370,240]);caption(s,'95% × 95% = 90.25%. The joint cascade target implies 95% × 95% × 95% = 85.7375%.');
const cas=d.cascade.filter(x=>x.is_southeast_asia===1&&x.art_coverage_pct!==null);
s=slide('Population treatment indicators, 2025');chart(s,'bar',cas.map(x=>x.country_name),[{name:'On ART / all PLHIV',values:cas.map(x=>x.art_coverage_pct)},{name:'Suppressed / all PLHIV',values:cas.map(x=>x.virally_suppressed_all_pct)}],'Country','Percent of all PLHIV',{yAxis:{min:0,max:100}});caption(s,'Direct reported indicators. Myanmar suppression is 70%, rather than the product of rounded conditional cascade stages.');
s=slide('Approximate treatment gaps, 2025');chart(s,'bar',d.gaps.map(x=>x.country_name),[{name:'PLHIV not on ART',values:d.gaps.map(x=>x.unreached_plhiv/1000)}],'Country','Approximate count (thousands)');caption(s,'PLHIV × (1 − ART coverage/100). Nine available countries. Brunei and Singapore are excluded from the denominator.');
s=slide('Panel model design');body(s,['Outcome: annual estimated AIDS deaths / estimated PLHIV ×100. This is a descriptive ratio.','Country fixed effects absorb stable country differences. Year effects absorb shared annual shocks.','Lags and first differences require consecutive years. Complete-case samples remain selective.','Country-clustered standard errors use full design-rank correction and a t reference with G−1 degrees of freedom.']);
s=slide('ART–mortality model comparisons');const selected=[models[1],models[3],models[4],models[6],models[10]];table(s,['Model','Coefficient','95% interval','N / countries'],selected.map(x=>[x.model_name.replace('Country and year FE','Country/year FE'),x.coefficient.toFixed(4),`[${x.ci_lower_95.toFixed(4)}, ${x.ci_upper_95.toFixed(4)}]`,x.n_observations+' / '+x.n_countries]),[500,170,270,190]);caption(s,'Outcome percentage points per one pp ART. Country-only versus country/year lag-1 models use the same 103 rows.');
s=slide('Sensitivity comparisons');body(s,[`First differences: coefficient ${models[9].coefficient.toFixed(4)}, N=${models[9].n_observations}.`,`Population-denominator model: coefficient ${models[8].coefficient.toFixed(4)} deaths per 100,000 per pp ART. Its interval includes zero.`,'Leave-one-country-out results document sensitivity to influential national trajectories.','Threshold substitution adds censored rows only as a disclosed scenario. It cannot recover their unknown exact values.']);
const gdp=cas.filter(x=>x.gdp_per_capita_ppp!==null);
s=slide('GDP and ART coverage, 2025');chart(s,'scatter',[],gdp.map(x=>({name:x.country_name,xValues:[x.gdp_per_capita_ppp],values:[x.art_coverage_pct]})),'GDP per capita PPP, constant 2021 international $','ART / all PLHIV (%)',{yAxis:{min:0,max:100},xAxis:{min:0,max:40000}});caption(s,'Nine available countries, same-year WDI values. Financing, programme spending, stigma and delivery quality are not measured.');
s=slide('Limits of the evidence');body(s,['Estimated outcomes depend on model inputs and survival assumptions.','Seven primary-sample country clusters make inference approximate.','Regression intervals omit UNAIDS estimation uncertainty and correlation across published estimates.','Residual confounding and reverse causality remain. No regression-based deaths-averted claim follows from this study.']);
s=slide('Reproducible research outputs');body(s,['Source-labelled CSVs, metadata and raw-input fingerprints.','SQLite star schema and seven analytical SQL outputs.','Machine-readable models and a notebook with executed cells.','Streamlit filters, downloads and read-only SQL examples.']);caption(s,'Repository: github.com/AungChitMoe1995/hiv-epidemiology-and-treatment-analytics');
s=slide('Questions for further research');body(s,['Programme records could examine retention, interruption and treatment initiation directly.','Subnational data could describe local gaps hidden by national averages.','Independent outcome data would strengthen evaluation of service changes.','Joint estimate draws and more country clusters would support better uncertainty analysis.']);
s=slide('Project summary');body(s,['Estimated national HIV outcomes and treatment access differ across Southeast Asia.','Censoring and denominator definitions materially affect comparisons.','ART–mortality associations vary across specifications and remain exploratory.','The portfolio links source data to consistent reports, figures and interactive outputs.']);caption(s,'Live dashboard: hiv-epidemiology-and-treatment-analytics-acm.streamlit.app');
if(p.slides.items.length!==22)throw new Error('Unexpected slide count');
await fs.mkdir(path.join(root,'docs/presentation'),{recursive:true});
await(await PresentationFile.exportPptx(p)).save(path.join(root,'docs/presentation/hiv_epidemiology_research_briefing.pptx'));
console.log('Exported 22 editable slides');

await fs.rename(path.join(root,'docs/presentation/hiv_epidemiology_research_briefing.pptx.inspect.ndjson'),path.join(build,'presentation.inspect.ndjson')).catch(()=>{});
