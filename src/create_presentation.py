"""
src/create_presentation.py
==========================
Generates an uncluttered, spacious, publication-grade widescreen (16:9) PowerPoint
research briefing for the HIV Epidemiological Trends & Treatment Disparities Project (1990–2025).

Design Principles (Anti-Clutter Executive Standard):
- 22 spacious widescreen slides (13.333" x 7.5")
- Single-line 24pt bold slide titles (never wrapping)
- Concise, high-impact bullet points (10–15 words per bullet, max 3 bullets per card)
- At least 20–35% open whitespace inside every card (zero text overflow or crowding)
- Dedicated full-canvas slides for all 6 publication figures so chart labels are large and crisp.

Outputs:
  - docs/presentation/hiv_epidemiology_research_briefing.pptx
  - reports/hiv_epidemiology_research_briefing.pptx
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_deck(base_dir: str):
    TOTAL_SLIDES = 22
    print("=" * 76)
    print(f"GENERATING SPACIOUS WIDESCREEN POWERPOINT BRIEFING ({TOTAL_SLIDES} SLIDES)")
    print("=" * 76)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    pres_dir = os.path.join(base_dir, "docs", "presentation")
    reports_dir = os.path.join(base_dir, "reports")
    figures_dir = os.path.join(base_dir, "figures")
    os.makedirs(pres_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # Color Palette
    NAVY = RGBColor(23, 43, 77)            # #172B4D - Primary Header & Brand
    NAVY_DARK = RGBColor(13, 27, 52)       # #0D1B34 - Deep Title / Closing Background
    SLATE = RGBColor(71, 85, 105)          # #475569 - Secondary / Subtitle Text
    CRIMSON = RGBColor(185, 28, 28)        # #B91C1C - Alert / Accent Red
    TEAL = RGBColor(13, 110, 102)          # #0D6E66 - Clinical / Protective Accent
    INDIGO = RGBColor(55, 48, 163)         # #3730A3 - Econometric / Method Accent
    AMBER = RGBColor(180, 83, 9)           # #B45309 - Warning / Highlight
    DARK = RGBColor(15, 23, 42)            # #0F172A - High-Contrast Body Text
    CARD_BG = RGBColor(248, 250, 252)      # #F8FAFC - Soft Card Fill
    CARD_BORDER = RGBColor(203, 213, 225)  # #CBD5E1 - Clean Card Border
    LIGHT_INDIGO = RGBColor(238, 242, 255)
    LIGHT_TEAL = RGBColor(240, 253, 250)
    LIGHT_RED = RGBColor(254, 242, 242)
    LIGHT_AMBER = RGBColor(254, 243, 199)
    WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header_and_footer(slide, slide_num, title_text, category_text="HIV EPIDEMIOLOGY & TREATMENT DISPARITIES"):
        header_box = slide.shapes.add_textbox(Inches(0.70), Inches(0.26), Inches(11.93), Inches(0.92))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CRIMSON

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_before = Pt(2)

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.70), Inches(1.18), Inches(11.93), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        footer_box = slide.shapes.add_textbox(Inches(0.70), Inches(7.10), Inches(11.93), Inches(0.30))
        tf_f = footer_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        pf = tf_f.paragraphs[0]
        pf.text = f"HIV Epidemiological Trends & Treatment Disparities in Southeast Asia (1990–2025)   |   UNAIDS 2026 • WHO GHO • World Bank WDI   |   Slide {slide_num} of {TOTAL_SLIDES}"
        pf.font.size = Pt(10.5)
        pf.font.color.rgb = SLATE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER,
                 accent_color=NAVY, accent_pos="top", accent_thickness=0.08):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.0)

        if accent_color is not None:
            if accent_pos == "top":
                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(accent_thickness))
            else:
                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(accent_thickness), Inches(height))
            bar.fill.solid()
            bar.fill.fore_color.rgb = accent_color
            bar.line.fill.background()

        is_compact = height < 1.5
        pad_l = 0.22 if accent_pos != "left" else (accent_thickness + 0.16)
        pad_t = (0.08 if is_compact else 0.18) if accent_pos != "top" else (accent_thickness + (0.08 if is_compact else 0.14))
        pad_b = 0.08 if is_compact else 0.14
        tb = slide.shapes.add_textbox(
            Inches(left + pad_l),
            Inches(top + pad_t),
            Inches(width - pad_l - 0.18),
            Inches(height - pad_t - pad_b)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        return tf

    def add_bullets(tf, items, font_size=15.5, color=DARK, space_after=12):
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(font_size)
            p.font.color.rgb = color
            p.space_after = Pt(space_after)

    def add_full_figure_slide(slide_num, title_text, category_text, fig_filename, banner_text, banner_color=NAVY, banner_bg=LIGHT_INDIGO):
        slide = prs.slides.add_slide(blank_layout)
        add_header_and_footer(slide, slide_num, title_text, category_text)

        # Top Takeaway Banner
        tf_b = add_card(slide, 0.70, 1.28, 11.93, 0.72, bg_color=banner_bg, border_color=banner_color,
                        accent_color=banner_color, accent_pos="left", accent_thickness=0.10)
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf_b.paragraphs[0]
        p.text = banner_text
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK

        # Full-Canvas Figure Placement
        fig_path = os.path.join(figures_dir, fig_filename)
        if os.path.exists(fig_path):
            from PIL import Image
            with Image.open(fig_path) as im:
                w_px, h_px = im.size
            aspect = w_px / h_px
            max_w = 11.80
            max_h = 4.82
            if max_w / max_h > aspect:
                disp_h = max_h
                disp_w = disp_h * aspect
            else:
                disp_w = max_w
                disp_h = disp_w / aspect
            left_in = (13.333 - disp_w) / 2.0
            top_in = 2.10 + (max_h - disp_h) / 2.0
            slide.shapes.add_picture(fig_path, Inches(left_in), Inches(top_in), width=Inches(disp_w))

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid(); bg1.fill.fore_color.rgb = NAVY_DARK; bg1.line.fill.background()

    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(0.75), Inches(0.14), Inches(4.05))
    stripe.fill.solid(); stripe.fill.fore_color.rgb = CRIMSON; stripe.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.15), Inches(0.75), Inches(11.4), Inches(4.05))
    tf1 = tb1.text_frame; tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PUBLIC-HEALTH SURVEILLANCE & EPIDEMIOLOGICAL ANALYTICS BRIEFING"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = RGBColor(248, 113, 113); p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "HIV Epidemiological Transitions and Treatment Disparities in Southeast Asia (1990–2025)"
    p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = WHITE; p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "A 36-Year Comparative Longitudinal Study of Myanmar Against Regional & Global Benchmarks"
    p.font.size = Pt(19.5); p.font.color.rgb = RGBColor(203, 213, 225); p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "Lead Investigator: MBBS Physician (Myanmar)  •  Healthcare Data Analytics & Clinical Research"
    p.font.size = Pt(15.5); p.font.bold = True; p.font.color.rgb = WHITE; p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Data Sources: UNAIDS 2026 Spectrum Estimates  •  WHO Global Health Observatory  •  World Bank WDI"
    p.font.size = Pt(14); p.font.color.rgb = RGBColor(148, 163, 184)

    badges = [
        ("6,624", "Global Country-Years", "184 entities (1990–2025)"),
        ("-63.3%", "Myanmar Deaths Drop", "ART scaled 12% → 73% (2010–25)"),
        ("+639%", "Philippine Surge", "Fastest-growing epidemic in SEA"),
        ("-0.49 pp", "Lagged ART Effect", "Per +10 pp ART (p < 0.00001)")
    ]
    for i, (b_val, b_title, b_desc) in enumerate(badges):
        bx = 0.75 + i * 3.01
        b_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(5.15), Inches(2.80), Inches(1.75))
        b_card.fill.solid(); b_card.fill.fore_color.rgb = RGBColor(27, 54, 93)
        b_card.line.color.rgb = RGBColor(71, 85, 105); b_card.line.width = Pt(1.2)
        btf = b_card.text_frame; btf.word_wrap = True
        btf.margin_left = btf.margin_right = Inches(0.18); btf.margin_top = Inches(0.18)

        bp1 = btf.paragraphs[0]; bp1.text = b_val; bp1.font.size = Pt(26); bp1.font.bold = True
        bp1.font.color.rgb = RGBColor(94, 234, 212); bp1.space_after = Pt(4)

        bp2 = btf.add_paragraph(); bp2.text = b_title; bp2.font.size = Pt(15); bp2.font.bold = True
        bp2.font.color.rgb = WHITE; bp2.space_after = Pt(4)

        bp3 = btf.add_paragraph(); bp3.text = b_desc; bp3.font.size = Pt(13)
        bp3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: CLINICAL & PATHOPHYSIOLOGICAL FRAMEWORK
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s2, 2, "Clinical Pathophysiology: How ART Reshapes Population Curves", "CLINICAL & EPIDEMIOLOGICAL FOUNDATION")

    pillars2 = [
        ("1. VIRAL SUPPRESSION", "Bedside Clinical Mechanism", TEAL, [
            "Untreated HIV depletes CD4+ T-cells, causing fatal TB and opportunistic infections.",
            "Potent ART suppresses plasma HIV RNA (<50 copies/mL) within 3–6 months.",
            "Sustained viral suppression halts AIDS mortality and blocks transmission (U=U)."
        ]),
        ("2. PREVALENCE PARADOX", "Prevalence ≈ Incidence × Duration", NAVY, [
            "When ART scales up rapidly, people living with HIV survive for decades.",
            "In Myanmar, new infections fell -44%, yet total PLHIV grew from 250k to 310k.",
            "Rising PLHIV alongside falling deaths is a hallmark of treatment success."
        ]),
        ("3. BIOLOGICAL LAGS", "Why Mortality Drops 1–2 Years Later", CRIMSON, [
            "Patients starting ART with low CD4 (<200) still face early mortality risk.",
            "Population-level immune reconstitution requires 12–24 months of retention.",
            "Thus, expanding ART in year (t-1) drives survival gains in year (t)."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(pillars2):
        tf = add_card(s2, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=15, space_after=12)

    # =========================================================================
    # SLIDE 3: STUDY DESIGN & RESEARCH QUESTIONS (2x2 GRID)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s3, 3, "Study Protocol: Four Core Research Questions (RQ1–RQ4)", "PRE-SPECIFIED RESEARCH DESIGN")

    rq_cards = [
        ("RQ1: LAGGED PROTECTIVE EFFECT OF ART (PRIMARY)", NAVY, LIGHT_INDIGO,
         "Does national ART expansion reduce AIDS mortality rates across Southeast Asia (2010–2025)?",
         "Hypothesis: +10 pp lagged ART significantly lowers PLHIV mortality (p < 0.001)."),
        ("RQ2: MYANMAR'S 36-YEAR TRAJECTORY (1990–2025)", CRIMSON, LIGHT_RED,
         "How did Myanmar transition from peak epidemic to ART scale-up and navigate the 2021 crisis?",
         "Hypothesis: Rapid ART cut deaths >60%, while the 2021 dip caused a 2022 mortality rebound."),
        ("RQ3: REGIONAL 95-95-95 CASCADE DISPARITIES", TEAL, LIGHT_TEAL,
         "Where do the largest diagnosis, linkage, and viral suppression bottlenecks persist in 2025?",
         "Hypothesis: Indonesia and the Philippines hold >55% of all untreated PLHIV in SEA."),
        ("RQ4: MACROECONOMIC WEALTH VS. TREATMENT", AMBER, LIGHT_AMBER,
         "Is higher GDP per capita (PPP) linearly associated with superior ART coverage in SEA?",
         "Hypothesis: National wealth is decoupled from ART coverage due to donor aid and policy gaps.")
    ]
    for i, (head, col, bg, q_txt, h_txt) in enumerate(rq_cards):
        col_idx = i % 2
        row_idx = i // 2
        x = 0.70 + col_idx * 6.08
        y = 1.38 + row_idx * 2.78
        tf = add_card(s3, x, y, 5.85, 2.55, bg_color=bg, border_color=col, accent_color=col, accent_pos="left", accent_thickness=0.12)
        p = tf.paragraphs[0]; p.text = head; p.font.size = Pt(15.5); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(6)
        p = tf.add_paragraph(); p.text = q_txt; p.font.size = Pt(14.5); p.font.color.rgb = DARK; p.space_after = Pt(8)
        p = tf.add_paragraph(); p.text = f"▸  {h_txt}"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 4: DATA PROVENANCE & ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s4, 4, "Data Provenance: Authenticated Surveillance Architecture", "STAGE 1 DATA RECONNAISSANCE & VERIFICATION")

    sources4 = [
        ("1. UNAIDS 2026 ESTIMATES", "Primary Epidemiological Core", CRIMSON, [
            "Official 2026 Spectrum/EPP workbook (6,228 burden rows, 1990–2025).",
            "Test-&-Treat cascade sheet (2,944 rows, 2010–2025) for 95-95-95 metrics.",
            "Includes 95% Uncertainty Bounds (Low / High) for all core indicators."
        ]),
        ("2. WHO GHO ODATA API", "Independent Cross-Validation", TEAL, [
            "Programmatically queried 15,320 records across 4 official HIV indicators.",
            "Verified 100.0% exact numerical concordance with UNAIDS for Myanmar & SEA.",
            "Confirmed identical point estimates and uncertainty intervals."
        ]),
        ("3. WORLD BANK WDI & SQL DB", "Macroeconomic & Relational Layer", NAVY, [
            "Extracted 28,728 records for GDP per capita (PPP & US$) and Total Population.",
            "Normalized into a 4-table SQLite star schema (hiv_surveillance.db).",
            "Isolated Global (03M49WLD) & Asia-Pacific (UNAAP) to prevent double-counting."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(sources4):
        tf = add_card(s4, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=15, space_after=12)

    # =========================================================================
    # SLIDE 5: PROGRAMMATIC DATA QUALITY AUDIT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s5, 5, "Programmatic Data Quality & Reconciliation Audit", "AUTOMATED SQL & PYTHON VERIFICATION")

    t_shape5 = s5.shapes.add_table(6, 4, Inches(0.70), Inches(1.38), Inches(11.93), Inches(3.90))
    t5 = t_shape5.table
    for idx, w in enumerate([2.80, 4.33, 3.30, 1.50]):
        t5.columns[idx].width = Inches(w)

    h5 = ["Audit Dimension", "Verification Logic", "Empirical Result", "Status"]
    rows5 = [
        ("Primary Key Uniqueness", "GROUP BY (iso3, year) HAVING COUNT(*) > 1", "0 duplicates across 6,624 rows", "PASS (100%)"),
        ("Foreign Key Integrity", "LEFT JOIN dim_country WHERE iso3 IS NULL", "0 orphaned rows across 3 fact tables", "PASS (100%)"),
        ("Boundary & Scale Parsing", "Parse '<100', '>98%' cascade, and 'm' millions", "100% parsed (KHM >98%, Global 41m)", "VERIFIED"),
        ("WHO vs. UNAIDS Identity", "Cross-check MMR deaths & ART (2000–2025)", "100% match (2025: 4,400 deaths, 73% ART)", "EXACT MATCH"),
        ("Python vs. SQL Parity", "Compare Pandas vs. SQLite view aggregates", "Discrepancy = 0.000000 (107,000 deaths)", "EXACT MATCH")
    ]
    for c_i, h_txt in enumerate(h5):
        cell = t5.cell(0, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = NAVY; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]; p.text = h_txt; p.font.size = Pt(14.5); p.font.bold = True; p.font.color.rgb = WHITE

    for r_i, r_data in enumerate(rows5, start=1):
        bg = WHITE if r_i % 2 == 1 else CARD_BG
        for c_i, val in enumerate(r_data):
            cell = t5.cell(r_i, c_i); cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_TEAL if c_i == 3 else bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(14)
            p.font.bold = (c_i in (0, 3))
            p.font.color.rgb = TEAL if c_i == 3 else (NAVY if c_i == 0 else DARK)

    tf_b5 = add_card(s5, 0.70, 5.48, 11.93, 1.38, bg_color=LIGHT_INDIGO, border_color=INDIGO, accent_color=INDIGO, accent_pos="left", accent_thickness=0.10)
    p = tf_b5.paragraphs[0]; p.text = "NON-NEGOTIABLE SCIENTIFIC INTEGRITY RULE: ZERO SYNTHETIC IMPUTATION"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = INDIGO; p.space_after = Pt(4)
    p = tf_b5.add_paragraph(); p.text = "Brunei Darussalam (suppressed '...' due to microstate privacy) and Singapore's suppressed cascade cells are documented transparently and never interpolated."
    p.font.size = Pt(14.5); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 6: FIGURE 1 FULL-SCREEN VISUAL (MYANMAR 36-YEAR TRAJECTORY)
    # =========================================================================
    add_full_figure_slide(
        6,
        "Myanmar 36-Year Epidemiological Trajectory (1990–2025)",
        "EMPIRICAL FINDINGS • FIGURE 1 VISUALIZATION",
        "fig1_myanmar_longitudinal_trajectory.png",
        "TAKEAWAY: New infections fell -64.8% from the 2000 peak (27k → 9.5k) and AIDS deaths fell -66.2% from the 2006 peak (13k → 4.4k).",
        banner_color=CRIMSON, banner_bg=LIGHT_RED
    )

    # =========================================================================
    # SLIDE 7: MYANMAR LONGITUDINAL ANALYSIS: THREE DISTINCT ERAS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s7, 7, "Myanmar Longitudinal Analysis: Three Epidemiological Eras", "CLINICAL & HISTORICAL INTERPRETATION OF FIGURE 1")

    eras7 = [
        ("ERA 1: EXPANSION & PEAK (1990–2006)", "Pre-ART Public Health Emergency", CRIMSON, [
            "Outbreaks in PWID and sex workers drove rapid early transmission.",
            "New infections peaked at 27,000 in 2000; adult prevalence hit 0.9%.",
            "Without public ART, annual AIDS deaths peaked at 13,000 in 2006."
        ]),
        ("ERA 2: RAPID ART SCALE-UP (2010–2020)", "Decentralized Clinical Transformation", TEAL, [
            "NAP and NGO clinics scaled national ART coverage from 12% to 69%.",
            "Annual AIDS deaths plunged -63.3% (12,000 in 2010 → 4,400 in 2020).",
            "Total PLHIV rose to 290,000 as patients survived long-term."
        ]),
        ("ERA 3: CRISIS & RESILIENCE (2021–2025)", "System Shock & Community Recovery", NAVY, [
            "In 2021, political crisis and COVID-19 caused ART to dip (69% → 66%).",
            "Interruptions triggered an +11.6% mortality rebound in 2022 (4,800 deaths).",
            "Multi-month dispensing restored ART to 73% (4,400 deaths) by 2025."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(eras7):
        tf = add_card(s7, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=15, space_after=12)

    # =========================================================================
    # SLIDE 8: MYANMAR SURVEILLANCE MILESTONE TABLE (2010–2025)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s8, 8, "Myanmar Surveillance Milestone Table (2010–2025)", "QUANTITATIVE ANATOMY OF THE 2021–2022 MORTALITY REBOUND")

    t_shape8 = s8.shapes.add_table(8, 7, Inches(0.70), Inches(1.38), Inches(11.93), Inches(5.35))
    t8 = t_shape8.table
    for idx, w in enumerate([1.15, 1.65, 1.75, 1.85, 1.75, 1.85, 1.93]):
        t8.columns[idx].width = Inches(w)

    h8 = ["Year", "Total PLHIV", "New Infections", "AIDS Deaths", "ART Coverage", "Mortality / PLHIV", "Clinical Phase"]
    mmr_rows8 = [
        ("2010", "250,000", "17,000", "12,000", "12%", "4.80%", "Baseline Expansion"),
        ("2015", "270,000", "14,000", "7,800", "40%", "2.89%", "Rapid Scale-Up"),
        ("2020", "290,000", "10,000", "4,400", "69%", "1.52%", "Pre-Crisis Peak"),
        ("2021", "290,000", "11,000", "4,300", "66% (-3 pp)", "1.48%", "Supply & Clinic Shock"),
        ("2022", "300,000", "11,000", "4,800 (+11.6%)", "70%", "1.60% (Spike)", "1-Yr Lagged Rebound"),
        ("2024", "300,000", "9,900", "4,400", "72%", "1.47%", "NGO / MMD Stabilization"),
        ("2025", "310,000", "9,500", "4,400", "73%", "1.42%", "Current Equilibrium")
    ]
    for c_i, h_txt in enumerate(h8):
        cell = t8.cell(0, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = NAVY; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]; p.text = h_txt; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = WHITE

    for r_i, r_data in enumerate(mmr_rows8, start=1):
        is_shock = r_data[0] in ("2021", "2022")
        bg = LIGHT_RED if is_shock else (WHITE if r_i % 2 == 1 else CARD_BG)
        for c_i, val in enumerate(r_data):
            cell = t8.cell(r_i, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = bg; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(14)
            p.font.bold = (c_i == 0 or is_shock)
            p.font.color.rgb = CRIMSON if is_shock else (NAVY if c_i == 0 else DARK)

    # =========================================================================
    # SLIDE 9: FIGURE 2 FULL-SCREEN VISUAL (REGIONAL DIVERGENCE 2010–2025)
    # =========================================================================
    add_full_figure_slide(
        9,
        "Regional Fast-Track Divergence in Southeast Asia (2010–2025)",
        "COMPARATIVE REGIONAL OUTCOMES • FIGURE 2 VISUALIZATION",
        "fig2_southeast_asia_mortality_infection_divergence.png",
        "TAKEAWAY: Thailand (-79.5%) and Myanmar (-63.3%) beat the Global mortality drop (-56.2%), while the Philippines surged +440%.",
        banner_color=NAVY, banner_bg=LIGHT_INDIGO
    )

    # =========================================================================
    # SLIDE 10: REGIONAL DIVERGENCE INSIGHTS: CONTROL VS. OUTBREAK
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s10, 10, "Regional Divergence Insights: Why Trajectories Split", "EPIDEMIOLOGICAL DRIVERS OF FIGURE 2")

    div_cards10 = [
        ("1. EPIDEMIC CONTROL LEADERS", "Thailand, Myanmar & Cambodia", TEAL, [
            "Thailand cut AIDS deaths by -79.5% (41k → 8.4k) and new infections by -65.2%.",
            "Myanmar achieved the 2nd largest mortality reduction in SEA (-63.3%).",
            "Cambodia reduced new infections by -58.3% via 95% ART coverage."
        ]),
        ("2. PHILIPPINE HYPER-OUTBREAK", "+639.1% Infections | +440% Deaths", CRIMSON, [
            "Annual new infections surged 7.4-fold from 4,600 (2010) to 34,000 (2025).",
            "Driven by youth MSM transmission, legal testing barriers, and low PrEP access.",
            "With 41% ART coverage, annual AIDS deaths rose from 500 to 2,700 (+440%)."
        ]),
        ("3. INDONESIA'S PARADOX", "-56.2% Infections vs. +28.6% Deaths", AMBER, [
            "New infections dropped -56.2%, yet AIDS deaths rose +28.6% (14k → 18k).",
            "Only 48% of Indonesia's 560,000 PLHIV receive ART (291,200 untreated).",
            "Untreated cohorts from earlier waves are now progressing to late-stage AIDS."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(div_cards10):
        tf = add_card(s10, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=15, space_after=12)

    # =========================================================================
    # SLIDE 11: FIGURE 6 FULL-SCREEN VISUAL (16-YEAR ART TRAJECTORIES)
    # =========================================================================
    add_full_figure_slide(
        11,
        "16-Year ART Coverage Expansion Trajectories (2010–2025)",
        "LONGITUDINAL TREATMENT SCALE-UP • FIGURE 6 VISUALIZATION",
        "fig6_southeast_asia_art_trajectories_2010_2025.png",
        "TAKEAWAY: Myanmar achieved the largest absolute ART coverage gain in Southeast Asia (+61 percentage points: 12% → 73%).",
        banner_color=TEAL, banner_bg=LIGHT_TEAL
    )

    # =========================================================================
    # SLIDE 12: TRIPARTITE EPIDEMIOLOGICAL ARCHETYPES TABLE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s12, 12, "Tripartite Classification of Southeast Asian Health Systems", "REGIONAL TYPOLOGY & BENCHMARK MATRIX (2010–2025)")

    t_shape12 = s12.shapes.add_table(11, 7, Inches(0.70), Inches(1.36), Inches(11.93), Inches(5.55))
    t12 = t_shape12.table
    for idx, w in enumerate([1.80, 1.25, 1.35, 1.35, 1.50, 2.38, 2.30]):
        t12.columns[idx].width = Inches(w)

    h12 = ["Country / Benchmark", "2025 PLHIV", "Deaths Δ%", "New Inf Δ%", "2025 ART Cov", "Epidemiological Archetype", "Primary System Driver"]
    arch_rows12 = [
        ("Cambodia (KHM)", "76,000", "-41.2%", "-58.3%", "95% (Gap 5%)", "Archetype A: Accelerated Control", "Universal ART & retention"),
        ("Thailand (THA)", "620,000", "-79.5%", "-65.2%", "82% (Gap 18%)", "Archetype A: Accelerated Control", "UHC & 100% Condom Program"),
        ("Viet Nam (VNM)", "270,000", "-14.6%", "-56.4%", "75% (Gap 25%)", "Archetype A: Accelerated Control", "Harm reduction & methadone"),
        ("Myanmar (MMR)", "310,000", "-63.3%", "-44.1%", "73% (Gap 27%)", "Archetype B: Fragile Progress", "Rapid scale-up; 2021 shock"),
        ("Timor-Leste (TLS)", "2,200", "0.0%", "0.0%", "66% (Gap 34%)", "Archetype B: Fragile Progress", "Small cohort containment"),
        ("Lao PDR (LAO)", "23,000", "0.0%", "+8.3%", "64% (Gap 36%)", "Archetype B: Fragile Progress", "Cross-border mobility"),
        ("Malaysia (MYS)", "85,000", "-41.2%", "-52.5%", "63% (Gap 37%)", "Archetype B: Fragile Progress", "PWID success; MSM barriers"),
        ("Indonesia (IDN)", "560,000", "+28.6%", "-56.2%", "48% (Gap 52%)", "Archetype C: Severe Gap", "Decentralized LTFU"),
        ("Philippines (PHL)", "250,000", "+440.0%", "+639.1%", "41% (Gap 59%)", "Archetype C: Counter-Epidemic", "Youth MSM surge; low ART"),
        ("Global (03M49WLD)", "41,000,000", "-56.2%", "-42.9%", "78% (Gap 22%)", "Global Benchmark", "Worldwide Fast-Track reference")
    ]
    for c_i, h_txt in enumerate(h12):
        cell = t12.cell(0, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = NAVY; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]; p.text = h_txt; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = WHITE

    for r_i, r_data in enumerate(arch_rows12, start=1):
        arch = r_data[5]
        if "Archetype A" in arch:
            b_bg, b_col = LIGHT_TEAL, TEAL
        elif "Archetype B" in arch:
            b_bg, b_col = LIGHT_INDIGO, INDIGO
        elif "Archetype C" in arch:
            b_bg, b_col = LIGHT_RED, CRIMSON
        else:
            b_bg, b_col = LIGHT_AMBER, AMBER
        row_bg = WHITE if r_i % 2 == 1 else CARD_BG
        for c_i, val in enumerate(r_data):
            cell = t12.cell(r_i, c_i); cell.fill.solid()
            cell.fill.fore_color.rgb = b_bg if c_i == 5 else row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(12.8)
            p.font.bold = (c_i in (0, 4, 5))
            p.font.color.rgb = b_col if c_i == 5 else (NAVY if c_i == 0 else DARK)

    # =========================================================================
    # SLIDE 13: FIGURE 3 FULL-SCREEN VISUAL (2025 95-95-95 CASCADE)
    # =========================================================================
    add_full_figure_slide(
        13,
        "UNAIDS 95-95-95 Cascade & Treatment Gap Burden (2025)",
        "CLINICAL CONTINUUM OF CARE • FIGURE 3 VISUALIZATION",
        "fig3_unaids_95_95_95_cascade_2025.png",
        "TAKEAWAY: Cambodia (95–>98–>98) met all three targets; Indonesia (291.2k) and Philippines (147.5k) hold 58.8% of untreated PLHIV.",
        banner_color=CRIMSON, banner_bg=LIGHT_RED
    )

    # =========================================================================
    # SLIDE 14: CLINICAL BOTTLENECKS IN THE 2025 CARE CONTINUUM
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s14, 14, "Clinical Continuum Analysis: Where the Cascade Breaks", "DIAGNOSIS, LINKAGE & VIRAL SUPPRESSION BOTTLENECKS")

    casc_cards14 = [
        ("1. HIGH VIRAL SUPPRESSION", "3rd 95 Exceeds 95% Across SEA", TEAL, [
            "Once on dolutegravir-based ART, >95% achieve viral suppression in KHM (>98%), THA (>98%), PHL (97%), VNM (96%), and MMR (96%).",
            "Clinical insight: Treatment gaps stem from upstream testing and linkage, not drug resistance."
        ]),
        ("2. UPSTREAM BOTTLENECKS", "1st & 2nd 95 Attrition", CRIMSON, [
            "Philippines: 62% diagnosed (1st 95) and 66% linked to ART (2nd 95) -> 41% coverage.",
            "Indonesia: 67% diagnosed and 72% linked to ART -> 48% coverage (291.2k untreated).",
            "Malaysia: 66% diagnosed, though 95% of diagnosed initiate ART."
        ]),
        ("3. MYANMAR'S 2025 CASCADE", "84% Diagnosed – 86% ART – 96% Suppressed", NAVY, [
            "Myanmar outperforms the Asia-Pacific average (81% Diagnosed, 72% ART Coverage).",
            "Population viral suppression is 69.4% of all PLHIV in Myanmar (vs. 68.4% in Asia-Pacific).",
            "Remaining gap: Reaching 83,700 untreated PLHIV (27%) in conflict zones."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(casc_cards14):
        tf = add_card(s14, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=14.8, space_after=12)

    # =========================================================================
    # SLIDE 15: FIGURE 4 FULL-SCREEN VISUAL (ECONOMETRIC DOSE-RESPONSE)
    # =========================================================================
    add_full_figure_slide(
        15,
        "Econometric Dose-Response: Lagged ART vs. Mortality",
        "FIXED-EFFECTS PANEL MODELING • FIGURE 4 VISUALIZATION",
        "fig4_lagged_art_mortality_dose_response.png",
        "TAKEAWAY: Within-country fixed-effects OLS confirms β = -0.0491 (t = -14.20, p < 0.00001, Within R² = 68.7%, N = 135).",
        banner_color=INDIGO, banner_bg=LIGHT_INDIGO
    )

    # =========================================================================
    # SLIDE 16: FIXED-EFFECTS PANEL REGRESSION SPECIFICATIONS TABLE
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s16, 16, "Fixed-Effects Panel Regression Models (2010–2025)", "ECONOMETRIC PARAMETER ESTIMATES & ROBUSTNESS CHECKS")

    t_shape16 = s16.shapes.add_table(6, 7, Inches(0.70), Inches(1.38), Inches(11.93), Inches(3.85))
    t16 = t_shape16.table
    for idx, w in enumerate([2.95, 2.15, 1.35, 1.35, 1.35, 1.38, 1.40]):
        t16.columns[idx].width = Inches(w)

    h16 = ["Model Specification (Within FE)", "Regressor", "Beta Coef", "Robust SE", "t-Stat", "p-Value", "Within R² (N)"]
    reg_rows16 = [
        ("Model 1: Contemporaneous ART", "ART Coverage (t)", "-0.0514", "0.0036", "-14.344", "< 0.00001", "0.6868 (N=144)"),
        ("Model 2: 1-Year Lagged ART [Primary]", "ART Coverage (t-1)", "-0.0491", "0.0035", "-14.202", "< 0.00001", "0.6874 (N=135)"),
        ("Model 3: 2-Year Lagged ART", "ART Coverage (t-2)", "-0.0462", "0.0035", "-13.302", "< 0.00001", "0.6674 (N=126)"),
        ("Model 4: Lagged ART + Macro Control", "ART Coverage (t-1)", "-0.0624", "0.0049", "-12.830", "< 0.00001", "0.7307 (N=135)"),
        ("Model 4: Lagged ART + Macro Control", "log(GDP PPP)", "+1.8376", "0.5688", "+3.231", "0.00123", "0.7307 (N=135)")
    ]
    for c_i, h_txt in enumerate(h16):
        cell = t16.cell(0, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = NAVY; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]; p.text = h_txt; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = WHITE

    for r_i, r_data in enumerate(reg_rows16, start=1):
        bg = LIGHT_TEAL if r_i == 2 else (WHITE if r_i % 2 == 1 else CARD_BG)
        for c_i, val in enumerate(r_data):
            cell = t16.cell(r_i, c_i); cell.fill.solid(); cell.fill.fore_color.rgb = bg; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(13.5)
            p.font.bold = (c_i in (0, 2, 5) or r_i == 2)
            p.font.color.rgb = TEAL if (r_i == 2 and c_i in (0, 2, 5)) else (NAVY if c_i == 0 else DARK)

    tf_b16 = add_card(s16, 0.70, 5.42, 11.93, 1.44, bg_color=LIGHT_TEAL, border_color=TEAL, accent_color=TEAL, accent_pos="left", accent_thickness=0.10)
    p = tf_b16.paragraphs[0]; p.text = "CLINICAL EFFECT SIZE TRANSLATION (MODEL 2 & MODEL 4)"; p.font.size = Pt(14.5); p.font.bold = True; p.font.color.rgb = TEAL; p.space_after = Pt(4)
    p = tf_b16.add_paragraph(); p.text = "Every +10 percentage point expansion in lagged ART coverage reduces the PLHIV mortality rate by 0.49 percentage points (or 0.62 pp controlling for log GDP PPP). In Myanmar's cohort of 310,000 PLHIV, each +10 pp ART gain averts ~1,520 AIDS deaths annually."
    p.font.size = Pt(14); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 17: DOCTOR'S BIOSTATISTICAL & INTERVIEW DEFENSE GUIDE
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s17, 17, "Methodological Defense: Fixed Effects & Lag Structure", "INTERVIEW DEFENSE GUIDE FOR HEALTHCARE ANALYTICS")

    def_cards17 = [
        ("1. WHY FIXED EFFECTS BEAT POOLED OLS", "Eliminating Omitted Variable Bias (Figure 4A vs 4B)", INDIGO, [
            "In raw pooled data (Figure 4A), the Philippines has low mortality (~1%) despite low ART (5%–41%).",
            "Reason: The Philippine cohort is newly infected and young, not yet at late-stage AIDS.",
            "Within-country Fixed Effects (Figure 4B) demean each country by its own baseline, isolating the true survival slope (β = -0.0491)."
        ]),
        ("2. WHY GDP CONTROL SHARPENED THE SLOPE", "Understanding Model 4 (β = -0.0624, R² = 73.1%)", TEAL, [
            "From 2010 to 2025, GDP grew across all SEA nations, including Indonesia and the Philippines where deaths rose.",
            "Controlling for log(GDP PPP) separates secular economic growth from programmatic ART scale-up.",
            "White's robust standard errors (HC1) account for heteroskedasticity across country sizes."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(def_cards17):
        tf = add_card(s17, 0.70 + i * 6.08, 1.38, 5.85, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=15, space_after=12)

    # =========================================================================
    # SLIDE 18: FIGURE 5 FULL-SCREEN VISUAL (GDP VS ART COVERAGE)
    # =========================================================================
    add_full_figure_slide(
        18,
        "Macroeconomic Wealth vs. ART Coverage in SEA (2025)",
        "SOCIOECONOMIC DETERMINANTS • FIGURE 5 VISUALIZATION",
        "fig5_gdp_vs_art_coverage_disparity.png",
        "TAKEAWAY: Cross-sectional correlation between GDP per capita (PPP) and ART coverage is weak (r = +0.149), proving policy outweighs wealth.",
        banner_color=TEAL, banner_bg=LIGHT_TEAL
    )

    # =========================================================================
    # SLIDE 19: THE HEALTH FINANCING PARADOX: POLICY OVER WEALTH
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s19, 19, "The Health Financing Paradox: Why Policy Beats GDP", "POLITICAL ECONOMY OF HIV SERVICE DELIVERY IN SOUTHEAST ASIA")

    fin_cards19 = [
        ("1. LOW-INCOME OVERACHIEVERS", "Cambodia ($7,300) & Myanmar ($5,137)", TEAL, [
            "Despite lower-middle income status, Cambodia (95% ART) and Myanmar (73% ART) beat wealthier peers.",
            "Driven by Global Fund/PEPFAR grants, centralized procurement, and NGO-community clinics.",
            "Proves donor-backed vertical execution can overcome low national GDP."
        ]),
        ("2. MIDDLE-INCOME LAGGARDS", "Indonesia ($15,091) & Philippines ($10,748)", CRIMSON, [
            "Higher national GDP does not automatically reach marginalized key populations.",
            "Decentralized municipal health financing and stigma against MSM/PWID impede linkage.",
            "Result: >50% of PLHIV remain untreated despite strong macroeconomic growth."
        ]),
        ("3. DOMESTIC UHC BENCHMARK", "Thailand ($22,432) vs. Malaysia ($35,461)", NAVY, [
            "Thailand embedded universal ART into its domestic Universal Coverage Scheme (82% ART).",
            "Malaysia ($35,461 PPP) succeeded in PWID harm reduction but lags in 1st-95 testing (66%).",
            "Lesson: Domestic UHC financing + stigma-free testing is the gold standard."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(fin_cards19):
        tf = add_card(s19, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=14.8, space_after=12)

    # =========================================================================
    # SLIDE 20: METHODOLOGICAL BOUNDARIES & LIMITATIONS (2x2 GRID)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s20, 20, "Methodological Boundaries & Surveillance Limitations", "SCIENTIFIC TRANSPARENCY & EPIDEMIOLOGICAL RIGOR")

    lim_cards20 = [
        ("1. SPECTRUM / EPP MODELED ESTIMATES", NAVY, LIGHT_INDIGO,
         "National HIV counts are compartmental model outputs calibrated to sentinel surveys, not raw census tallies. Regression slopes reflect both empirical surveillance and structural survival parameters."),
        ("2. ECOLOGICAL FALLACY BOUNDARY", CRIMSON, LIGHT_RED,
         "Our unit of analysis is the country-year (N = 144). Associations demonstrate population-level health-system effectiveness and must not be extrapolated to individual patient hazard ratios."),
        ("3. CENSORING & MICROSTATE SUPPRESSION", TEAL, LIGHT_TEAL,
         "Bounded strings ('<100', '<0.1%', '>98%') are parsed at their numeric threshold, and suppressed microstate cells (Brunei '...', Singapore cascade) are excluded without synthetic imputation."),
        ("4. SUB-NATIONAL CONFLICT HETEROGENEITY", AMBER, LIGHT_AMBER,
         "National aggregates for Myanmar mask disparities between urban centers (Yangon, Mandalay) and conflict-affected border states (Kachin, Shan, Sagaing) where clinic disruptions are sharpest.")
    ]
    for i, (head, col, bg, body) in enumerate(lim_cards20):
        col_idx = i % 2
        row_idx = i // 2
        x = 0.70 + col_idx * 6.08
        y = 1.38 + row_idx * 2.78
        tf = add_card(s20, x, y, 5.85, 2.55, bg_color=bg, border_color=col, accent_color=col, accent_pos="left", accent_thickness=0.12)
        p = tf.paragraphs[0]; p.text = head; p.font.size = Pt(15.5); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(8)
        p = tf.add_paragraph(); p.text = body; p.font.size = Pt(14.5); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 21: ACTIONABLE PUBLIC-HEALTH & CLINICAL RECOMMENDATIONS
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(s21, 21, "Actionable Public-Health & Clinical Recommendations", "EVIDENCE-BASED INTERVENTIONS BY EPIDEMIOLOGICAL ARCHETYPE")

    rec_cards21 = [
        ("1. MYANMAR (ARCHETYPE B)", "Conflict-Resilient HIV Care", CRIMSON, [
            "Scale 6-month Multi-Month Dispensing (MMD) of TLD to buffer supply-chain shocks.",
            "Expand mobile NGO and peer-led ART delivery in conflict zones (Kachin, Shan, Sagaing).",
            "Deploy portable patient records for internally displaced PLHIV."
        ]),
        ("2. PHILIPPINES & INDONESIA", "Emergency Testing & Linkage", AMBER, [
            "Remove adolescent consent barriers and scale up HIV self-testing & PrEP in the Philippines.",
            "Mandate Same-Day ART Initiation to close Indonesia's 28% linkage gap.",
            "Prioritize the 438,700 untreated PLHIV across both countries."
        ]),
        ("3. THAILAND, CAMBODIA & VIET NAM", "Last-Mile Elimination & UHC", TEAL, [
            "Transition donor-funded key-population clinics into domestic UHC budgets.",
            "Deploy index-partner testing and long-acting injectable PrEP (CAB-LA).",
            "Institutionalize ASEAN cross-border surveillance exchanges."
        ])
    ]
    for i, (title, sub, col, bullets) in enumerate(rec_cards21):
        tf = add_card(s21, 0.70 + i * 4.06, 1.38, 3.80, 5.42, accent_color=col, accent_pos="top", accent_thickness=0.10)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf.add_paragraph(); p.text = sub; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(14)
        add_bullets(tf, bullets, font_size=14.8, space_after=12)

    # =========================================================================
    # SLIDE 22: CLOSING EXECUTIVE SUMMARY & PORTFOLIO DEFENSE
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    bg22 = s22.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg22.fill.solid(); bg22.fill.fore_color.rgb = NAVY_DARK; bg22.line.fill.background()

    tb22 = s22.shapes.add_textbox(Inches(0.75), Inches(0.50), Inches(11.83), Inches(1.25))
    tf22 = tb22.text_frame; tf22.word_wrap = True
    p = tf22.paragraphs[0]; p.text = "EXECUTIVE SUMMARY & PORTFOLIO TAKEAWAYS"; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = RGBColor(94, 234, 212); p.space_after = Pt(4)
    p = tf22.add_paragraph(); p.text = "Bridging Clinical Medicine, Surveillance & Data Engineering"; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = WHITE

    summary_blocks = [
        ("1. VERIFIED MULTI-SOURCE PIPELINE", "6,624 Global Country-Years (1990–2025)",
         "End-to-end Python & SQLite star-schema pipeline integrating UNAIDS 2026, WHO GHO, and World Bank WDI with 100% programmatic reconciliation."),
        ("2. MYANMAR'S TRIUMPH & FRAGILITY", "-63.3% Deaths (2010–25) | +11.6% Crisis Spike (2022)",
         "Rapid ART expansion (12% → 73%) saved tens of thousands of lives, while the 2021–2022 rebound proves uninterrupted ART supply chains are vital."),
        ("3. REGIONAL BIFURCATION", "58.8% of Untreated HIV in Indonesia & Philippines",
         "While Cambodia (95% ART) and Thailand (82% ART) near epidemic control, the Philippines (+639% new infections) and Indonesia (291.2k untreated) lag."),
        ("4. ECONOMETRIC PROOF OF ART IMPACT", "β = -0.0491 (p < 0.00001, Within R² = 68.7%)",
         "Fixed-effects panel modeling proves that within-country ART expansion—not aggregate GDP per capita (r = +0.149)—drives AIDS survival.")
    ]
    for i, (s_head, s_metric, s_body) in enumerate(summary_blocks):
        col_idx = i % 2
        row_idx = i // 2
        bx = 0.75 + col_idx * 6.04
        by = 1.90 + row_idx * 2.32
        b_card = s22.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(by), Inches(5.78), Inches(2.08))
        b_card.fill.solid(); b_card.fill.fore_color.rgb = RGBColor(27, 54, 93)
        b_card.line.color.rgb = RGBColor(71, 85, 105); b_card.line.width = Pt(1.2)
        btf = b_card.text_frame; btf.word_wrap = True
        btf.margin_left = btf.margin_right = Inches(0.22); btf.margin_top = Inches(0.18)

        p1 = btf.paragraphs[0]; p1.text = s_head; p1.font.size = Pt(13.5); p1.font.bold = True; p1.font.color.rgb = RGBColor(248, 113, 113); p1.space_after = Pt(3)
        p2 = btf.add_paragraph(); p2.text = s_metric; p2.font.size = Pt(16.5); p2.font.bold = True; p2.font.color.rgb = RGBColor(94, 234, 212); p2.space_after = Pt(5)
        p3 = btf.add_paragraph(); p3.text = s_body; p3.font.size = Pt(13.8); p3.font.color.rgb = RGBColor(226, 232, 240)

    foot22 = s22.shapes.add_textbox(Inches(0.75), Inches(6.75), Inches(11.83), Inches(0.45))
    tf_f22 = foot22.text_frame
    pf22 = tf_f22.paragraphs[0]
    pf22.text = f"Thank You  •  Clinical & Epidemiological Research Portfolio  •  Slide {TOTAL_SLIDES} of {TOTAL_SLIDES}"
    pf22.font.size = Pt(14); pf22.font.bold = True; pf22.font.color.rgb = WHITE

    # Save outputs
    out_pres = os.path.join(pres_dir, "hiv_epidemiology_research_briefing.pptx")
    out_rep = os.path.join(reports_dir, "hiv_epidemiology_research_briefing.pptx")
    prs.save(out_pres)
    shutil.copy2(out_pres, out_rep)
    print(f"Saved presentation -> {out_pres} ({os.path.getsize(out_pres):,} bytes)")
    print(f"Copied presentation -> {out_rep} ({os.path.getsize(out_rep):,} bytes)")


if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    create_deck(base)
