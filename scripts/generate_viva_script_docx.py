"""
TabTime: Viva Voce Defense & Academic Supervisor Briefing Script Generator
Generates a comprehensive, professional Word (.docx) document for York St John University
Module: LDC6005M Individual Research Project (Component 3: Oral Defense & Viva Voce)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

WORKSPACE_DIR = r"D:\My Project\Browser Extenstion project"
OUTPUT_DOCX_PRIMARY = os.path.join(WORKSPACE_DIR, "documents", "reports", "TabTime_Viva_and_Supervisor_Explanation_Script.docx")
OUTPUT_DOCX_ROOT = os.path.join(WORKSPACE_DIR, "TabTime_Viva_and_Supervisor_Explanation_Script.docx")

# Styling Palette
HEX_NAVY = "0F172A"       # Primary Headings & Dark accents (#0F172A)
HEX_BLUE = "1D4ED8"       # Primary Accent & Badges (#1D4ED8)
HEX_CYAN = "0284C7"       # Secondary Accent (#0284C7)
HEX_SLATE = "475569"      # Subheadings & Metadata (#475569)
HEX_BG_CARD = "F8FAFC"    # Callout background (#F8FAFC)
HEX_BG_ALT = "F1F5F9"     # Table alternating rows (#F1F5F9)
HEX_BORDER = "CBD5E1"     # Border grey (#CBD5E1)
HEX_GREEN = "059669"      # Success / Confirmed badges (#059669)
HEX_AMBER = "D97706"      # Warning / Cues (#D97706)
HEX_RED = "DC2626"        # Critical alerts (#DC2626)

COLOR_NAVY = RGBColor(15, 23, 42)
COLOR_BLUE = RGBColor(29, 78, 216)
COLOR_CYAN = RGBColor(2, 132, 199)
COLOR_SLATE = RGBColor(71, 85, 105)
COLOR_MUTED = RGBColor(100, 116, 139)
COLOR_GREEN = RGBColor(5, 150, 105)
COLOR_AMBER = RGBColor(217, 119, 6)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table_borders(tbl, border_color=HEX_BORDER):
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_BLUE}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_callout_box(doc, title, paragraphs_text, border_color=HEX_BLUE, bg_color=HEX_BG_CARD, badge=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=130, bottom=130, left=180, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(4)
    p0.paragraph_format.line_spacing = 1.15
    if badge:
        run_badge = p0.add_run(f"[{badge}] ")
        run_badge.font.name = "Segoe UI"
        run_badge.font.size = Pt(9.5)
        run_badge.font.bold = True
        run_badge.font.color.rgb = COLOR_BLUE if border_color == HEX_BLUE else (COLOR_AMBER if border_color == HEX_AMBER else (COLOR_GREEN if border_color == HEX_GREEN else COLOR_CYAN))

    run_title = p0.add_run(title)
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(10.5)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY

    for pt in paragraphs_text:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(pt)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_NAVY

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_header_footer(doc):
    for s_idx, section in enumerate(doc.sections):
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "TabTime: Viva Voce Defense & Academic Supervisor Briefing Script | York St John University"
        hp.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        hp.style.font.name = "Calibri"
        hp.style.font.size = Pt(8.5)
        hp.style.font.color.rgb = RGBColor(100, 116, 139)
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "LDC6005M Individual Research Project | Component 3 Oral Defense & Viva Voce Script"
        fp.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        fp.style.font.name = "Calibri"
        fp.style.font.size = Pt(8.5)
def add_slide_section(doc, slide_num, title, category, duration, visual_desc, physical_cues, spoken_script, transition_text):
    """Adds a structured slide section to the document."""
    h2 = doc.add_heading(level=2)
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    r_num = h2.add_run(f"Slide {slide_num:02d}: ")
    r_num.font.name = "Segoe UI"
    r_num.font.size = Pt(14)
    r_num.font.bold = True
    r_num.font.color.rgb = COLOR_BLUE
    
    r_title = h2.add_run(title)
    r_title.font.name = "Segoe UI"
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    # Metadata Strip (Table)
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(2.3)
    tbl.columns[2].width = Inches(2.0)
    style_table_borders(tbl, HEX_BORDER)

    meta_items = [
        ("SECTION / CATEGORY", category),
        ("TIME ALLOCATION", duration),
        ("SLIDE TEMPLATE", f"Slide #{slide_num} (Animated)")
    ]
    for c_idx, (m_label, m_val) in enumerate(meta_items):
        cell = tbl.cell(0, c_idx)
        set_cell_background(cell, HEX_BG_ALT)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r_lbl = p.add_run(f"{m_label}: ")
        r_lbl.font.name = "Segoe UI"
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_SLATE
        r_v = p.add_run(m_val)
        r_v.font.name = "Segoe UI"
        r_v.font.size = Pt(8.5)
        r_v.font.bold = True
        r_v.font.color.rgb = COLOR_BLUE if c_idx == 1 else COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Visual Description & Screen Content Callout
    add_callout_box(
        doc,
        "VISUAL LAYOUT & SCREEN CONTENT",
        [visual_desc],
        border_color=HEX_CYAN,
        bg_color=HEX_BG_CARD,
        badge="SCREEN DISPLAY"
    )

    # Delivery & Physical Cues Callout
    add_callout_box(
        doc,
        "PRESENTATION CUES & PHYSICAL CHOREOGRAPHY",
        physical_cues,
        border_color=HEX_AMBER,
        bg_color="FFFBEB",
        badge="ACTION CUES"
    )

    # Verbatim Spoken Text
    p_lead = doc.add_paragraph()
    p_lead.paragraph_format.space_before = Pt(6)
    p_lead.paragraph_format.space_after = Pt(4)
    r_lead = p_lead.add_run("🎙️ VERBATIM SPOKEN SCRIPT (Read with confident, steady academic delivery):")
    r_lead.font.name = "Segoe UI"
    r_lead.font.size = Pt(11)
    r_lead.font.bold = True
    r_lead.font.color.rgb = COLOR_BLUE

    for para in spoken_script:
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(3)
        p_sp.paragraph_format.space_after = Pt(6)
        p_sp.paragraph_format.line_spacing = 1.2
        r_sp = p_sp.add_run(f'"{para}"')
        r_sp.font.name = "Calibri"
        r_sp.font.size = Pt(10.5)
        r_sp.font.color.rgb = COLOR_NAVY

    # Transition Callout
    if transition_text:
        add_callout_box(
            doc,
            "TRANSITION TO NEXT SLIDE",
            [transition_text],
            border_color=HEX_GREEN,
            bg_color="F0FDF4",
            badge="SEGUE"
        )

    # Dividing rule / space
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(12)
    r_div = p_div.add_run("―" * 48)
    r_div.font.color.rgb = RGBColor(203, 213, 225)
    p_div.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

def build_script_document():
    print("Initializing Word Document...")
    doc = docx.Document()
    add_header_footer(doc)

    # Set normal style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_NAVY

    # =========================================================================
    # PART 1: FRONT MATTER & OFFICIAL YORK ST JOHN UNIVERSITY COVERSHEET
    # =========================================================================
    print("Building Part 1: Front Matter & Declarations...")
    
    # Title Block
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("YORK ST JOHN UNIVERSITY\nSCHOOL OF SCIENCE, TECHNOLOGY & HEALTH")
    r_inst.font.name = "Segoe UI"
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_SLATE

    p_title = doc.add_paragraph()
    p_title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("TAB TIME: VIVA VOCE ORAL DEFENSE &\nACADEMIC SUPERVISOR EXPLANATION SCRIPT")
    r_title.font.name = "Segoe UI"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management\nModule: LDC6005M Individual Research Project | Component 3: Oral Presentation & Viva Voce")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_BLUE

    # Coversheet Table
    tbl_cov = doc.add_table(rows=8, cols=2)
    tbl_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cov.autofit = False
    tbl_cov.columns[0].width = Inches(3.0)
    tbl_cov.columns[1].width = Inches(3.5)
    style_table_borders(tbl_cov, HEX_BORDER)

    coversheet_meta = [
        ("The Coversheet", "Module: LDC6005M Individual Research Project (Component 3)"),
        ("Student Name (unless anonymised):", "[Student Name / Candidate]"),
        ("Student Number (as shown on student ID card):", "[Student ID Number]"),
        ("Assessment Component Number:", "Component 3 (Oral Presentation, Viva Voce & Demonstration)"),
        ("Assessment Type:", "Technical Viva Voce Presentation & System Defense"),
        ("Word Count / Duration / Limits:", "20 Minutes Oral Presentation + 10 Minutes Defense Q&A (~8,500 Words Script)"),
        ("Attempt Number:", "Attempt 1 (First Sit)"),
        ("Date of Submission / Examination:", "Academic Year 2025 / 2026 (June 2026)")
    ]
    for r_idx, (c0, c1) in enumerate(coversheet_meta):
        cell0 = tbl_cov.cell(r_idx, 0)
        cell1 = tbl_cov.cell(r_idx, 1)
        set_cell_background(cell0, HEX_BG_ALT if r_idx % 2 == 0 else HEX_BG_CARD)
        set_cell_background(cell1, HEX_BG_ALT if r_idx % 2 == 0 else HEX_BG_CARD)
        set_cell_margins(cell0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell1, top=70, bottom=70, left=100, right=100)

        p0 = cell0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(c0)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_NAVY

        p1 = cell1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(c1)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.bold = (r_idx == 0 or r_idx == 3)
        r1.font.color.rgb = COLOR_BLUE if (r_idx == 0 or r_idx == 3) else COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Formal Declarations Table (Table 5 equivalent)
    h_decl = doc.add_heading(level=3)
    h_decl.paragraph_format.space_before = Pt(8)
    h_decl.paragraph_format.space_after = Pt(4)
    r_hd = h_decl.add_run("Formal Academic Declarations (York St John Academic Integrity Framework)")
    r_hd.font.name = "Segoe UI"
    r_hd.font.size = Pt(11)
    r_hd.font.bold = True
    r_hd.font.color.rgb = COLOR_NAVY

    tbl_decl = doc.add_table(rows=3, cols=2)
    tbl_decl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_decl.autofit = False
    tbl_decl.columns[0].width = Inches(5.0)
    tbl_decl.columns[1].width = Inches(1.5)
    style_table_borders(tbl_decl, HEX_BORDER)

    decls_data = [
        ("Academic Misconduct Statement:\nI confirm that this work is entirely my own independent research and implementation. All external literature, libraries, and frameworks have been cited accurately in accordance with Harvard referencing.", "✔ Confirmed & Understood"),
        ("Generative Artificial Intelligence Statement:\nI confirm that AI tools were utilized strictly in compliance with York St John University guidelines, acting as an assistive coding/testing co-pilot without replacing independent intellectual work.", "✔ Confirmed & Compliant"),
        ("Module Learning Outcomes Satisfaction (LO1–LO5):\nI confirm that all five prescribed learning outcomes for LDC6005M have been rigorously evidenced across the dissertation, software artifact, and this viva defense.", "✔ All Prescribed LOs Met")
    ]
    for r_idx, (t0, t1) in enumerate(decls_data):
        c0 = tbl_decl.cell(r_idx, 0)
        c1 = tbl_decl.cell(r_idx, 1)
        set_cell_background(c0, HEX_BG_CARD if r_idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, HEX_BG_CARD if r_idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(t0)
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_NAVY

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(t1)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_GREEN

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Learning Outcomes Mapping Table
    h_lo = doc.add_heading(level=3)
    h_lo.paragraph_format.space_before = Pt(8)
    h_lo.paragraph_format.space_after = Pt(4)
    r_hlo = h_lo.add_run("Module Learning Outcomes Mapping Matrix (LDC6005M Component 3)")
    r_hlo.font.name = "Segoe UI"
    r_hlo.font.size = Pt(11)
    r_hlo.font.bold = True
    r_hlo.font.color.rgb = COLOR_NAVY

    tbl_lo = doc.add_table(rows=6, cols=3)
    tbl_lo.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lo.autofit = False
    tbl_lo.columns[0].width = Inches(1.5)
    tbl_lo.columns[1].width = Inches(2.6)
    tbl_lo.columns[2].width = Inches(2.4)
    style_table_borders(tbl_lo, HEX_BORDER)

    lo_headers = ["Learning Outcome", "Prescribed Competency (YSJ Brief)", "Evidenced in Viva & Project Artifact"]
    for c_idx, h in enumerate(lo_headers):
        cell = tbl_lo.cell(0, c_idx)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    lo_matrix = [
        ("LO1: Critical Review & Synthesis", "Critically analyze and synthesize literature within digital wellbeing, browser architecture, and HCI.", "Slide 8 comparative matrix, Chapter 2 review, evaluating 5 industry tools vs TabTime."),
        ("LO2: Scientific Method & Design", "Formulate a rigorous research methodology and design specification (DSR framework).", "Slides 7 & 9, DSR lifecycle, 5 SMART objectives, formal hypotheses H1 and H2."),
        ("LO3: Technical Engineering", "Implement a robust, production-ready software artifact conforming to modern standards.", "Slides 9 & 13, Manifest V3 service worker, IndexedDB, DeclarativeNetRequest compiler."),
        ("LO4: Empirical Evaluation", "Conduct systematic evaluation, statistical analysis, and performance benchmarking.", "Slides 10, 11 & 12, Google Forms survey (n=65), SUS score 89.04, stopwatch validation."),
        ("LO5: Professional Defense & Reflection", "Defend technical decisions professionally, reflecting on ethics, BCS code, and limitations.", "Slides 3, 13, 14 & 17, live demonstration, comprehensive Q&A defense playbook.")
    ]
    for r_idx, (c0, c1, c2) in enumerate(lo_matrix):
        cell0 = tbl_lo.cell(r_idx + 1, 0)
        cell1 = tbl_lo.cell(r_idx + 1, 1)
        cell2 = tbl_lo.cell(r_idx + 1, 2)
        set_cell_background(cell0, HEX_BG_ALT if r_idx % 2 == 0 else "FFFFFF")
        set_cell_background(cell1, HEX_BG_ALT if r_idx % 2 == 0 else "FFFFFF")
        set_cell_background(cell2, HEX_BG_ALT if r_idx % 2 == 0 else "FFFFFF")
        set_cell_margins(cell0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(cell1, top=60, bottom=60, left=80, right=80)
        set_cell_margins(cell2, top=60, bottom=60, left=80, right=80)

        for c, txt, bold in [(cell0, c0, True), (cell1, c1, False), (cell2, c2, False)]:
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(txt)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.bold = bold
            r.font.color.rgb = COLOR_BLUE if bold else COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # PART 2: EXECUTIVE OVERVIEW & PACING GUIDELINES
    # =========================================================================
    print("Building Part 2: Executive Overview & Pacing Guidelines...")
    h1_p2 = doc.add_heading(level=1)
    h1_p2.paragraph_format.space_before = Pt(0)
    h1_p2.paragraph_format.space_after = Pt(6)
    r = h1_p2.add_run("Part 1: Executive Overview & Viva Pacing Guidelines")
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    add_callout_box(
        doc,
        "ORAL DEFENSE STRUCTURE & TIME MANAGEMENT PROTOCOL",
        [
            "The LDC6005M Viva Voce examination is strictly scheduled for a 30-minute allocation: 20 minutes of uninterrupted candidate presentation and technical demonstration, followed by 10 minutes of panel cross-examination and technical defense.",
            "Target Verbal Cadence: Maintain a steady, articulate pace of 130 to 140 words per minute. Do not rush through mathematical formulations or architecture slides; examiners award high credit for calm, authoritative composure and precise technical terminology.",
            "Visual Cue Signaling: Throughout this document, specific cues guide your physical delivery: [SLIDE CUE] indicates when to advance slides, [TIME: MM:SS] marks running duration, [ACTION / GESTURE] dictates physical engagement, and [VERBATIM SPOKEN SCRIPT] provides your exact spoken script."
        ],
        border_color=HEX_BLUE,
        bg_color=HEX_BG_CARD,
        badge="EXAM BLUEPRINT"
    )

    p_pace = doc.add_paragraph()
    p_pace.paragraph_format.space_before = Pt(6)
    p_pace.paragraph_format.space_after = Pt(4)
    r = p_pace.add_run("Master 20-Minute Cumulative Timing Timeline:")
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    tbl_timing = doc.add_table(rows=6, cols=4)
    tbl_timing.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_timing.autofit = False
    tbl_timing.columns[0].width = Inches(1.2)
    tbl_timing.columns[1].width = Inches(2.2)
    tbl_timing.columns[2].width = Inches(1.8)
    tbl_timing.columns[3].width = Inches(1.3)
    style_table_borders(tbl_timing, HEX_BORDER)

    t_headers = ["Presentation Phase", "Slide Range & Content", "Time Window", "Target Pacing"]
    for c_idx, h in enumerate(t_headers):
        cell = tbl_timing.cell(0, c_idx)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    timing_rows = [
        ("Phase 1: Setup & Context", "Slides 1 to 4: Title, Coversheet, Declarations, Agenda", "00:00 – 02:45 (2m 45s)", "Clear, steady, welcoming"),
        ("Phase 2: Problem & Lit", "Slides 5 to 8: Digital Crisis, Motives, Aims, Lit Review", "02:45 – 07:30 (4m 45s)", "Compelling problem hook"),
        ("Phase 3: DSR & Architecture", "Slides 9 to 10: 3-Layer Design, Telemetry Pipeline", "07:30 – 10:15 (2m 45s)", "Rigorous technical depth"),
        ("Phase 4: Results & Analysis", "Slides 11 to 13: SUS 89.04, Hypotheses, Challenges", "10:15 – 14:45 (4m 30s)", "Empirical data emphasis"),
        ("Phase 5: Discussion & Wrap", "Slides 14 to 20: BCS Ethics, Roadmap, Summary, Q&A", "14:45 – 20:00 (5m 15s)", "Authoritative conclusion")
    ]
    for r_idx, row in enumerate(timing_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_timing.cell(r_idx + 1, c_idx)
            set_cell_background(cell, HEX_BG_ALT if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.bold = (c_idx == 0 or c_idx == 2)
            r.font.color.rgb = COLOR_BLUE if (c_idx == 0 or c_idx == 2) else COLOR_NAVY

    doc.add_page_break()

    # =========================================================================
    # PART 3: ACADEMIC SUPERVISOR EXPLANATION & DEFENSE BRIEFING GUIDE
    # =========================================================================
    print("Building Part 3: Supervisor Explanation & Progress Guide...")
    h1_sup = doc.add_heading(level=1)
    h1_sup.paragraph_format.space_before = Pt(0)
    h1_sup.paragraph_format.space_after = Pt(6)
    r = h1_sup.add_run("Part 2: Academic Supervisor Explanation & Progress Defense Briefing")
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_sup_intro = doc.add_paragraph()
    p_sup_intro.paragraph_format.space_before = Pt(2)
    p_sup_intro.paragraph_format.space_after = Pt(6)
    p_sup_intro.paragraph_format.line_spacing = 1.15
    r = p_sup_intro.add_run(
        "This section is engineered specifically for one-on-one progress meetings with your academic project supervisor and for addressing critical supervisory inquiries prior to the final viva voce. It arms you with concise conceptual summaries, pedagogical justifications, software trade-off analyses, and structured rebuttals to common supervisory critiques."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)

    # 3.1 The 2-Minute Elevator Pitch
    h2_sp1 = doc.add_heading(level=2)
    h2_sp1.paragraph_format.space_before = Pt(12)
    h2_sp1.paragraph_format.space_after = Pt(4)
    r = h2_sp1.add_run("2.1 The 2-Minute Executive Project Pitch to Your Supervisor")
    r.font.name = "Segoe UI"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE

    add_callout_box(
        doc,
        "VERBATIM 2-MINUTE SUPERVISOR BRIEFING",
        [
            "\"Good morning / afternoon [Supervisor Name]. To summarize where TabTime stands: over 80% of modern academic study and digital knowledge work is conducted directly inside web browsers. While browsers provide seamless access to research tools, their frictionless design exposes users to algorithmic distraction and constant attention fragmentation. Research shows recovering from an interruption takes up to 23 minutes.",
            "Commercial time trackers like RescueTime and Toggl attempt to address this, but they suffer from two major flaws: first, they practice surveillance capitalism—harvesting full user URL streams and timestamps to remote clouds; second, they enforce a rigid binary dichotomy—offering either passive retrospective logging with zero intervention, or heavy-handed website blocking that frustrates users.",
            "TabTime bridges this gap by engineering an open-source, client-side browser extension under the modern Manifest V3 specification. It delivers millisecond-accurate automated tracking, mathematical productivity scoring, interactive Chart.js analytics, and non-coercive focus interventions powered by dynamic declarativeNetRequest redirection. Most importantly, it operates under a strict Privacy-by-Design architecture: 100% of telemetry and logs remain isolated inside the browser's local IndexedDB, with zero external network calls.",
            "We empirically evaluated TabTime across 65 participants. The system achieved a composite System Usability Scale (SUS) score of 89.04 out of 100—placing it in the top 10th percentile (Grade A). Automated ground-truth testing proved timing accuracy within ±1.8 seconds of an external stopwatch with a lightweight memory footprint of only 14 to 22 MB of RAM. Both research hypotheses—enhancing digital habit awareness (95.4%) and reducing distractions (93.8%)—were confirmed. All deliverables, codebases, and viva assets are complete, tested, and ready for defense.\""
        ],
        border_color=HEX_BLUE,
        bg_color=HEX_BG_CARD,
        badge="SPOKEN ELEVATOR PITCH"
    )

    # 3.2 Pedagogical & Theoretical Justification
    h2_sp2 = doc.add_heading(level=2)
    h2_sp2.paragraph_format.space_before = Pt(14)
    h2_sp2.paragraph_format.space_after = Pt(4)
    r = h2_sp2.add_run("2.2 Theoretical & Pedagogical Grounding: How Theory Translates to Code")
    r.font.name = "Segoe UI"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.add_run("When your supervisor asks: ").bold = True
    p.add_run("\"What academic literature directly informed your technical design, and how is it reflected in your code?\", ")
    p.add_run("present the following three-pillar theoretical mapping:")

    tbl_theories = doc.add_table(rows=4, cols=3)
    tbl_theories.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_theories.autofit = False
    tbl_theories.columns[0].width = Inches(1.8)
    tbl_theories.columns[1].width = Inches(2.2)
    tbl_theories.columns[2].width = Inches(2.5)
    style_table_borders(tbl_theories, HEX_BORDER)

    th_headers = ["Theoretical Framework", "Seminal Literature Principle", "Operationalization in TabTime Implementation"]
    for c_idx, h in enumerate(th_headers):
        cell = tbl_theories.cell(0, c_idx)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    th_rows = [
        ("Self-Regulation Theory", "Bandura (1991): Human self-regulation depends on self-monitoring, judgment against personal standards, and self-reaction.", "Implemented via real-time productivity scoring (0-100), active toolbar donut badges, and instant visual categorization in popup.js."),
        ("Attention Restoration Theory (ART)", "Kaplan (1995): Directed attention fatigue can be mitigated through restorative breaks and mindful disengagement cues.", "Focus Mode does not use punitive locks; instead, declarativeNetRequest redirects distracting tabs to blocked.html with serene breathing nudges."),
        ("Cognitive Load Theory", "Sweller (1988): Extraneous cognitive load impairs task performance during digital knowledge work.", "Eliminated complex multi-layer menus. Created an ultra-clean popup (<300ms render) and offloaded historical trends to a dedicated dashboard.html.")
    ]
    for r_idx, row in enumerate(th_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_theories.cell(r_idx + 1, c_idx)
            set_cell_background(cell, HEX_BG_ALT if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.bold = (c_idx == 0)
            r.font.color.rgb = COLOR_BLUE if (c_idx == 0) else COLOR_NAVY

    # 3.3 Software Engineering Trade-Off Defense
    h2_sp3 = doc.add_heading(level=2)
    h2_sp3.paragraph_format.space_before = Pt(14)
    h2_sp3.paragraph_format.space_after = Pt(4)
    r = h2_sp3.add_run("2.3 Software Engineering Trade-Off Defense: Architecture Decisions")
    r.font.name = "Segoe UI"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE

    add_callout_box(
        doc,
        "CORE TECHNICAL ARCHITECTURAL JUSTIFICATIONS FOR SUPERVISORY SCRUTINY",
        [
            "1. Why Manifest V3 Instead of Legacy Manifest V2? Chrome and Firefox are permanently deprecating MV2. Building in MV3 guarantees production longevity, enhanced browser security, and compliance with modern W3C WebExtensions standards. While MV3 service workers terminate after 30 seconds of idle time, we engineered an event-driven state hydration mechanism via chrome.storage.local that saves session states prior to worker termination.",
            "2. Why DeclarativeNetRequest Instead of WebRequest Blocking? Legacy webRequest.onBeforeRequest with blocking permissions introduced severe browser latency and posed major security risks. DeclarativeNetRequest delegates URL rule matching directly to the browser's native C++ network stack, executing redirections at near-zero CPU overhead with zero risk of page tampering.",
            "3. Why IndexedDB Over Pure chrome.storage.local? Chrome's storage API is key-value based and has quota limits (typically 10MB without unlimitedStorage). TabTime generates time-series domain log entries with timestamps, durations, and categories. IndexedDB provides structured transactional indexing, multi-megabyte capacity, and ultra-fast composite range queries needed to render 30-day Chart.js analytics smoothly.",
            "4. Why Local-First Architecture Over Cloud Firebase / Supabase? Deploying a cloud database introduces severe GDPR compliance burdens, hosting maintenance, and vulnerability to data breaches. By maintaining 100% of telemetry on the local client machine, TabTime eliminates remote server attack vectors, guarantees user data sovereignty, and upholds BCS ethical guidelines."
        ],
        border_color=HEX_CYAN,
        bg_color=HEX_BG_CARD,
        badge="ENGINEERING JUSTIFICATIONS"
    )

    # 3.4 Pre-empting Supervisor Feedback & Critiques (8 Questions & Rebuttals)
    h2_sp4 = doc.add_heading(level=2)
    h2_sp4.paragraph_format.space_before = Pt(14)
    h2_sp4.paragraph_format.space_after = Pt(4)
    r = h2_sp4.add_run("2.4 Defending Critical Supervisor Questions & Objections")
    r.font.name = "Segoe UI"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE

    supervisor_qa = [
        (
            "Supervisor Objection 1: \"Why didn't you implement cloud sync? Wouldn't users want their time tracked across both their desktop and laptop?\"",
            "Candidate Rebuttal: While cross-device synchronization is convenient, introducing a centralized cloud backend immediately compromises the core research premise of TabTime—namely, evaluating whether high-utility productivity analytics can be achieved under a strict Privacy-by-Design paradigm. Commercial trackers like RescueTime upload granular browsing logs containing sensitive academic and personal URLs. Furthermore, under GDPR Article 25, data minimization is mandatory. In Chapter 8 (Future Work), we propose a privacy-preserving sync compromise: client-side zero-knowledge encrypted blobs stored on user-controlled storage (such as WebDAV or personal Google Drive) using the Web Cryptography API (AES-GCM-256), preserving privacy without centralized harvesting."
        ),
        (
            "Supervisor Objection 2: \"How do you know your 65 survey participants represent genuine users and not just biased friends or coursemates?\"",
            "Candidate Rebuttal: We designed our recruitment strategy using a stratified sampling approach across multiple cohorts. As demonstrated in Figure 6.1, our 65 participants consist of 47.7% undergraduate students, 27.7% corporate knowledge workers and software professionals, 13.8% university faculty and lecturers, and 10.8% postgraduate researchers. Furthermore, the survey was deployed across four distinct web browsers (Chrome, Brave, Edge, Firefox). The psychometric instrument used—Brooke's 10-item System Usability Scale—specifically includes alternating positive and negative polarity questions to detect and eliminate response acquiescence bias. The resulting 89.04 score is statistically robust."
        ),
        (
            "Supervisor Objection 3: \"What happens if a user leaves a YouTube tab playing music in the background while working in Google Docs? Does TabTime misattribute that time?\"",
            "Candidate Rebuttal: TabTime tracks active window and active tab focus exclusively through chrome.windows.onFocusChanged and chrome.tabs.onActivated listeners. If a YouTube tab is playing audio in the background while the user actively types in Google Docs, the active, focused tab is Google Docs. TabTime accurately attributes the elapsed time to Google Docs (Productive/Work). In addition, we implemented a 60-second idle debounce threshold using the chrome.idle API; if the user steps away from their keyboard while YouTube plays, TabTime suspends tracking after 60 seconds, preventing idle skewing."
        ),
        (
            "Supervisor Objection 4: \"Why did you choose a non-coercive focus blocker instead of a strict, unbreakable password lock? Won't students just disable it?\"",
            "Candidate Rebuttal: HCI and behavioral psychology literature (Mark et al., 2008; Bandura, 1991) demonstrates that rigid, coercive blocking induces psychological reactance—users experience frustration, view the software as punitive, and either uninstall the extension or bypass it via incognito windows. TabTime's focus mode leverages behavioral nudge theory: by redirecting the user to blocked.html with serene imagery and mindful reflection cues, it breaks the unconscious impulse loop and invites intentional self-regulation. Our survey results validate this approach: 92.3% of participants rated the Focus Mode as highly effective, and 93.8% reported a substantial decrease in task interruptions."
        )
    ]

    for q_title, a_text in supervisor_qa:
        add_callout_box(
            doc,
            q_title,
            [a_text],
            border_color=HEX_AMBER,
            bg_color="FFFBEB",
            badge="SUPERVISOR REBUTTAL"
        )

    doc.add_page_break()

    # =========================================================================
    # PART 4: SLIDE-BY-SLIDE MASTER VIVA VOCE PRESENTATION SPOKEN SCRIPT
    # =========================================================================
    print("Building Part 4: Slide-by-Slide Spoken Script (Slides 1-20)...")
    h1_slides = doc.add_heading(level=1)
    h1_slides.paragraph_format.space_before = Pt(0)
    h1_slides.paragraph_format.space_after = Pt(6)
    r = h1_slides.add_run("Part 3: Slide-by-Slide Master Viva Voce Presentation Spoken Script")
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_sl_desc = doc.add_paragraph()
    p_sl_desc.paragraph_format.space_before = Pt(2)
    p_sl_desc.paragraph_format.space_after = Pt(8)
    p_sl_desc.paragraph_format.line_spacing = 1.15
    r = p_sl_desc.add_run(
        "This is the complete, verbatim spoken delivery script for all 20 slides of the TabTime IRP Viva Presentation (TabTime_IRP_Viva_Presentation_Final.pptx). It includes exact visual descriptions, physical choreography, slide animation cues, verbatim speech text, and seamless slide transitions. Total allocated duration: 20 minutes."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # SLIDE 1
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=1,
        title="Title Slide: Mindful Digital Engagement",
        category="MODULE LDC6005M VIVA DEFENSE",
        duration="00:00 – 00:45 (45 Seconds)",
        visual_desc="Displays the official York St John University template title slide featuring the TabTime application icon (128x128px), the prominent blue category badge 'LDC6005M INDIVIDUAL RESEARCH PROJECT VIVA VOCE', the main title 'TAB TIME: A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management', and candidate metadata (Candidate Name, Student ID, BSc Hons Computer Science, School of Science, Technology & Health, June 2026).",
        physical_cues=[
            "[00:00] Stand erect, hands comfortably clasped or resting on lectern. Make direct eye contact with the examination panel.",
            "[00:05] Offer a warm, professional greeting. Do not fidget with the clicker or touch your laptop.",
            "[00:30] Smile slightly when introducing TabTime, conveying confidence in your engineering artifact."
        ],
        spoken_script=[
            "Good morning, esteemed members of the examination committee, my supervisor, and panel assessors. Welcome to the oral defense of my Individual Research Project for module LDC6005M.",
            "My name is [Student Name], candidate number [Student ID Number], pursuing the Bachelor of Science with Honours in Computer Science here at York St John University. Today, I am proud to present TabTime—a privacy-preserving, client-side browser extension engineered under Manifest V3 to promote digital wellbeing, real-time temporal awareness, visual productivity analytics, and focus management.",
            "Over the next twenty minutes, I will guide you through the contextual background, theoretical framework, engineering architecture, empirical evaluation across 65 participants, and critical contributions of this project."
        ],
        transition_text="\"Before diving into our research problem, allow me to present the official assessment coversheet and institutional compliance declarations for this examination.\""
    )

    # -------------------------------------------------------------
    # SLIDE 2
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=2,
        title="Assessment Coversheet & Administrative Transparency",
        category="ADMINISTRATIVE COMPLIANCE",
        duration="00:45 – 01:15 (30 Seconds)",
        visual_desc="Standardized York St John University Assessment Coversheet table (Table 1) detailing Module LDC6005M, Student Name, Student ID Number, Component 3 (Oral Presentation & Technical Viva Voce), First Sit Attempt, Academic Session 2025/2026, and the 20-minute presentation plus 10-minute panel defense time allocation.",
        physical_cues=[
            "[00:45] Advance to Slide 2 using the remote clicker. Keep your gesture subtle.",
            "[00:50] Point briefly toward the coversheet table to confirm institutional alignment.",
            "[01:05] Maintain an upright, respectful posture."
        ],
        spoken_script=[
            "Shown on screen is the official York St John University Assessment Coversheet for Component 3 of module LDC6005M. This assessment component represents the capstone technical viva voce and system demonstration.",
            "All administrative details—including candidate identification, first-sit declaration, and strict adherence to the prescribed 20-minute presentation and 10-minute panel defense format—have been verified and fully compliant with school regulations."
        ],
        transition_text="\"Turning to Slide 3, we address our formal declarations regarding academic misconduct, ethical AI usage, and learning outcomes satisfaction.\""
    )

    # -------------------------------------------------------------
    # SLIDE 3
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=3,
        title="Declarations & Critical Self-Assessment",
        category="ACADEMIC INTEGRITY & REFLECTION",
        duration="01:15 – 02:00 (45 Seconds)",
        visual_desc="Two distinct structured tables: Table 5 outlines three formal declarations (Academic Misconduct statement understood, Generative AI policy adherence confirmed, all five module learning outcomes LO1-LO5 comprehensively met) marked with prominent green checkmarks. Table 7 details the candidate's Critical Self-Assessment reflecting on technical mastery of Manifest V3, empirical evaluation rigor (n=65, SUS 89.04), and constructive reflections for future on-device NLP integration.",
        physical_cues=[
            "[01:15] Advance to Slide 3. Draw the panel's attention to the green verification badges.",
            "[01:30] Emphasize the Generative AI statement with clear, honest academic integrity.",
            "[01:45] Nod slightly when addressing the technical challenges overcome during Manifest V3 development."
        ],
        spoken_script=[
            "Slide 3 presents our formal academic declarations and critical self-reflection. I formally certify that this research and software implementation are entirely my own independent work.",
            "In strict accordance with York St John University's Generative AI policy, AI co-pilots were utilized transparently as assistive productivity tools for code syntax checking and unit test scaffold generation, without replacing independent engineering design.",
            "In reflecting on this project, our greatest engineering achievement was successfully overcoming Chrome's ephemeral 30-second service worker lifecycle to deliver a 99.85% accurate tracking engine. Our greatest empirical strength is a 65-participant study yielding a Grade A SUS score of 89.04. Constructively, future iterations will look to embed on-device WebAssembly NLP to eliminate manual domain categorization."
        ],
        transition_text="\"With these administrative foundations established, let us review the structural agenda for today's defense.\""
    )

    # -------------------------------------------------------------
    # SLIDE 4
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=4,
        title="Table of Contents: Presentation Roadmap",
        category="AGENDA & STRUCTURE",
        duration="02:00 – 02:45 (45 Seconds)",
        visual_desc="Five modern rounded cards organized in a clean staggered layout outlining the five core phases of the presentation: Phase 01: Context & Problem Statement; Phase 02: Aims, Objectives & Hypotheses; Phase 03: Literature Review & Benchmark; Phase 04: DSR Methodology & Architecture; Phase 05: Empirical Results & Discussion.",
        physical_cues=[
            "[02:00] Advance to Slide 4. Open your hands outward to indicate the holistic scope.",
            "[02:15] Sequentially sweep your hand across the five roadmap cards as you describe them.",
            "[02:35] Lower your voice slightly to build anticipation for Phase 1."
        ],
        spoken_script=[
            "To provide a clear roadmap for this defense, our presentation is structured into five cohesive phases.",
            "Phase 1 examines the digital wellbeing crisis, attention fragmentation, and the pervasive surveillance capitalism of current commercial trackers. Phase 2 defines our core research aim, five measurable objectives, and testable hypotheses. Phase 3 reviews seminal human-computer interaction literature and presents a 5-way comparative matrix.",
            "Phase 4 details our Design Science Research methodology, three-layer Manifest V3 architecture, and 65-participant telemetry pipeline. Finally, Phase 5 reveals our empirical results, System Usability Scale evaluation, engineering problem resolutions, and future directions."
        ],
        transition_text="\"Let us commence Phase 1 by exploring the modern digital wellbeing landscape and research context.\""
    )

    # -------------------------------------------------------------
    # SLIDE 5
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=5,
        title="Chapter 1: Introduction & Research Context",
        category="CHAPTER 1: INTRODUCTION",
        duration="02:45 – 03:45 (60 Seconds)",
        visual_desc="Left side: clean content card outlining the digital wellbeing landscape (frictionless web environments, over 80% browser-based knowledge work, attention fragmentation, 23-minute recovery cost from Mark et al. 2008, the TabTime solution, and privacy-by-design core). Right side: high-resolution conceptual diagram Figure 1.1 depicting the TabTime Mindful Digital Engagement Pipeline.",
        physical_cues=[
            "[02:45] Advance to Slide 5. Turn slightly toward the screen to reference Figure 1.1.",
            "[03:00] Point to the 23-minute statistic; pause for 1 second to let the cognitive impact sink in.",
            "[03:25] Emphasize the phrase 'Privacy-by-Design' with conviction."
        ],
        spoken_script=[
            "Turning to Chapter 1, contemporary academic study and professional knowledge work are overwhelmingly conducted within web browsers—exceeding 80% of daily computer interactions.",
            "While modern browsers provide frictionless access to global knowledge, collaboration tools, and research libraries, their very frictionlessness constitutes their greatest cognitive flaw. With a single click or keyboard shortcut, a user can instantly pivot from an academic journal into an algorithmic social media feed or entertainment vortex.",
            "Seminal HCI research by Dr. Gloria Mark and colleagues at UC Irvine demonstrated that recovering from a single digital interruption takes an average of 23 minutes and 15 seconds, creating immense cognitive switching costs, heightened cortisol levels, and severe loss of temporal awareness.",
            "TabTime was conceived to address this exact crisis: providing non-intrusive, millisecond-accurate time tracking, instantaneous visual feedback, and mindful focus interventions, engineered under a strict Privacy-by-Design ethos where 100% of telemetry remains on the client's machine."
        ],
        transition_text="\"This brings us to the core problem statement and research motives underpinning this study.\""
    )

    # -------------------------------------------------------------
    # SLIDE 6
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=6,
        title="Chapter 1: Problem Statement & Research Motives",
        category="CHAPTER 1: PROBLEM STATEMENT",
        duration="03:45 – 04:55 (70 Seconds)",
        visual_desc="Four balanced, rounded cards in a 2x2 grid highlighting the research motives: 1. Surveillance Capitalism in Trackers (amber badge, critique of RescueTime/Toggl cloud URL harvesting, Zuboff 2019, GDPR Art 5); 2. The Functional Binary Dichotomy (blue badge, passive logging vs rigid punitive blocking); 3. Lack of Real-Time Behavioral Nudges (navy badge, micro-distractions unnoticed during context switching); 4. The TabTime Research Opportunity (green badge, on-device sandbox merging tracking, scoring, and declarative blocking).",
        physical_cues=[
            "[03:45] Advance to Slide 6. Gesture toward the top-left amber card.",
            "[04:05] Move your gesture to the top-right blue card when discussing the binary dichotomy.",
            "[04:30] Conclude with the bottom-right green card, projecting enthusiasm for the TabTime solution."
        ],
        spoken_script=[
            "Our critical review of the digital productivity domain revealed three acute engineering and ethical deficiencies in existing commercial solutions.",
            "First is the pervasive issue of Surveillance Capitalism. Mainstream utilities such as RescueTime and Toggl mandate continuous cloud synchronization, harvesting complete URL strings, page titles, and timestamps to remote corporate servers. Under GDPR Article 5, this creates severe privacy vulnerabilities, exposing sensitive research, health, and personal data to cloud breaches and commercial profiling.",
            "Second is what we term the Functional Binary Dichotomy. Existing tools either offer passive retrospective dashboards that tell you how much time you wasted yesterday without intervening, or they enforce draconian, rigid website blocks that trigger frustration and prompt users to quickly uninstall the extension.",
            "Third is the absence of real-time behavioral nudges during active browsing. Users accumulate dozens of micro-distractions without realizing their cumulative loss of focus.",
            "The TabTime research opportunity lies in engineering a unified, privacy-first system that combines automated tracking, instant mathematical scoring, and non-coercive focus interventions entirely inside the browser's local sandbox."
        ],
        transition_text="\"To solve these problems, we formulated clear research aims, measurable objectives, and formal hypotheses.\""
    )

    # -------------------------------------------------------------
    # SLIDE 7
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=7,
        title="Chapter 1: Research Aims, Objectives & Hypotheses",
        category="CHAPTER 1: AIMS & OBJECTIVES",
        duration="04:55 – 06:00 (65 Seconds)",
        visual_desc="Left side: comprehensive card detailing the Overarching Project Aim, Central Research Question, and formal testable hypotheses H1 (active monitoring improves time awareness and self-regulation) and H2 (dynamic focus sessions significantly reduce distraction interruptions). Right side: Figure 1.2 diagram illustrating the hierarchical mapping of Aim, 5 SMART Objectives (FR-01 to FR-09), and verification criteria.",
        physical_cues=[
            "[04:55] Advance to Slide 7. Read the overarching aim with clear, deliberate articulation.",
            "[05:20] Point to the Central Research Question.",
            "[05:40] Emphasize Hypotheses H1 and H2 by counting on your fingers."
        ],
        spoken_script=[
            "Slide 7 establishes our formal academic scaffolding. Our overarching project aim is to design, develop, and empirically evaluate a privacy-preserving browser extension that promotes digital wellbeing and time awareness through real-time tracking, productivity analytics, and focus management.",
            "Our central research question asks: Can a browser extension combining automated time tracking, visual analytics, and focus management improve users' awareness of digital habits and reduce online distractions without compromising privacy?",
            "To answer this definitively, we formulated two testable research hypotheses:",
            "Hypothesis 1 posits that active monitoring via automated tracking and instantaneous visual feedback significantly improves temporal awareness and personal self-regulation.",
            "Hypothesis 2 posits that dynamic focus sessions with non-coercive redirection significantly reduce distraction-related interruptions during focused work.",
            "These hypotheses guided our five core functional objectives—from low-overhead background tracking to local IndexedDB storage and empirical user evaluation."
        ],
        transition_text="\"Let us examine how these objectives relate to existing literature and commercial benchmarks in Chapter 2.\""
    )

    # -------------------------------------------------------------
    # SLIDE 8
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=8,
        title="Chapter 2: Literature Review & Comparative Analysis",
        category="CHAPTER 2: LITERATURE REVIEW",
        duration="06:00 – 07:30 (90 Seconds)",
        visual_desc="Top card: theoretical foundations synthesizing Bandura's Self-Regulation Theory (1991), Kaplan's Attention Restoration Theory (1995), and the Manifest V3 paradigm shift. Bottom: 6x6 comprehensive comparative evaluation matrix benchmarking TabTime against RescueTime, Toggl Track, StayFocusd, and Forest across five technical metrics: 100% Local Privacy, Real-Time Productivity Score, Manifest V3 Support, Dynamic Rule Redirection, and Open Source License.",
        physical_cues=[
            "[06:00] Advance to Slide 8. Refer to the theoretical foundations at the top.",
            "[06:25] Direct attention to the comparative table below. Highlight the 'TabTime (Ours)' column.",
            "[06:55] Trace down the column, pointing out the green checkmarks against the red crosses of competitors."
        ],
        spoken_script=[
            "Our research is theoretically grounded in three foundational HCI and psychological frameworks: Albert Bandura's Social Cognitive Theory of Self-Regulation, Stephen Kaplan's Attention Restoration Theory, and John Sweller's Cognitive Load Theory.",
            "Furthermore, our work addresses the monumental architectural shift currently underway in web browsers: Google Chrome's transition to Manifest Version 3. MV3 deprecates persistent background scripts, enforces ephemeral service workers, and eliminates arbitrary remote code execution, demanding a complete redesign of extension telemetry.",
            "The comparative matrix on screen highlights why TabTime is unique compared to industry leaders:",
            "While RescueTime and Toggl require mandatory cloud synchronization and paid subscriptions, TabTime guarantees 100% on-device privacy via IndexedDB with zero cloud transmission.",
            "While StayFocusd and Forest rely on legacy Manifest V2 background scripts or simple gamified mobile timers, TabTime is built natively on Manifest V3, utilizing the modern declarativeNetRequest API for seamless network redirection without CPU lag.",
            "TabTime is the only tool that unifies local privacy, instant mathematical scoring, MV3 compliance, and an open-source architecture."
        ],
        transition_text="\"Having identified this research gap, let us examine our Design Science Research methodology and system architecture.\""
    )

    # -------------------------------------------------------------
    # SLIDE 9
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=9,
        title="Chapter 4 & 5: Design Science Methodology & Architecture",
        category="CHAPTER 4 & 5: METHODOLOGY",
        duration="07:30 – 09:00 (90 Seconds)",
        visual_desc="Left side: comprehensive card detailing the Design Science Research (DSR) paradigm (Hevner et al., 2004) and breaking down the Three-Layer System Architecture: 1. Presentation Layer (popup.html, dashboard.html, settings.html); 2. Logic Engine Layer (background.js MV3 service worker, event listeners, debounce timers); 3. Local Data Persistence Layer (storage.js, IndexedDB, chrome.storage.local). Right side: Figure 5.1 high-resolution diagram of the Three-Layer Architecture.",
        physical_cues=[
            "[07:30] Advance to Slide 9. Reference Hevner's DSR framework with academic authority.",
            "[07:55] Use your hands to depict the three vertical layers shown in Figure 5.1.",
            "[08:35] Emphasize the asynchronous separation between the service worker and IndexedDB."
        ],
        spoken_script=[
            "We adopted the Design Science Research framework established by Hevner and colleagues (2004). DSR is the preeminent methodology for information systems engineering, emphasizing the iterative creation and rigorous empirical evaluation of an innovative software artifact to solve an identified human problem.",
            "As shown in Figure 5.1, TabTime is architected around a strict Three-Layer Model:",
            "Layer 1 is the Presentation Layer, comprising our responsive popup for rapid daily checks, our full-screen analytics dashboard powered by Chart.js, and our user configuration interface.",
            "Layer 2 is the Logic Engine Layer, implemented inside background.js as a Manifest V3 service worker. It listens to chrome.windows.onFocusChanged, chrome.tabs.onActivated, and chrome.tabs.onUpdated events. It incorporates an idle detector that suspends tracking when user inactivity exceeds 60 seconds.",
            "Layer 3 is the Local Persistence Layer, encapsulated in storage.js. Rather than polluting browser storage with key-value blobs, we utilize native IndexedDB for time-series domain logs and chrome.storage.local for fast configuration caching, guaranteeing zero server communication."
        ],
        transition_text="\"Now let us inspect how empirical data was gathered and how our evaluation pipeline was structured.\""
    )

    # -------------------------------------------------------------
    # SLIDE 10
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=10,
        title="Chapter 4: Data Collection Process & Telemetry Pipeline",
        category="CHAPTER 4: DATA COLLECTION",
        duration="09:00 – 10:15 (75 Seconds)",
        visual_desc="Left side: dual-stream evaluation card explaining Stream 1 (automated client-side telemetry with 60-second idle debounce threshold) and Stream 2 (Google Forms empirical survey featuring 25 Likert-scale questions, 10-item SUS scale, and behavioral metrics). It outlines the 65-participant demographic profile (47.7% undergraduates, 27.7% knowledge workers, 10.8% postgraduates, 13.8% faculty; 78.5% Chrome, 10.8% Brave, 6.2% Edge, 4.6% Firefox). Right side: Figure 6.1 demographic breakdown chart.",
        physical_cues=[
            "[09:00] Advance to Slide 10. Gesture toward the dual-stream card.",
            "[09:30] Refer to the demographic distribution chart in Figure 6.1.",
            "[09:55] Highlight the cross-browser diversity (Chrome, Brave, Edge, Firefox)."
        ],
        spoken_script=[
            "To evaluate TabTime thoroughly, we executed a dual-stream evaluation methodology.",
            "Stream 1 consisted of automated client-side telemetry: capturing domain transition events, window focus shifts, and idle timeouts directly within the browser runtime.",
            "Stream 2 was an extensive empirical User Acceptance Testing study conducted via Google Forms, comprising 25 structured questions that captured user demographics, feature ratings, behavioral changes, and John Brooke's standardized 10-item System Usability Scale.",
            "Our participant cohort totaled 65 verified respondents, providing robust statistical representation across diverse digital workflows: 47.7% undergraduate students, 27.7% knowledge workers and IT professionals, 10.8% postgraduate researchers, and 13.8% academic faculty.",
            "Crucially, participants evaluated TabTime across four major Chromium and Gecko browsers—with 78.5% on Google Chrome, 10.8% on Brave, 6.2% on Microsoft Edge, and 4.6% on Firefox—confirming broad cross-platform interoperability."
        ],
        transition_text="\"Let us examine the headline empirical results and usability scores in Chapter 6.\""
    )

    # -------------------------------------------------------------
    # SLIDE 11
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=11,
        title="Chapter 6: Results Presentation: Usability & Feature Ratings",
        category="CHAPTER 6: RESULTS",
        duration="10:15 – 11:45 (90 Seconds)",
        visual_desc="Top: prominent royal blue hero banner proclaiming: 'SYSTEM USABILITY SCALE (SUS) COMPOSITE SCORE: 89.04 / 100 | GRADE A (TOP 10% PERCENTILE)'. Bottom-left: Figure 6.2 displaying the item-by-item SUS score breakdown across all 10 standard items. Bottom-right: Figure 6.3 displaying user satisfaction and utility ratings for automated tracking (95.4%), focus mode (92.3%), and dashboard visual analytics (93.8%).",
        physical_cues=[
            "[10:15] Advance to Slide 11. Allow the panel to read the 89.04 banner.",
            "[10:30] Point to the SUS breakdown graph on the bottom-left.",
            "[11:00] Move to the feature satisfaction chart on the bottom-right; smile with pride."
        ],
        spoken_script=[
            "I am thrilled to present our headline evaluation metric: TabTime achieved a composite System Usability Scale score of 89.04 out of 100.",
            "According to the definitive psychometric benchmarks established by Bangor, Kortum, and Miller (2008), any SUS score above 68 is considered average, above 80 is Grade A, and above 85 represents the top 10th percentile of software usability. A score of 89.04 demonstrates exceptional ease of use, intuitive interaction design, and rapid user onboarding.",
            "Examining the 10-item breakdown in Figure 6.2, participants strongly agreed with Item 3 ('I found the system easy to use') and Item 7 ('Most people would learn to use this system very quickly'), while strongly disagreeing with Item 4 ('I think I would need technical support') and Item 8 ('I found the system very cumbersome').",
            "Furthermore, as illustrated in Figure 6.3, our core features received overwhelming user approval: automated tracking achieved 95.4% satisfaction, focus mode redirection reached 92.3%, and our Chart.js visual analytics earned 93.8% positive utility ratings."
        ],
        transition_text="\"Now, how do these empirical scores correlate with our research hypotheses and technical benchmarks? Let us look at Slide 12.\""
    )

    # -------------------------------------------------------------
    # SLIDE 12
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=12,
        title="Chapter 6: Results Analysis & Hypotheses Interpretation",
        category="CHAPTER 6: ANALYSIS",
        duration="11:45 – 13:15 (90 Seconds)",
        visual_desc="Left card: formal hypotheses validation summary (Hypothesis H1 confirmed: 95.4% reported heightened habit awareness, 89.2% demonstrated self-regulation; Hypothesis H2 confirmed: 93.8% reported substantial reduction in distractions). Ground-truth stopwatch benchmarks showing mean timing precision within ±1.8 seconds over 1 hour (99.85% accuracy), and ultra-low system footprint (14–22 MB RAM, <0.5% CPU). Right side: Figure 6.4 behavioral impact chart.",
        physical_cues=[
            "[11:45] Advance to Slide 12. Speak with deliberate academic authority.",
            "[12:10] Point to H1 and H2 validation bullet points.",
            "[12:40] Emphasize the ±1.8 second stopwatch accuracy benchmark as an objective engineering proof."
        ],
        spoken_script=[
            "Slide 12 delivers the formal resolution of our research hypotheses.",
            "Hypothesis 1 is conclusively confirmed: 95.4% of surveyed participants reported heightened awareness of their daily digital browsing habits, and 89.2% reported demonstrable improvements in their personal self-regulation after utilizing TabTime's real-time productivity scoring.",
            "Hypothesis 2 is also conclusively confirmed: 93.8% of users confirmed a substantial reduction in distraction-related interruptions during study and work sessions when utilizing Focus Mode.",
            "Crucially, we did not rely solely on subjective survey self-reports. We subjected TabTime to rigorous laboratory stress testing against an external physical stopwatch. Across repeated one-hour automated browsing trials, TabTime's recorded elapsed time deviated by a mean of only ±1.8 seconds from the ground truth stopwatch, establishing an objective tracking accuracy of 99.85%.",
            "Simultaneously, Chrome DevTools process profiling confirmed an exceptionally lightweight footprint: background memory stabilized between 14 and 22 megabytes of RAM, with background CPU utilization remaining below 0.5%."
        ],
        transition_text="\"Achieving these results was not without obstacles. Slide 13 details the major engineering challenges we encountered and resolved.\""
    )

    # -------------------------------------------------------------
    # SLIDE 13
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=13,
        title="Chapter 5: Engineering Challenges & Problem Resolution",
        category="CHAPTER 5: CHALLENGES",
        duration="13:15 – 14:45 (90 Seconds)",
        visual_desc="Four detailed cards detailing technical hurdles and resolutions: 1. MV3 Service Worker Ephemerality (blue badge, 30s shutdown solved via state hydration in storage.local and alarms); 2. IndexedDB Transaction Contention (cyan badge, rapid tab switching causing write collisions solved via FIFO queue); 3. DeclarativeNetRequest Migration (amber badge, deprecated blocking webRequest replaced by dynamic ruleset compiler); 4. Study Limitations & Boundaries (slate badge, desktop Chromium focus, longitudinal habit shifts).",
        physical_cues=[
            "[13:15] Advance to Slide 13. Shift to an analytical, problem-solving tone.",
            "[13:35] Explain the service worker challenge clearly; supervisors love this technical detail.",
            "[14:10] Acknowledge the study limitations honestly and maturely."
        ],
        spoken_script=[
            "Engineering a sophisticated telemetry system within the constraints of Manifest V3 presented four complex hurdles.",
            "Challenge 1 was Service Worker Ephemerality. Under MV3, the browser terminates the background script after 30 seconds of perceived inactivity. If a user was reading a static article, in-memory session timers risked complete loss. We resolved this by engineering an event-driven state hydration mechanism: active timestamps are cached synchronously into chrome.storage.local on every state transition, and a heartbeat chrome.alarms listener flushes pending records to disk.",
            "Challenge 2 was IndexedDB Transaction Contention. When users rapidly switched between multiple tabs, concurrent asynchronous write transactions collided, throwing AbortErrors. We resolved this by implementing a serialized First-In, First-Out (FIFO) queue that batches database writes into safe atomic transactions.",
            "Challenge 3 was the MV3 DeclarativeNetRequest Migration. Because blocking webRequest was deprecated, we developed a dynamic ruleset compiler that maps user-defined blocklists directly to browser-level redirection headers, redirecting blocked requests instantaneously to blocked.html.",
            "Finally, we acknowledge our research boundaries: our 65-user study was conducted on desktop browsers over several weeks; multi-month longitudinal behavioral shifts remain an exciting area for future study."
        ],
        transition_text="\"Let us synthesize these findings in our Chapter 7 critical discussion on Slide 14.\""
    )

    # -------------------------------------------------------------
    # SLIDE 14
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=14,
        title="Chapter 7: Critical Discussion & Project Contributions",
        category="CHAPTER 7: DISCUSSION",
        duration="14:45 – 16:00 (75 Seconds)",
        visual_desc="Left side: card discussing Theoretical & HCI Contributions (validating non-coercive interventions, mindfulness over punishment), Practical Software Engineering Impact (debunking the commercial myth that time tracking requires cloud surveillance), and Professional Standards Compliance (British Computer Society BCS Code of Conduct). Right side: Figure 7.1 high-resolution UI screenshot of the full-screen Analytics Dashboard.",
        physical_cues=[
            "[14:45] Advance to Slide 14. Gesture toward the dashboard screenshot on the right.",
            "[15:10] Stand tall when referencing the British Computer Society Code of Conduct.",
            "[15:40] Emphasize 'data sovereignty' as a central ethical contribution."
        ],
        spoken_script=[
            "Chapter 7 contextualizes our project's contributions to computer science and human-computer interaction.",
            "Theoretically, TabTime validates the efficacy of non-coercive digital interventions. Rather than imposing punitive app lockers, our findings prove that presenting immediate visual feedback—such as the Chart.js daily distribution donuts shown in Figure 7.1—fosters intrinsic metacognitive reflection and sustained self-regulation.",
            "Practically, TabTime debunks the prevailing commercial assumption that comprehensive time tracking requires harvesting user data to the cloud. We have proven that modern browser sandboxes possess sufficient computational power and local storage capacity to deliver enterprise-grade analytics entirely on-device.",
            "Professionally, this project upholds the British Computer Society (BCS) Code of Conduct. By prioritizing user privacy, data minimization, and total data sovereignty, TabTime exemplifies ethical software engineering that protects the public interest and complies with W3C web standards."
        ],
        transition_text="\"Building upon this foundation, Slide 15 outlines our strategic roadmap for future work.\""
    )

    # -------------------------------------------------------------
    # SLIDE 15
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=15,
        title="Chapter 8: Recommendations for Future Work",
        category="CHAPTER 8: FUTURE WORK",
        duration="16:00 – 17:15 (75 Seconds)",
        visual_desc="Four forward-looking cards in a 2x2 grid outlining future research avenues: 1. On-Device NLP Categorization (blue badge, WebAssembly micro-LLMs or TensorFlow.js for semantic page understanding without cloud API transmission); 2. Client-Side Zero-Knowledge Sync (cyan badge, AES-GCM-256 encrypted sync via WebDAV/Google Drive); 3. Mobile Extension Compatibility (green badge, porting to Firefox Android and Safari iOS); 4. Adaptive Biometric & Audio Pacing (navy badge, WebHID webcam fatigue detection and binaural ambient audio).",
        physical_cues=[
            "[16:00] Advance to Slide 15. Adopt an enthusiastic, forward-looking vision.",
            "[16:20] Highlight the on-device NLP concept with technical specificity.",
            "[16:50] Conclude with the biometric pacing vision."
        ],
        spoken_script=[
            "Looking beyond the scope of this undergraduate project, we have formulated a four-stage architectural roadmap in Chapter 8.",
            "First is On-Device Natural Language Processing. While TabTime currently categorizes domains using high-speed heuristic rule-matching, future iterations can embed a quantized micro-model—such as WebAssembly TensorFlow.js or Chrome's built-in Gemini Nano API—to parse page content semantically on-device, categorizing pages without transmitting text to external servers.",
            "Second is Client-Side Zero-Knowledge Synchronization. To allow cross-device analytics while preserving privacy, we propose encrypting IndexedDB snapshots with AES-GCM-256 via the Web Cryptography API and syncing them across user-owned cloud containers like personal Google Drive or WebDAV.",
            "Third is Mobile Portability, porting our background service worker to mobile runtimes like Firefox for Android and Safari on iOS.",
            "Finally, we envision Adaptive Biometric Pacing—integrating passive fatigue indicators and subtle binaural ambient audio cues to help users disengage mindfully from high-strain sessions."
        ],
        transition_text="\"Let us bring together our core findings and conclusions on Slide 16.\""
    )

    # -------------------------------------------------------------
    # SLIDE 16
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=16,
        title="Chapter 7: Project Conclusions & Core Takeaways",
        category="CHAPTER 7: CONCLUSION",
        duration="17:15 – 18:15 (60 Seconds)",
        visual_desc="Three wide horizontal cards summarizing the project conclusions: 1. Overall Project Outcome & Artefact Success (blue accent, production-ready MV3 browser extension delivering tracking, analytics, and focus management with 100% local privacy); 2. Definitive Resolution of Research Question (cyan accent, validated non-coercive nudges, 95.4% habit awareness, 93.8% distraction reduction, confirming H1 and H2); 3. Academic & Industry Significance (green accent, SUS score of 89.04, proving privacy and high precision can coexist).",
        physical_cues=[
            "[17:15] Advance to Slide 16. Lower cadence, speaking with solemn, authoritative conclusion.",
            "[17:35] Reiterate the definitive resolution of the central research question.",
            "[18:00] Hold your posture steady, looking directly at the examiners."
        ],
        spoken_script=[
            "In conclusion, this Individual Research Project has successfully designed, engineered, and empirically validated TabTime—a production-ready, open-source browser extension operating under Manifest V3.",
            "To answer our central research question definitively: Yes, a browser extension combining automated time tracking, visual analytics, and non-coercive focus management significantly improves users' awareness of digital habits (95.4%) and reduces online distractions (93.8%), fully verifying Hypotheses 1 and 2.",
            "Moreover, achieving a System Usability Scale score of 89.04 demonstrates that rigorous Privacy-by-Design principles do not require sacrificing visual sophistication, real-time feedback, or user satisfaction. TabTime proves that software engineers can create powerful digital wellbeing tools while respecting fundamental user privacy rights."
        ],
        transition_text="\"Allow me to briefly highlight our ethical governance and research compliance on Slide 17.\""
    )

    # -------------------------------------------------------------
    # SLIDE 17
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=17,
        title="Ethics & Regulatory Governance",
        category="ETHICS & GOVERNANCE",
        duration="18:15 – 19:00 (45 Seconds)",
        visual_desc="Four cards in a 2x2 grid covering ethical and regulatory pillars: 1. YSJ Ethical Approval (blue badge, formal clearance under School of Science, Technology & Health framework); 2. GDPR Data Protection by Design (green badge, Article 25 and UK DPA 2018 compliance, local IndexedDB isolation); 3. Voluntary Informed Consent (cyan badge, Participant Information Sheet, digital consent, right to withdraw); 4. Total Anonymity & Zero PII (navy badge, no names, IP addresses, full URLs, or query parameters stored).",
        physical_cues=[
            "[18:15] Advance to Slide 17. Present the ethical clearance with professional solemnity.",
            "[18:35] Emphasize that full URLs and personal query tokens were never captured.",
            "[18:50] Nod respectfully to demonstrate ethical maturity."
        ],
        spoken_script=[
            "Ethical integrity and legal governance were foundational to this project from day one.",
            "Full ethical approval was granted under the York St John University School of Science, Technology & Health research ethics protocol.",
            "Under GDPR Article 25 and the UK Data Protection Act 2018, TabTime operationalizes Data Protection by Design and by Default: zero external telemetry, zero centralized databases, and complete local isolation.",
            "All 65 study participants provided voluntary, informed digital consent following review of a comprehensive Participant Information Sheet, retaining full rights to withdraw. Furthermore, our telemetry strictly logged normalized domain hostnames—never recording full URL paths, search queries, or personally identifiable information."
        ],
        transition_text="\"A brief review of our foundational academic references is presented on Slide 18.\""
    )

    # -------------------------------------------------------------
    # SLIDE 18
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=18,
        title="Academic References & Cited Works",
        category="REFERENCES",
        duration="19:00 – 19:25 (25 Seconds)",
        visual_desc="Two neat columns of Harvard-style academic citations including Bandura (1991), Bangor et al. (2008), British Computer Society (2022), Brooke (1996), GDPR (2016), Google Chrome Developers (2024), Hevner et al. (2004), Kaplan (1995), Mark et al. (2008), and Zuboff (2019).",
        physical_cues=[
            "[19:00] Advance to Slide 18. Briefly glance at the citations.",
            "[19:15] Keep this slide brisk; examiners can inspect citations in the dissertation.",
            "[19:22] Transition smoothly to the Executive Summary."
        ],
        spoken_script=[
            "Slide 18 details our primary academic literature citations in Harvard format—encompassing seminal works in self-regulation, usability psychometrics, information systems design science, cognitive interruption costs, surveillance capitalism, and the official W3C and Google WebExtensions technical specifications."
        ],
        transition_text="\"To synthesize everything we have covered, let us review our Executive Summary on Slide 19.\""
    )

    # -------------------------------------------------------------
    # SLIDE 19
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=19,
        title="Executive Summary & Wrap-Up",
        category="EXECUTIVE SUMMARY",
        duration="19:25 – 19:55 (30 Seconds)",
        visual_desc="Four structured cards recapping the four core pillars: 1. Project Purpose & Value Proposition (lightweight, client-side browser extension empowering students with millisecond time awareness); 2. Design Science Research Methodology (rigorous DSR lifecycle, automated benchmarks, n=65 empirical UAT); 3. Key Evaluation Findings (composite SUS 89.04 Grade A, 95.4% habit awareness, 93.8% distraction reduction, 14-22 MB RAM); 4. Academic & Ethical Contributions (zero-cloud privacy-preserving telemetry model adhering to BCS standards).",
        physical_cues=[
            "[19:25] Advance to Slide 19. Deliver the summary with energy and authority.",
            "[19:40] Emphasize the four pillars as a cohesive body of scholarly work.",
            "[19:50] Prepare for the formal closing."
        ],
        spoken_script=[
            "In summary, TabTime represents a rigorous, end-to-end realization of computer science research:",
            "We identified a pressing societal problem in browser attention fragmentation and surveillance capitalism; we applied Design Science Research to engineer an elegant Three-Layer Manifest V3 solution; we validated it empirically with 65 users achieving an 89.04 SUS score; and we proved that high-performance analytics and absolute user privacy can successfully unite."
        ],
        transition_text="\"With that, we arrive at our final slide and invite your questions.\""
    )

    # -------------------------------------------------------------
    # SLIDE 20
    # -------------------------------------------------------------
    add_slide_section(
        doc,
        slide_num=20,
        title="Q&A Defense & Formal Invitation",
        category="Q&A DEFENSE",
        duration="19:55 – 20:15 (20 Seconds)",
        visual_desc="Large, elegant card centered with white background and royal blue border reading: 'THANK YOU FOR YOUR TIME & ATTENTION', 'TAB TIME: A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management', 'The Examination Panel is Respectfully Invited for Questions, Discussion & Technical Defense', candidate details, supervisor acknowledgment, and the TabTime application icon cleanly anchored at the bottom.",
        physical_cues=[
            "[19:55] Advance to Slide 20. Smile warmly and look across all panel members.",
            "[20:05] Place the clicker gently on the desk. Open your hands slightly in an inviting gesture.",
            "[20:15] Stand ready and attentive for the panel's first question."
        ],
        spoken_script=[
            "Thank you very much for your time, attention, and consideration. I would like to extend my sincere gratitude to my supervisor, [Supervisor Name], and the faculty of the School of Science, Technology & Health for their invaluable guidance throughout this academic year.",
            "I now respectfully invite the examination committee for your questions, critical discussion, and technical defense. Thank you."
        ],
        transition_text=None
    )

    doc.add_page_break()

    # =========================================================================
    # PART 5: COMPREHENSIVE VIVA DEFENSE MASTER Q&A PLAYBOOK
    # =========================================================================
    print("Building Part 5: Comprehensive Viva Q&A Playbook (20 Questions)...")
    h1_qa = doc.add_heading(level=1)
    h1_qa.paragraph_format.space_before = Pt(0)
    h1_qa.paragraph_format.space_after = Pt(6)
    r = h1_qa.add_run("Part 4: Comprehensive Viva Voce Defense Master Q&A Playbook")
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_qa_intro = doc.add_paragraph()
    p_qa_intro.paragraph_format.space_before = Pt(2)
    p_qa_intro.paragraph_format.space_after = Pt(8)
    p_qa_intro.paragraph_format.line_spacing = 1.15
    r = p_qa_intro.add_run(
        "This master playbook prepares the candidate for anticipated challenging cross-examination questions from viva voce examiners. The questions are categorized into five academic and technical domains. For each question, we provide the Examiner's Intent (what the examiner is probing), a Model Verbal Answer (structured for maximum marks), and Key Citations & Technical Benchmarks."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)

    qa_master_list = [
        # CATEGORY A: Architecture & WebExtensions
        (
            "Category A: Architecture, WebExtensions & Software Engineering",
            "Q1: Explain how you resolved Chrome's 30-second service worker idle shutdown without losing active tracking timestamps.",
            "Examiner Intent: Probing whether the candidate truly understands Manifest V3 lifecycle constraints or simply treated background.js like a legacy Manifest V2 background page.",
            "Model Verbal Answer: In Manifest V2, background pages were persistent singletons that remained resident in memory indefinitely. Under Manifest V3, background scripts are implemented as service workers that the browser terminates after approximately 30 seconds of inactivity to conserve RAM. If a candidate attempts to store in-flight session durations in global memory variables, those variables vanish when the service worker is suspended.\n\nTo resolve this, we engineered an event-driven state hydration mechanism. Every time a tab or window focus event fires, we write a lightweight snapshot of the active tab ID, normalized domain, and start timestamp into chrome.storage.local. Because chrome.storage.local survives worker termination, when a subsequent event wakes the service worker, our initialization routine immediately inspects this stored snapshot, calculates the delta elapsed time, and writes the completed session record to IndexedDB. Furthermore, we implemented a periodic chrome.alarms heartbeat that wakes the worker periodically during extended static reading sessions, guaranteeing that no more than 60 seconds of telemetry can ever be affected by unexpected process termination.",
            "Key References: Google Chrome Developers (2024) MV3 Service Worker Migration Guide; chrome.storage.local and chrome.alarms APIs."
        ),
        (
            "Category A: Architecture, WebExtensions & Software Engineering",
            "Q2: Why did you choose declarativeNetRequest instead of injecting content scripts or using the webRequest API for Focus Mode?",
            "Examiner Intent: Testing candidate's knowledge of browser security models, network interception, and API deprecation in MV3.",
            "Model Verbal Answer: In Manifest V2, focus blocking was typically implemented using webRequest.onBeforeRequest with the 'blocking' permission. However, Google deprecated blocking webRequest in MV3 because it forced the browser to pause every network request synchronously while JavaScript code evaluated whether to allow or block it, introducing significant latency and enabling malicious extensions to inspect or modify sensitive traffic.\n\nContent script injection is equally flawed: a content script can only manipulate the DOM after the page has already begun loading, allowing distracting content or media to flash briefly on screen before being hidden.\n\ndeclarativeNetRequest is the superior architectural choice. Instead of evaluating requests in JavaScript, TabTime compiles user blocklists into declarative JSON rule structures and registers them with the browser via chrome.declarativeNetRequest.updateDynamicRules. The browser's native C++ networking engine evaluates these rules directly at the network layer before any TCP connection or DNS resolution begins, redirecting matching domains to our local blocked.html instantaneously with zero execution overhead and complete tamper-resistance.",
            "Key References: W3C WebExtensions Working Group; chrome.declarativeNetRequest API specification."
        ),
        (
            "Category A: Architecture, WebExtensions & Software Engineering",
            "Q3: What happens if a user opens 50 tabs across 3 different browser windows simultaneously? How does your tracking algorithm prevent race conditions and over-counting?",
            "Examiner Intent: Checking algorithmic concurrency, multi-window event management, and edge-case handling.",
            "Model Verbal Answer: A naive tracking extension might listen to tabs.onUpdated across all tabs and erroneously accumulate time for every open tab simultaneously, multiplying a 1-hour session into 50 hours of recorded time. TabTime completely prevents this through single-focus mutual exclusivity.\n\nOur tracking engine relies on a dual-event listener structure: chrome.windows.onFocusChanged and chrome.tabs.onActivated. At any given millisecond, a user can only interact with exactly one active tab inside one focused browser window. When a window loses focus (e.g. windowId === chrome.windows.WINDOW_ID_NONE), our engine immediately pauses tracking and commits the current domain's elapsed time. When the user switches tabs or windows, our tracking-core.js module executes a clean transition: it finalizes the timestamp of the prior tab, flushes the delta, and initializes tracking for the newly focused tab ID. Even with 50 open tabs across 3 monitors, exactly one tab is being timed at any instant.",
            "Key References: TabTime tracking-core.js; Chrome Window & Tab Focus Events specification."
        ),
        (
            "Category A: Architecture, WebExtensions & Software Engineering",
            "Q4: Explain how IndexedDB transaction contention was handled during high-frequency tab switching.",
            "Examiner Intent: Probing understanding of asynchronous database locking, write collisions, and storage performance.",
            "Model Verbal Answer: IndexedDB operates on an asynchronous transaction model. When rapid tab switching occurs—such as a user rapidly cycling through 10 tabs using Ctrl+Tab—multiple write transactions attempt to open the 'domainLogs' object store in readwrite mode simultaneously. In early prototypes, this triggered TransactionInactiveError and AbortError exceptions because a subsequent event attempted to reuse a transaction that had already closed.\n\nTo solve this, we implemented a serialized First-In, First-Out (FIFO) transaction queue in storage.js. When an event fires, the telemetry payload is appended to an in-memory queue. A dedicated async queue processor dequeues items sequentially, opening a single readwrite transaction to batch write multiple records or waiting for the current transaction's oncomplete event before opening the next. This eliminated 100% of write collisions and reduced disk I/O overhead.",
            "Key References: W3C Indexed Database API 3.0 Specification; TabTime storage.js FIFO implementation."
        ),
        (
            "Category A: Architecture, WebExtensions & Software Engineering",
            "Q5: How is your mathematical productivity score calculated, and what prevents score distortion from idle tabs?",
            "Examiner Intent: Verifying mathematical rigor, heuristic validity, and edge-case filtering.",
            "Model Verbal Answer: TabTime calculates a daily Productivity Score ranging from 0 to 100 using a normalized time-weighted formula:\n\nScore = [ (Time_Productive * 1.0) + (Time_Neutral * 0.5) + (Time_Distracting * 0.0) ] / Total_Active_Time * 100\n\nIf total active time is zero, the score defaults cleanly to 0. Productive domains (e.g. academic libraries, GitHub, Google Docs) receive full weight; neutral domains (e.g. search engines, system utilities) receive half weight; distracting domains (e.g. entertainment, social media) receive zero weight.\n\nTo prevent score distortion from abandoned or idle tabs, the score denominator strictly uses Total Active Time, not wall-clock time. If a user walks away from their laptop for 45 minutes while an educational article is open, the chrome.idle API detects the absence of mouse and keyboard events after 60 seconds and suspends the tracking accumulator, preventing the score from artificially inflating.",
            "Key References: TabTime Mathematical Formulation (Report Chapter 5.2); chrome.idle API."
        ),

        # CATEGORY B: Privacy, Security & GDPR
        (
            "Category B: Privacy, Security, Ethics & GDPR",
            "Q6: How can you empirically prove to this panel that TabTime sends zero bytes of telemetry to external servers?",
            "Examiner Intent: Probing verification methodology, network security validation, and evidence standards.",
            "Model Verbal Answer: We verified our zero-cloud telemetry claim through three rigorous testing tiers:\n\nFirst, Static Manifest Auditing: In manifest.json, we strictly limited permissions to 'storage', 'tabs', 'idle', 'declarativeNetRequest', and 'alarms'. There are zero remote host permissions (no 'http://*/*' or 'https://*/*'), and no external Content Security Policy directives. Chrome enforces this declaratively; an extension cannot make an unauthorized network call without declaring matching host permissions.\n\nSecond, Automated Source Code Check: We built an automated test script (npm run check / scripts/check-extension.mjs) that scans every JavaScript file for fetch(), XMLHttpRequest(), WebSocket(), or navigator.sendBeacon(). The test passes with zero occurrences.\n\nThird, Dynamic Runtime Network Inspection: In Chrome DevTools, opening the background service worker inspection panel and monitoring the Network tab during hours of active use confirms zero outbound HTTP requests, WebSockets, or background beacons. 100% of telemetry originates and terminates within the browser's local IndexedDB instance.",
            "Key References: TabTime scripts/check-extension.mjs; Chrome Content Security Policy (CSP) specification."
        ),
        (
            "Category B: Privacy, Security, Ethics & GDPR",
            "Q7: How does TabTime comply with GDPR Article 25 (Data Protection by Design and by Default) and Article 5 (Data Minimisation)?",
            "Examiner Intent: Testing legal and ethical understanding of European/UK data protection frameworks.",
            "Model Verbal Answer: GDPR Article 25 mandates that system architectures must integrate data protection principles into their core engineering rather than treating privacy as an afterthought. TabTime achieves this by design: there is no centralized database, no user account creation, and no telemetry transmission.\n\nUnder Article 5(1)(c) (Data Minimisation), personal data must be adequate, relevant, and limited to what is strictly necessary. TabTime strips full URL paths (such as specific query strings, video IDs, or private document tokens) and stores only normalized domain hostnames (e.g., 'wikipedia.org'). This provides sufficient granularity for productivity analysis while ensuring that sensitive personal queries or medical browsing paths are never captured.\n\nFinally, under Article 17 (Right to Erasure) and Article 20 (Data Portability), TabTime provides one-click JSON export of all logged records and an instant 'Purge All Data' button in the settings UI that executes indexedDB.deleteDatabase(), giving the user unconditional sovereignty over their data.",
            "Key References: Regulation (EU) 2016/679 (GDPR), Articles 5, 17, 20, and 25; UK Data Protection Act 2018."
        ),
        (
            "Category B: Privacy, Security, Ethics & GDPR",
            "Q8: Why did you decide to store domain hostnames rather than full page URLs, and what are the analytical trade-offs?",
            "Examiner Intent: Probing understanding of the tension between data granularity and user privacy.",
            "Model Verbal Answer: Choosing between domain hostnames (e.g. 'github.com') and full URLs (e.g. 'github.com/user/private-repo/commit/123') is a classic privacy-utility trade-off. We deliberately chose domain hostnames for three reasons:\n\n1. Privacy & Security: Full URLs frequently contain sensitive authentication tokens, search parameters, or confidential document IDs. Storing full URLs would turn TabTime's local database into a high-risk surveillance artifact.\n\n2. Storage Optimization: A domain hostname requires approximately 15 to 30 bytes, whereas full URLs can exceed 2,000 bytes. Across thousands of daily browsing transitions, storing full URLs would bloat IndexedDB and degrade Chart.js query performance.\n\n3. Analytical Sufficiency: For personal time awareness and productivity scoring, knowing that a user spent 45 minutes on 'stackoverflow.com' or 'youtube.com' provides 99% of the behavioral insight needed for self-regulation.\n\nThe trade-off is that multi-purpose domains (like YouTube, which hosts both educational lectures and entertainment) cannot be automatically differentiated by domain alone. We solved this by allowing users to create custom domain categorization overrides and manually toggle focus session rules.",
            "Key References: TabTime Final Comprehensive Report, Chapter 3.1 & 5.1."
        ),
        (
            "Category B: Privacy, Security, Ethics & GDPR",
            "Q9: What security threats exist if a malicious extension or script attempts to access TabTime's IndexedDB data?",
            "Examiner Intent: Testing understanding of browser sandbox boundaries and the Same-Origin Policy.",
            "Model Verbal Answer: The browser's native security model enforces the Same-Origin Policy (SOP). In Chrome and Firefox, every installed extension is assigned a unique, cryptographically random extension origin (e.g., 'chrome-extension://<extension_id>/').\n\nIndexedDB instances and chrome.storage.local facilities are strictly partitioned by origin. A web page running in a tab has zero access to an extension's IndexedDB, and another third-party extension installed in the browser cannot read TabTime's storage because it resides in a distinct security principal. The only vector for data compromise would be local operating system-level malware possessing full administrator disk access, at which point the entire machine is compromised regardless of application design.",
            "Key References: W3C Same-Origin Policy specification; Chromium Security Architecture Model."
        ),

        # CATEGORY C: Methodology, Sampling & Evaluation
        (
            "Category C: Research Methodology, Sampling & Evaluation",
            "Q10: Why was Design Science Research (DSR) appropriate for this project rather than a traditional empirical control experiment?",
            "Examiner Intent: Checking whether the student understands scientific methodology and can defend their research design.",
            "Model Verbal Answer: Traditional empirical control experiments are suited for testing natural phenomena or passive observations. However, when the primary research goal is to design, engineer, and evaluate an innovative technological artifact that solves an identified practical problem, Design Science Research—as formalized by Hevner et al. (2004)—is the internationally recognized standard.\n\nDSR provides a rigorous, cyclical framework consisting of six structured steps: problem identification, objective definition, artifact design and development, laboratory demonstration, empirical evaluation, and scholarly communication. By utilizing DSR, we were able to bridge theoretical HCI constructs (Bandura's self-regulation) with production software engineering (Manifest V3), evaluating the artifact through both objective system benchmarking and subjective human usability testing.",
            "Key References: Hevner, A.R. et al. (2004) 'Design science in information systems research', MIS Quarterly, 28(1), pp. 75–105."
        ),
        (
            "Category C: Research Methodology, Sampling & Evaluation",
            "Q11: Your SUS score is 89.04. Isn't there an inherent self-selection bias in your sample of 65 participants?",
            "Examiner Intent: Probing statistical awareness, sampling limitations, and critical research objectivity.",
            "Model Verbal Answer: Self-selection bias is an acknowledged consideration in voluntary software evaluation studies. Participants who volunteer may possess higher digital literacy or an existing interest in productivity tools. We actively mitigated this threat through three deliberate methodological controls:\n\n1. Cohort Stratification: We did not sample exclusively from computer science students. As shown in Figure 6.1, our 65 participants include academic faculty (13.8%), non-technical knowledge workers (27.7%), and postgraduate researchers (10.8%), providing a broad cross-section of workplace and educational contexts.\n\n2. Alternating Polarity Psychometrics: John Brooke's System Usability Scale is specifically constructed with 10 alternating positive and negative statements (e.g. Item 1 is positive, Item 2 is negative). This design mathematically neutralizes acquiescence bias and extreme response biases.\n\n3. Objective Triangulation: We triangulated our subjective survey findings with objective physical stopwatch benchmarks (showing 99.85% timing accuracy) and automated stress tests, proving that high usability ratings were backed by genuine technical precision.",
            "Key References: Brooke, J. (1996) 'SUS: A quick and dirty usability scale'; Bangor, Kortum & Miller (2008)."
        ),
        (
            "Category C: Research Methodology, Sampling & Evaluation",
            "Q12: How did you establish the ground-truth benchmark for your stopwatch accuracy validation?",
            "Examiner Intent: Assessing empirical rigor in physical laboratory benchmarking.",
            "Model Verbal Answer: To validate timing accuracy independently of the operating system clock, we established a physical ground-truth testbed. A certified digital stopwatch with a precision of 1/100th of a second was synchronized with the manual trigger of an automated test script running via Puppeteer / browser automation.\n\nThe script executed a standardized 60-minute browsing simulation comprising active reading sessions, rapid 5-second tab switches, window minimizations, and 5-minute simulated idle periods. At the conclusion of the 60-minute physical stopwatch period, TabTime's IndexedDB log recorded 3,598.2 seconds of active tracking. The mean deviation across five repeated trials was ±1.8 seconds—an error margin of less than 0.15%, confirming 99.85% accuracy.",
            "Key References: TabTime Final Comprehensive Report, Chapter 6.2; System Telemetry Verification."
        ),
        (
            "Category C: Research Methodology, Sampling & Evaluation",
            "Q13: What are the primary threats to internal and external validity in your empirical findings?",
            "Examiner Intent: Testing scientific maturity and the ability to critique one's own research methodology.",
            "Model Verbal Answer: Threats to internal validity include the Hawthorne Effect—the phenomenon where participants temporarily modify their browsing behavior simply because they know their productivity is being studied. While our survey confirmed significant behavioral improvements (95.4% habit awareness), longitudinal studies over six months would be required to verify whether this heightened awareness translates into permanent habit change.\n\nThreats to external validity relate to platform generalizability: our evaluation cohort evaluated TabTime exclusively on desktop Chromium and Gecko browsers (Windows, macOS, Linux). The findings cannot be directly generalized to mobile browsing environments (such as iOS or Android), where tab management and background execution models differ substantially.",
            "Key References: Research Methodology Chapter 4.4; Threats to Validity."
        ),

        # CATEGORY D: Human-Computer Interaction & Behavioral Impact
        (
            "Category D: Human-Computer Interaction & Behavioral Impact",
            "Q14: Your survey indicates 93.8% distraction reduction. How do you distinguish genuine cognitive focus from simple compliance?",
            "Examiner Intent: Probing understanding of HCI, user psychology, and cognitive measurement.",
            "Model Verbal Answer: Distinguishing genuine focus from superficial compliance requires examining user interactions during Focus Mode. In systems with punitive blocking, users frequently experience cognitive frustration and attempt to circumvent the blocker (compliance failure).\n\nIn TabTime, Focus Mode is non-coercive. When a user attempts to access a blocked site (such as YouTube), they are redirected to blocked.html, which displays a calm, aesthetic visual reminder and a reflective quote. Qualitative feedback from survey respondents revealed that this subtle intervention broke the automatic 'muscle-memory' impulse of opening social media tabs. Participants actively chose to return to their academic work rather than looking for workarounds, demonstrating genuine metacognitive reflection rather than forced compliance.",
            "Key References: Mark et al. (2008) Interruption Recovery Costs; Kaplan (1995) Attention Restoration Theory."
        ),
        (
            "Category D: Human-Computer Interaction & Behavioral Impact",
            "Q15: Why did you choose Chart.js over other visualization libraries like D3.js or Apache ECharts?",
            "Examiner Intent: Testing technical evaluation of frontend dependencies and performance trade-offs.",
            "Model Verbal Answer: We conducted a formal technical trade-off evaluation between D3.js, ECharts, and Chart.js. While D3.js offers limitless custom SVG manipulation, it has a steep learning curve, a large bundle size (>500KB), and requires direct DOM manipulation that introduces rendering latency in extension popups. ECharts is equally powerful but carries a heavy runtime footprint (>1MB).\n\nChart.js was selected because it utilizes HTML5 Canvas rendering rather than SVG DOM nodes, executing chart redraws in under 16 milliseconds (60 frames per second). Furthermore, its bundled UMD library is lightweight (~180KB), fully compliant with Manifest V3 Content Security Policy (requiring zero eval() or inline scripts), and natively supports responsive canvas resizing within our popup and dashboard views.",
            "Key References: Chart.js 4.4 Documentation; TabTime tabtime-extension/libs/chart.umd.js."
        ),

        # CATEGORY E: Limitations, Reflection & Future Roadmap
        (
            "Category E: Limitations, Critical Reflection & Future Roadmap",
            "Q16: What is the single biggest technical limitation of your current implementation?",
            "Examiner Intent: Testing candid self-awareness and critical engineering maturity.",
            "Model Verbal Answer: The single biggest technical limitation of the current implementation is its reliance on domain-level heuristic categorization rather than page-level semantic analysis.\n\nCurrently, TabTime categorizes 'youtube.com' as 'Entertainment / Distracting'. However, a student watching a two-hour university lecture or technical coding tutorial on YouTube is engaged in highly productive academic work. While TabTime provides a user settings interface where domains can be re-categorized manually, the extension cannot automatically differentiate between educational YouTube videos and recreational gaming streams without inspecting page metadata or video titles. Solving this without compromising privacy is the primary goal of our Chapter 8 roadmap.",
            "Key References: TabTime Final Comprehensive Report, Chapter 5.4 & 8.1."
        ),
        (
            "Category E: Limitations, Critical Reflection & Future Roadmap",
            "Q17: How would you implement privacy-preserving semantic categorization without sending page text to third-party cloud LLMs?",
            "Examiner Intent: Testing forward-looking AI knowledge and architectural innovation.",
            "Model Verbal Answer: We have designed an on-device semantic classification architecture for future implementation using WebAssembly (Wasm) and Chrome's emerging built-in AI APIs (such as Gemini Nano / Window.ai).\n\nInstead of transmitting web page text to OpenAI or Google cloud endpoints—which would violate GDPR data minimization—a lightweight, quantized text classification model (e.g. MobileBERT or a fine-tuned ONNX model) runs entirely on the user's local hardware via Wasm or WebGPU. The content script extracts the document title and meta-description tags, passes them to the local in-browser model, and produces a semantic category vector in under 50 milliseconds. Telemetry remains 100% on-device, uniting deep semantic awareness with absolute privacy.",
            "Key References: W3C Web Machine Learning Working Group; Chrome Built-in AI (Prompt API). "
        ),
        (
            "Category E: Limitations, Critical Reflection & Future Roadmap",
            "Q18: If you had an additional 6 months of research funding, what specific architectural component would you rebuild?",
            "Examiner Intent: Testing strategic research planning and architectural vision.",
            "Model Verbal Answer: With six months of dedicated funding, I would focus on two major architectural extensions:\n\nFirst, I would build a Zero-Knowledge Client-Side Synchronisation Layer. Using the Web Cryptography API, TabTime would encrypt local IndexedDB snapshots client-side using AES-GCM-256 with a user-held passphrase. Encrypted blobs could then synchronize across laptops and mobile devices via standard user-owned storage (such as WebDAV or personal cloud drive), achieving multi-device time tracking without exposing unencrypted telemetry to any third party.\n\nSecond, I would conduct a 6-month longitudinal behavioral study tracking 200 participants across diverse universities to measure whether visual nudges yield permanent neuro-cognitive habit shifts over semester-long examination cycles.",
            "Key References: Recommendations for Further Work, Chapter 8.2 & 8.3."
        ),
        (
            "Category E: Limitations, Critical Reflection & Future Roadmap",
            "Q19: What was the most significant bug or failure during your development lifecycle, and how did you diagnose it?",
            "Examiner Intent: Assessing real-world debugging capability, resilience, and software engineering discipline.",
            "Model Verbal Answer: The most critical failure occurred during early multi-tab stress testing: after leaving the browser running overnight with 30 tabs open, the dashboard showed zero tracked time for the entire previous evening. Diagnosing this revealed a silent failure in our IndexedDB upgrade handler.\n\nWhen Chrome auto-updated in the background, our database versioning logic in storage.js had a race condition: the service worker woke up and immediately attempted to write telemetry before the IndexedDB onupgradeneeded event had finished creating the object stores. Because the error was caught in an unhandled promise rejection, it failed silently.\n\nI diagnosed this using Chrome's persistent background inspection flags (chrome://inspect/#extensions) and DevTools console log persistence. I resolved it by wrapping the database connection in a robust Singleton Promise pattern: all read/write methods await a single getDB() promise that guarantees the database is open, upgraded, and indexed before any transaction can execute.",
            "Key References: TabTime tabtime-extension/storage.js Singleton Promise pattern."
        ),
        (
            "Category E: Limitations, Critical Reflection & Future Roadmap",
            "Q20: What have you personally learned as a software engineer through undertaking this Individual Research Project?",
            "Examiner Intent: Assessing personal reflection, professional growth, and alignment with BCS standards.",
            "Model Verbal Answer: Undertaking this project has transformed my perspective on software engineering in three profound ways:\n\nFirst, I learned that architectural elegance is defined by constraints. Navigating the strict lifecycle of Manifest V3 taught me asynchronous systems programming, event-driven state persistence, and memory optimization far beyond simple web development.\n\nSecond, I developed a deep ethical commitment to Privacy-by-Design. Building TabTime proved to me that engineers do not have to accept the surveillance capitalism paradigm; with thoughtful design, we can deliver rich analytics while upholding user data sovereignty.\n\nThird, I learned the value of empirical humility. Seeing real users interact with TabTime during our 65-participant study taught me that what seems intuitive to a developer is often confusing to a user. Listening to user feedback and watching our SUS score climb to 89.04 was the most rewarding aspect of my degree.",
            "Key References: BCS Code of Conduct (2022); Chapter 7.5 Personal Reflection."
        )
    ]

    for cat_title, q_text, intent, answer, refs in qa_master_list:
        add_callout_box(
            doc,
            q_text,
            [
                f"🎯 EXAMINER INTENT: {intent}",
                f"🎙️ MODEL VERBAL ANSWER:\n{answer}",
                f"📚 KEY REFERENCES & EVIDENCE: {refs}"
            ],
            border_color=HEX_BLUE if "Architecture" in cat_title else (HEX_GREEN if "Privacy" in cat_title else (HEX_CYAN if "Methodology" in cat_title else HEX_AMBER)),
            bg_color=HEX_BG_CARD,
            badge=cat_title.split(":")[0].upper()
        )

    doc.add_page_break()

    # =========================================================================
    # PART 6: MINUTE-BY-MINUTE LIVE SYSTEM DEMONSTRATION PROTOCOL
    # =========================================================================
    print("Building Part 6: Live Demonstration Protocol & Contingency Plan...")
    h1_demo = doc.add_heading(level=1)
    h1_demo.paragraph_format.space_before = Pt(0)
    h1_demo.paragraph_format.space_after = Pt(6)
    r = h1_demo.add_run("Part 5: Minute-by-Minute Live System Demonstration Protocol")
    r.font.name = "Segoe UI"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_demo_desc = doc.add_paragraph()
    p_demo_desc.paragraph_format.space_before = Pt(2)
    p_demo_desc.paragraph_format.space_after = Pt(8)
    p_demo_desc.paragraph_format.line_spacing = 1.15
    r = p_demo_desc.add_run(
        "A practical, step-by-step choreography for delivering a flawless live technical demonstration of the TabTime browser extension during your viva voce or supervisor review. Includes pre-demo environment setup, step-by-step feature execution, and a robust contingency fallback plan."
    )
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)

    add_callout_box(
        doc,
        "PRE-DEMO ENVIRONMENT SETUP & VERIFICATION CHECKLIST",
        [
            "1. Browser Profile: Open a fresh Google Chrome or Microsoft Edge profile. Ensure no conflicting ad-blockers or productivity extensions are active.",
            "2. Unpacked Extension Folder: Ensure D:\\My Project\\Browser Extenstion project\\tabtime-extension is accessible.",
            "3. Seeded Historical Data: Pre-load the extension with 3-5 days of representative browsing data so charts and trends populate instantly.",
            "4. DevTools Setup: Open DevTools (F12) docked to the right side of the window, navigated to the Network tab with filter set to 'Fetch/XHR' to prove zero outbound traffic live.",
            "5. Prepared Test Tabs: Have three clean tabs prepared: (a) An academic paper on researchgate.net or wikipedia.org (Productive); (b) A search query on google.com (Neutral); (c) A video on youtube.com or reddit.com (Distracting)."
        ],
        border_color=HEX_BLUE,
        bg_color=HEX_BG_CARD,
        badge="SETUP CHECKLIST"
    )

    demo_steps = [
        (
            "Stage 1: Extension Loading & Manifest V3 Verification (Time: 00:00 – 01:00)",
            "Step 1: Navigate to chrome://extensions/ in Google Chrome.\n"
            "Step 2: Point to the 'Developer mode' toggle in the top-right corner to show it is enabled.\n"
            "Step 3: Click 'Load unpacked' and select the 'tabtime-extension' folder.\n"
            "Spoken Script: 'Examiners can observe that TabTime loads instantly without compilation or build steps. Notice the Manifest Version 3 badge and service worker status in the extensions manager. The background script background.js is registered cleanly as a native service worker.'",
            HEX_CYAN
        ),
        (
            "Stage 2: First-Launch GDPR Consent Modal (Time: 01:00 – 01:45)",
            "Step 1: Open the extension popup for the first time.\n"
            "Step 2: Demonstrate the initial Privacy & Data Protection Onboarding Modal.\n"
            "Step 3: Show the explicit user opt-in and confirmation of local storage.\n"
            "Spoken Script: 'In compliance with GDPR Article 25, TabTime greets new users with an explicit data sovereignty notice. Telemetry tracking remains disabled until the user actively confirms their informed consent.'",
            HEX_GREEN
        ),
        (
            "Stage 3: Real-Time Tab Tracking & Active Window Switching (Time: 01:45 – 03:00)",
            "Step 1: Navigate to 'wikipedia.org/wiki/Computer_science'. Notice the extension toolbar badge displaying active time in real-time.\n"
            "Step 2: Switch to 'google.com' (Neutral). Show the toolbar badge updating immediately.\n"
            "Step 3: Minimize the browser window for 5 seconds. Show that tracking pauses.\n"
            "Spoken Script: 'Notice how our window focus listener immediately halts tracking when the browser loses active focus, eliminating idle skewing. The toolbar badge reflects active time seamlessly.'",
            HEX_BLUE
        ),
        (
            "Stage 4: Popup Interface & Instant Productivity Scoring (Time: 03:00 – 04:15)",
            "Step 1: Click the TabTime toolbar icon to open popup.html.\n"
            "Step 2: Highlight the Productivity Score gauge (e.g. 84/100, 'Highly Focused').\n"
            "Step 3: Point to the animated Chart.js donut chart breaking down Productive, Neutral, and Distracting percentages.\n"
            "Step 4: Highlight the Top 3 Sites list with live minute counts.\n"
            "Spoken Script: 'Our popup renders in under 200 milliseconds. It provides immediate, non-intrusive behavioral feedback grounded in Bandura's self-monitoring theory.'",
            HEX_BLUE
        ),
        (
            "Stage 5: Full Analytics Dashboard Deep-Dive (Time: 04:15 – 06:00)",
            "Step 1: Click 'Open Full Dashboard' in the popup, launching dashboard.html.\n"
            "Step 2: Demonstrate the Weekly Trend Bar Chart showing daily focus patterns.\n"
            "Step 3: Demonstrate the Date Range Selector (Today, Last 7 Days, Last 30 Days).\n"
            "Step 4: Show the Category Breakdown table with exact time totals and percentages.\n"
            "Spoken Script: 'This full-screen dashboard queries local IndexedDB records asynchronously. Even with hundreds of domain log entries, Chart.js renders the time-series trends smoothly at 60 frames per second.'",
            HEX_CYAN
        ),
        (
            "Stage 6: Focus Mode & DeclarativeNetRequest Blocking (Time: 06:00 – 07:45)",
            "Step 1: In the dashboard or popup, toggle 'Focus Mode' ON and set a 15-minute focus session.\n"
            "Step 2: Attempt to open a new tab and navigate to 'youtube.com'.\n"
            "Step 3: Show that the browser instantaneously redirects to blocked.html before the video can load.\n"
            "Step 4: Highlight the serene blocked page with mindful reflection cues and remaining session countdown.\n"
            "Spoken Script: 'Observe the instantaneous network redirection. Because we compile dynamic rules via declarativeNetRequest, the browser intercepts the request at the network layer, preventing the distraction before a single byte of video data loads.'",
            HEX_AMBER
        ),
        (
            "Stage 7: Domain Rule Customization & Score Recalculation (Time: 07:45 – 08:45)",
            "Step 1: Navigate to settings.html.\n"
            "Step 2: Add a custom domain rule: reclassify 'youtube.com' from 'Distracting' to 'Productive' (e.g. for student tutorial viewing).\n"
            "Step 3: Return to the popup: show the immediate recalculation of the Productivity Score.\n"
            "Spoken Script: 'TabTime empowers users to tailor category definitions to their unique academic workflows, supporting metacognitive self-regulation.'",
            HEX_GREEN
        ),
        (
            "Stage 8: Live DevTools Zero-Network Proof & GDPR Erasure (Time: 08:45 – 10:00)",
            "Step 1: Open Chrome DevTools Network tab. Refresh the dashboard and browse tabs. Point out: 0 requests sent to external servers.\n"
            "Step 2: In settings.html, click 'Export Data as JSON'. Open the exported file to show clean, structured, human-readable JSON.\n"
            "Step 3: Click 'Purge All Data'. Inspect IndexedDB in DevTools Application tab: show that all object stores are cleanly emptied.\n"
            "Spoken Script: 'This concludes our empirical demonstration: zero remote telemetry, full data portability under GDPR Article 20, and absolute right to erasure under Article 17.'",
            HEX_NAVY
        )
    ]

    for title, desc, col in demo_steps:
        add_callout_box(
            doc,
            title,
            [desc],
            border_color=col,
            bg_color=HEX_BG_CARD,
            badge="LIVE DEMO ACTION"
        )

    # Contingency Fallback Plan
    add_callout_box(
        doc,
        "EMERGENCY CONTINGENCY & TECHNICAL FALLBACK PROTOCOL",
        [
            "Scenario A: Chrome Crashes or Browser Freezes during Demo.\n"
            "Resolution: Immediately open the secondary backup browser (Microsoft Edge or Brave), which is pre-configured with TabTime. Extension settings and test data are mirrored in both browsers.",
            "Scenario B: Service Worker shows 'Inactive' in Extensions Manager.\n"
            "Resolution: Explain to the panel: 'This is the expected, correct behavior of Chrome Manifest V3 service workers to save RAM. Clicking the extension icon wakes the worker in under 15 milliseconds.' Click the popup to demonstrate instant wake-up.",
            "Scenario C: Screen Projector / Video Connection Fails.\n"
            "Resolution: Refer to the high-resolution interface figures in the dissertation (Figures 6.2, 7.1, and Figure 5.1) and continue verbal delivery calmly from your physical script."
        ],
        border_color=HEX_RED,
        bg_color="FEF2F2",
        badge="CONTINGENCY PLAN"
    )

    # Save to both target locations
    print(f"Saving primary document to: {OUTPUT_DOCX_PRIMARY}")
    os.makedirs(os.path.dirname(OUTPUT_DOCX_PRIMARY), exist_ok=True)
    doc.save(OUTPUT_DOCX_PRIMARY)

    print(f"Saving root copy to: {OUTPUT_DOCX_ROOT}")
    doc.save(OUTPUT_DOCX_ROOT)
    print("SUCCESS: Viva and Supervisor Explanation Script Word Document created successfully!")

if __name__ == "__main__":
    build_script_document()
