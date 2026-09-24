"""
TabTime IRP Viva Presentation Generator - Refined Master Version
York St John University - School of Science, Technology & Health
Module: LDC6005M Individual Research Project
"""

import os
import sys
import time
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import win32com.client

# Palette
C_NAVY = RGBColor(15, 23, 42)       # #0F172A - Deep Slate / Navy
C_BLUE = RGBColor(29, 78, 216)      # #1D4ED8 - Royal Blue Accent
C_CYAN = RGBColor(2, 132, 199)      # #0284C7 - Teal / Cyan Accent
C_SLATE = RGBColor(71, 85, 105)     # #475569 - Secondary text
C_MUTED = RGBColor(100, 116, 139)   # #64748B - Muted text
C_BG_CARD = RGBColor(248, 250, 252) # #F8FAFC - Card background
C_BG_ALT = RGBColor(241, 245, 249)  # #F1F5F9 - Alternate card background
C_BORDER = RGBColor(203, 213, 225)  # #CBD5E1 - Card border
C_WHITE = RGBColor(255, 255, 255)
C_GREEN = RGBColor(5, 150, 105)     # #059669 - Green badge
C_AMBER = RGBColor(217, 119, 6)     # #D97706 - Amber badge

FONT_HEADING = "Segoe UI"
FONT_BODY = "Calibri"

WORKSPACE_DIR = r"D:\My Project\Browser Extenstion project"
TEMPLATE_PATH = os.path.join(WORKSPACE_DIR, "IRP (Viva Presentation slide Template).pptx")
OUTPUT_PPTX = os.path.join(WORKSPACE_DIR, "TabTime_IRP_Viva_Presentation_Final.pptx")
PREVIEW_DIR = os.path.join(WORKSPACE_DIR, "presentation_slides_preview")

YSJ_LOGO_PATH = os.path.join(WORKSPACE_DIR, "images", "ysj_logo.png")
TABTIME_LOGO_PATH = os.path.join(WORKSPACE_DIR, "tabtime-extension", "icons", "icon128.png")

def format_para(p, text, font_name=FONT_BODY, size_pt=14, bold=False, color=C_NAVY, align=PP_ALIGN.LEFT, space_after_pt=6):
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(size_pt)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    p.space_after = Pt(space_after_pt)

def add_card(slide, left, top, width, height, bg_color=C_BG_CARD, border_color=C_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

def add_header_badge(slide, text, left, top, width=Inches(3.0), height=Inches(0.35), bg_color=C_BLUE, text_color=C_WHITE):
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    p = badge.text_frame.paragraphs[0]
    p.text = text
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return badge

def clean_placeholder(slide):
    for shape in list(slide.shapes):
        if shape.name == "Title 1" or shape.shape_type == 9:
            continue
        if "Placeholder" in shape.name or (shape.has_text_frame and any(w in shape.text_frame.text for w in ["Add your content here", "Table of Content", "Invite questions"])):
            sp = shape._element
            sp.getparent().remove(sp)

def setup_slide_header(slide, title_text, category_badge="LDC6005M VIVA PRESENTATION"):
    if len(slide.shapes) > 0 and slide.shapes[0].has_text_frame:
        t_shape = slide.shapes[0]
        t_shape.text_frame.text = ""
        p = t_shape.text_frame.paragraphs[0]
        format_para(p, title_text, FONT_HEADING, 25, bold=True, color=C_NAVY, space_after_pt=0)
        
    add_header_badge(slide, category_badge, Inches(0.6), Inches(0.18), Inches(3.2), Inches(0.28), C_BLUE, C_WHITE)

def build_presentation():
    print(f"Loading template: {TEMPLATE_PATH}")
    prs = Presentation(TEMPLATE_PATH)
    
    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Refined layout avoiding background collisions)
    # -------------------------------------------------------------
    print("Building Slide 1: Title Slide")
    s1 = prs.slides[0]
    for shp in list(s1.shapes):
        if shp.has_text_frame or shp.shape_type == 9: # line
            sp = shp._element
            sp.getparent().remove(sp)
            
    # TabTime Logo at top left
    if os.path.exists(TABTIME_LOGO_PATH):
        s1.shapes.add_picture(TABTIME_LOGO_PATH, Inches(0.8), Inches(0.65), width=Inches(1.05))
        
    # Badge next to TabTime logo
    add_header_badge(s1, "BSc (Hons) Computer Science | Final Technical Viva Voce", Inches(2.05), Inches(0.85), Inches(5.0), Inches(0.38), C_BLUE, C_WHITE)

    # Main Title Area
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(11.6), Inches(1.9))
    tf = tb_title.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    format_para(p1, "TAB TIME", FONT_HEADING, 40, bold=True, color=C_NAVY, space_after_pt=4)
    p2 = tf.add_paragraph()
    format_para(p2, "A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management", FONT_HEADING, 19, bold=False, color=C_BLUE, space_after_pt=8)
    p3 = tf.add_paragraph()
    format_para(p3, "School of Science, Technology & Health | York St John University (London Campus)", FONT_BODY, 13, bold=False, color=C_SLATE, space_after_pt=0)

    # Metadata Cards (Student & Supervisor)
    card_stu = add_card(s1, Inches(0.8), Inches(4.2), Inches(5.6), Inches(2.3))
    tf_stu = card_stu.text_frame
    tf_stu.word_wrap = True
    tf_stu.margin_left = tf_stu.margin_top = Inches(0.25)
    p = tf_stu.paragraphs[0]
    format_para(p, "PRESENTER & CANDIDATE DETAILS", FONT_HEADING, 11, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf_stu.add_paragraph()
    format_para(p, "• Student Name: [Your Name / Candidate]", FONT_BODY, 13, bold=True, color=C_NAVY, space_after_pt=3)
    p = tf_stu.add_paragraph()
    format_para(p, "• Student ID: [Student ID / Number]", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=3)
    p = tf_stu.add_paragraph()
    format_para(p, "• Degree Programme: BSc (Hons) Computer Science", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=3)
    p = tf_stu.add_paragraph()
    format_para(p, "• Email: [Student Email / YSJ Account]", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=0)

    card_mod = add_card(s1, Inches(6.8), Inches(4.2), Inches(5.6), Inches(2.3))
    tf_mod = card_mod.text_frame
    tf_mod.word_wrap = True
    tf_mod.margin_left = tf_mod.margin_top = Inches(0.25)
    p = tf_mod.paragraphs[0]
    format_para(p, "ACADEMIC ASSESSMENT METADATA", FONT_HEADING, 11, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf_mod.add_paragraph()
    format_para(p, "• Module: LDC6005M Individual Research Project", FONT_BODY, 13, bold=True, color=C_NAVY, space_after_pt=3)
    p = tf_mod.add_paragraph()
    format_para(p, "• Assessment: Component 3 – Technical Viva Voce Defense", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=3)
    p = tf_mod.add_paragraph()
    format_para(p, "• Project Supervisor: [Project Supervisor Name]", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=3)
    p = tf_mod.add_paragraph()
    format_para(p, "• Academic Session: 2025 / 2026 | Submission: June 2026", FONT_BODY, 12, bold=False, color=C_SLATE, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 2: Assessment Coversheet
    # -------------------------------------------------------------
    print("Building Slide 2: Coversheet")
    s2 = prs.slides[1]
    for shp in s2.shapes:
        if shp.has_table:
            tbl = shp.table
            coversheet_data = [
                ("The Coversheet", "Module: LDC6005M Individual Research Project (Component 3)"),
                ("Student Name  (unless anonymised)", "[Student Name / Candidate]"),
                ("Student Number  (as shown on student ID card):", "[Student ID Number]"),
                ("Word Count / Pages / Duration / Other Limits:", "20 Minutes Presentation + 10 Minutes Q&A / Panel Defense"),
                ("Assessment component number (1,2 or 3)", "Component 3 (Oral Presentation & Viva Voce)"),
                ("Assessment type", "Technical Viva Voce Presentation & System Demonstration"),
                ("Attempt Number:", "Attempt 1 (First Sit)"),
                ("Date of Submission:", "Academic Year 2025 / 2026 (June 2026)")
            ]
            for r_idx, (col0, col1) in enumerate(coversheet_data):
                if r_idx < len(tbl.rows):
                    cell0 = tbl.cell(r_idx, 0)
                    cell1 = tbl.cell(r_idx, 1)
                    cell0.text = col0
                    cell1.text = col1
                    
                    for p in cell0.text_frame.paragraphs:
                        p.font.name = FONT_HEADING
                        p.font.size = Pt(12)
                        p.font.bold = True
                        p.font.color.rgb = C_NAVY
                    for p in cell1.text_frame.paragraphs:
                        p.font.name = FONT_BODY
                        p.font.size = Pt(12)
                        p.font.bold = (r_idx == 0 or r_idx == 4)
                        p.font.color.rgb = C_BLUE if (r_idx == 0 or r_idx == 4) else C_NAVY

    # -------------------------------------------------------------
    # SLIDE 3: Declarations (Refined Table 5 & Table 7)
    # -------------------------------------------------------------
    print("Building Slide 3: Declarations")
    s3 = prs.slides[2]
    for shp in s3.shapes:
        if shp.has_table:
            tbl = shp.table
            if len(tbl.columns) == 2 and len(tbl.rows) == 3: # Table 5
                tbl.cell(0, 0).text = "Academic Misconduct Statement:\nI confirm that this work is entirely my own independent research and implementation."
                tbl.cell(0, 1).text = "✔ Confirmed & Understood"
                tbl.cell(1, 0).text = "Generative Artificial Intelligence Statement:\nAI tools were used strictly in compliance with YSJ guidelines for code refinement and testing assistance."
                tbl.cell(1, 1).text = "✔ Confirmed & Compliant"
                tbl.cell(2, 0).text = "Module Learning Outcomes (LO1–LO5):\nI confirm that all five prescribed learning outcomes for LDC6005M have been comprehensively met."
                tbl.cell(2, 1).text = "✔ All Prescribed LOs Met"
                for r in tbl.rows:
                    for c in r.cells:
                        for p in c.text_frame.paragraphs:
                            p.font.size = Pt(11)
                            p.font.name = FONT_BODY
                            if "✔" in p.text:
                                p.font.bold = True
                                p.font.color.rgb = C_GREEN
            elif len(tbl.columns) == 1 and len(tbl.rows) >= 2: # Table 7 (Self-Assessment)
                cell0 = tbl.cell(0, 0)
                cell0.text = "Self-Assessment & Critical Reflection (LDC6005M Viva Voce Defense)"
                cell0.fill.solid()
                cell0.fill.fore_color.rgb = C_BLUE
                for p in cell0.text_frame.paragraphs:
                    p.font.name = FONT_HEADING
                    p.font.size = Pt(12)
                    p.font.bold = True
                    p.font.color.rgb = C_WHITE

                cell1 = tbl.cell(1, 0)
                cell1.text = (
                    "• Progress & Technical Learning: Overcame complex Manifest V3 ephemeral service worker lifecycles by designing an event-driven debounce mechanism and asynchronous IndexedDB storage layer.\n"
                    "• Strongest Submission Asset: The rigorous empirical evaluation (n = 65 participants) achieving a System Usability Scale (SUS) score of 89.04/100 (Grade A), backed by ground-truth stopwatch validation.\n"
                    "• Constructive Reflection: Future iterations will incorporate WebAssembly-driven on-device NLP to provide semantic categorization without relying on cloud processing."
                )
                for p in cell1.text_frame.paragraphs:
                    p.font.size = Pt(10.5)
                    p.font.name = FONT_BODY

                if len(tbl.rows) >= 3:
                    cell2 = tbl.cell(2, 0)
                    cell2.text = "Formal Declaration: I certify that the information provided in this viva presentation accurately reflects my independent technical implementation and empirical research."
                    for p in cell2.text_frame.paragraphs:
                        p.font.size = Pt(9.5)
                        p.font.name = FONT_BODY
                        p.font.italic = True
                        p.font.color.rgb = C_SLATE

    # -------------------------------------------------------------
    # SLIDE 4: Table of Content
    # -------------------------------------------------------------
    print("Building Slide 4: Table of Contents")
    s4 = prs.slides[3]
    setup_slide_header(s4, "Table of Contents: Presentation Roadmap", "AGENDA & STRUCTURE")
    clean_placeholder(s4)

    agenda_items = [
        ("01", "Context & Problem Statement", "Digital wellbeing crisis, attention fragmentation, surveillance capitalism & cloud tracking vulnerabilities.", Inches(0.6), Inches(1.8)),
        ("02", "Aims, Objectives & Hypotheses", "Main aim, 5 measurable objectives, central research question, and formal testable hypotheses (H1, H2).", Inches(6.5), Inches(1.8)),
        ("03", "Literature Review & Benchmark", "Theories of self-regulation, cognitive interruption costs, Manifest V2 vs V3, comparative matrix.", Inches(0.6), Inches(3.4)),
        ("04", "DSR Methodology & Architecture", "Design Science Research model, Three-Layer architecture, telemetry data flow, participant cohort (n=65).", Inches(6.5), Inches(3.4)),
        ("05", "Empirical Results & Discussion", "SUS Score (89.04 / 100), feature utility, stopwatch accuracy, technical challenges, ethics & future roadmap.", Inches(0.6), Inches(5.0)),
    ]
    for num, title, desc, l, t in agenda_items:
        card = add_card(s4, l, t, Inches(5.5), Inches(1.35))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.15)
        p = tf.paragraphs[0]
        format_para(p, f"PHASE {num} : {title.upper()}", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=4)
        p2 = tf.add_paragraph()
        format_para(p2, desc, FONT_BODY, 11, bold=False, color=C_SLATE, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 5: Introduction
    # -------------------------------------------------------------
    print("Building Slide 5: Introduction")
    s5 = prs.slides[4]
    setup_slide_header(s5, "1. Introduction & Research Context", "CHAPTER 1: INTRODUCTION")
    clean_placeholder(s5)

    card1 = add_card(s5, Inches(0.6), Inches(1.8), Inches(6.0), Inches(4.8))
    tf1 = card1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.25)
    tf1.margin_top = Inches(0.25)
    
    p = tf1.paragraphs[0]
    format_para(p, "THE DIGITAL WELLBEING LANDSCAPE", FONT_HEADING, 13, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf1.add_paragraph()
    format_para(p, "• Frictionless Web Environments: Over 80% of modern academic research, study, and professional knowledge work is conducted directly inside web browsers.", FONT_BODY, 12, color=C_NAVY, space_after_pt=8)
    p = tf1.add_paragraph()
    format_para(p, "• Attention Fragmentation Crisis: Single-click access to social feeds and algorithmic entertainment fragments cognitive focus; recovering from an interruption requires up to 23 minutes (Mark et al., 2008).", FONT_BODY, 12, color=C_NAVY, space_after_pt=8)
    p = tf1.add_paragraph()
    format_para(p, "• The TabTime Solution: A lightweight, client-side browser extension engineered under Manifest V3 that provides real-time time awareness, visual analytics, and non-coercive focus management.", FONT_BODY, 12, color=C_NAVY, space_after_pt=8)
    p = tf1.add_paragraph()
    format_para(p, "• Privacy-by-Design Core: Completely operates on the user's local machine with zero external cloud telemetry, guaranteeing total user data sovereignty and GDPR compliance.", FONT_BODY, 12, color=C_NAVY, space_after_pt=0)

    img_fig1 = os.path.join(WORKSPACE_DIR, "images", "diagrams", "fig1_conceptual_overview.png")
    if os.path.exists(img_fig1):
        s5.shapes.add_picture(img_fig1, Inches(6.8), Inches(1.8), width=Inches(5.6))
        tb = s5.shapes.add_textbox(Inches(6.8), Inches(5.6), Inches(5.6), Inches(0.8))
        format_para(tb.text_frame.paragraphs[0], "Figure 1.1: Conceptual Overview of TabTime Mindful Digital Engagement Pipeline", FONT_BODY, 11, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 6: Problem Statement
    # -------------------------------------------------------------
    print("Building Slide 6: Problem Statement")
    s6 = prs.slides[5]
    setup_slide_header(s6, "2. Problem Statement & Research Motives", "CHAPTER 1: PROBLEM STATEMENT")
    clean_placeholder(s6)

    cards_p = [
        ("SURVEILLANCE CAPITALISM IN TRACKERS", 
         "Commercial tools (e.g. RescueTime, Toggl) mandate continuous cloud synchronization, harvesting full URL streams and timestamps to external servers. This creates severe privacy vulnerabilities and corporate surveillance risks (Zuboff, 2019; GDPR Art. 5).",
         Inches(0.6), Inches(1.8), Inches(5.5), Inches(2.2), C_AMBER),
        ("THE FUNCTIONAL BINARY DICHOTOMY",
         "Existing solutions exhibit a stark functional divide: they either offer passive retrospective logging without active intervention, or enforce rigid, punitive website blocking that induces user frustration without encouraging reflective mindfulness.",
         Inches(6.5), Inches(1.8), Inches(5.5), Inches(2.2), C_BLUE),
        ("LACK OF REAL-TIME BEHAVIORAL NUDGES",
         "Users rarely comprehend cumulative micro-distractions during active browsing. Without instantaneous, transparent productivity scoring and gentle redirection, time slips away unnoticed across cognitive context switches (Mark et al., 2008).",
         Inches(0.6), Inches(4.3), Inches(5.5), Inches(2.3), C_NAVY),
        ("THE TABTIME RESEARCH OPPORTUNITY",
         "A privacy-preserving, on-device architecture merging automated millisecond tracking, instant mathematical scoring, and non-coercive focus interventions directly within modern browser sandboxes without remote infrastructure.",
         Inches(6.5), Inches(4.3), Inches(5.5), Inches(2.3), C_GREEN)
    ]
    for title, text, l, t, w, h, acc in cards_p:
        c = add_card(s6, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=6)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 7: Aims and Objectives
    # -------------------------------------------------------------
    print("Building Slide 7: Aims & Objectives")
    s7 = prs.slides[6]
    setup_slide_header(s7, "3. Research Aims, Objectives & Hypotheses", "CHAPTER 1: AIMS & OBJECTIVES")
    clean_placeholder(s7)

    c_left = add_card(s7, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9))
    tf = c_left.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)

    p = tf.paragraphs[0]
    format_para(p, "OVERARCHING PROJECT AIM", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "To design, develop, and empirically evaluate a privacy-preserving browser extension that promotes digital wellbeing and time awareness through real-time tracking, productivity analytics, and focus management.", FONT_BODY, 11, bold=True, color=C_NAVY, space_after_pt=10)

    p = tf.add_paragraph()
    format_para(p, "CENTRAL RESEARCH QUESTION", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "Can a browser extension combining automated time tracking, visual analytics, and focus management improve users' awareness of digital habits and reduce online distractions without compromising privacy?", FONT_BODY, 11, color=C_NAVY, space_after_pt=10)

    p = tf.add_paragraph()
    format_para(p, "FORMAL RESEARCH HYPOTHESES", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "• H1: Active monitoring via automated tracking and visual feedback significantly improves temporal awareness and personal self-regulation.", FONT_BODY, 11, color=C_NAVY, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "• H2: Dynamic focus sessions with non-coercive redirection significantly reduce distraction-related interruptions during focused tasks.", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    img_fig2 = os.path.join(WORKSPACE_DIR, "images", "diagrams", "fig2_main_aim.png")
    if os.path.exists(img_fig2):
        s7.shapes.add_picture(img_fig2, Inches(6.7), Inches(1.8), width=Inches(5.7))
        tb = s7.shapes.add_textbox(Inches(6.7), Inches(5.6), Inches(5.7), Inches(0.8))
        format_para(tb.text_frame.paragraphs[0], "Figure 1.2: Project Main Aim and Core Research Objectives Framework", FONT_BODY, 11, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 8: Literature Review Summary
    # -------------------------------------------------------------
    print("Building Slide 8: Literature Review")
    s8 = prs.slides[7]
    setup_slide_header(s8, "4. Literature Review & Comparative Analysis", "CHAPTER 2: LITERATURE REVIEW")
    clean_placeholder(s8)

    c_th = add_card(s8, Inches(0.6), Inches(1.8), Inches(11.5), Inches(1.3))
    tf = c_th.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.12)
    p = tf.paragraphs[0]
    format_para(p, "THEORETICAL FOUNDATIONS & HCI FRAMEWORKS", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "• Grounded in Self-Regulation Theory (Bandura, 1991), Attention Restoration Theory (Kaplan, 1995), and Cognitive Load Theory (Sweller, 1988).\n• Manifest V3 Paradigm Shift: Chrome MV3 enforces service workers, declarativeNetRequest, and eliminates arbitrary remote code execution, demanding a radical overhaul of extension design.", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    rows = 6
    cols = 6
    tbl_shape = s8.shapes.add_table(rows, cols, Inches(0.6), Inches(3.3), Inches(11.5), Inches(3.4))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(2.0)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(1.7)
    tbl.columns[4].width = Inches(1.8)
    tbl.columns[5].width = Inches(1.7)

    headers = ["Evaluation Metric", "TabTime (Ours)", "RescueTime", "Toggl Track", "StayFocusd", "Forest"]
    matrix_data = [
        ("100% Local Privacy (No Cloud)", "✔ Yes (IndexedDB)", "✖ No (Remote Cloud)", "✖ No (Remote Cloud)", "✔ Yes (Local Storage)", "✖ No (Cloud Sync)"),
        ("Real-Time Productivity Score", "✔ Instant Formula", "✔ Proprietary Cloud", "✖ None (Manual)", "✖ None (Limit Only)", "✖ Gamified Tree"),
        ("Modern Manifest V3 Support", "✔ Native MV3 Engine", "✖ Legacy MV2 Script", "✖ Web / Desktop", "✖ Legacy MV2 Extension", "✖ Mobile App"),
        ("Dynamic Rule Redirection", "✔ declarativeNetRequest", "✖ Hard Blocking", "✖ None", "✔ DOM Blocking", "✖ App Locking"),
        ("Cost & Open Source License", "✔ 100% Free & Open", "✖ Paid Sub ($12/mo)", "✖ Paid Sub ($9/mo)", "✔ Free / Proprietary", "✖ Freemium")
    ]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BLUE if c_idx == 1 else C_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.name = FONT_HEADING
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.alignment = PP_ALIGN.CENTER

    for r_idx, row in enumerate(matrix_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if c_idx == 1 else (C_BG_CARD if r_idx % 2 == 0 else C_WHITE)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.name = FONT_BODY
                p.font.bold = (c_idx == 1 or c_idx == 0)
                if c_idx == 1:
                    p.font.color.rgb = C_BLUE
                elif "✔" in val:
                    p.font.color.rgb = C_GREEN
                elif "✖" in val:
                    p.font.color.rgb = RGBColor(220, 38, 38)
                else:
                    p.font.color.rgb = C_NAVY
                p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 9: Methodology
    # -------------------------------------------------------------
    print("Building Slide 9: Methodology")
    s9 = prs.slides[8]
    setup_slide_header(s9, "5. Design Science Methodology & Architecture", "CHAPTER 4 & 5: METHODOLOGY")
    clean_placeholder(s9)

    c_m = add_card(s9, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9))
    tf = c_m.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    format_para(p, "DESIGN SCIENCE RESEARCH (DSR) PARADIGM", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• DSR Framework (Hevner et al., 2004): Structured iterative engineering consisting of problem identification, artifact design, laboratory testing, and empirical evaluation.", FONT_BODY, 11, color=C_NAVY, space_after_pt=8)
    p = tf.add_paragraph()
    format_para(p, "THREE-LAYER SYSTEM ARCHITECTURE", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "1. Presentation Layer: Clean UI popup (`popup.html`), full-screen analytics dashboard (`dashboard.html`), and rule configuration view (`settings.html`).", FONT_BODY, 11, color=C_NAVY, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "2. Logic Engine Layer: Manifest V3 background service worker (`background.js`), window focus tracking, tab lifecycle listener, and idle debounce detector.", FONT_BODY, 11, color=C_NAVY, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "3. Local Data Persistence Layer: Client-side storage abstraction (`storage.js`) backed by browser IndexedDB and `chrome.storage.local`.", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    img_fig4 = os.path.join(WORKSPACE_DIR, "images", "diagrams", "fig4_three_layer_architecture.png")
    if os.path.exists(img_fig4):
        s9.shapes.add_picture(img_fig4, Inches(6.7), Inches(1.8), width=Inches(5.7))
        tb = s9.shapes.add_textbox(Inches(6.7), Inches(5.6), Inches(5.7), Inches(0.8))
        format_para(tb.text_frame.paragraphs[0], "Figure 5.1: Three-Layer System Architecture (Presentation, Logic, Local Storage)", FONT_BODY, 11, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 10: Data Collection Process
    # -------------------------------------------------------------
    print("Building Slide 10: Data Collection Process")
    s10 = prs.slides[9]
    setup_slide_header(s10, "6. Data Collection Process & Telemetry Pipeline", "CHAPTER 4: DATA COLLECTION")
    clean_placeholder(s10)

    c_dc = add_card(s10, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9))
    tf = c_dc.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    format_para(p, "DUAL-STREAM EVALUATION STRATEGY", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Stream 1: Automated Client-Side Telemetry: Captures active tab timestamps, window focus events, and domain transitions with a 60-second idle debounce threshold.", FONT_BODY, 11, color=C_NAVY, space_after_pt=8)
    p = tf.add_paragraph()
    format_para(p, "• Stream 2: Google Forms Empirical Study: Comprehensive 25-question survey capturing user demographics, 10-item System Usability Scale (SUS), feature ratings, and behavioral impact.", FONT_BODY, 11, color=C_NAVY, space_after_pt=8)
    p = tf.add_paragraph()
    format_para(p, "PARTICIPANT COHORT DEMOGRAPHICS (n = 65)", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Undergraduate Students: 47.7% (31 participants)\n• Knowledge Workers & Professionals: 27.7% (18 participants)\n• Postgraduate Researchers: 10.8% (7 participants)\n• Academic Faculty: 13.8% (9 participants)\n• Browser Distribution: Google Chrome (78.5%), Brave (10.8%), Edge (6.2%), Firefox (4.6%).", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    img_demo = os.path.join(WORKSPACE_DIR, "images", "charts", "fig_gform_demographics.png")
    if os.path.exists(img_demo):
        s10.shapes.add_picture(img_demo, Inches(6.7), Inches(1.8), width=Inches(5.7))
        tb = s10.shapes.add_textbox(Inches(6.7), Inches(5.6), Inches(5.7), Inches(0.8))
        format_para(tb.text_frame.paragraphs[0], "Figure 6.1: Google Forms Evaluation Participant Demographic Profile (n = 65)", FONT_BODY, 11, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 11: Results Presentation
    # -------------------------------------------------------------
    print("Building Slide 11: Results Presentation")
    s11 = prs.slides[10]
    setup_slide_header(s11, "7. Results Presentation: Usability & Feature Ratings", "CHAPTER 6: RESULTS")
    clean_placeholder(s11)

    banner = add_card(s11, Inches(0.6), Inches(1.75), Inches(11.5), Inches(0.8), C_BLUE, C_BLUE)
    p = banner.text_frame.paragraphs[0]
    format_para(p, "SYSTEM USABILITY SCALE (SUS) COMPOSITE SCORE: 89.04 / 100  |  GRADE A (TOP 10% PERCENTILE)", FONT_HEADING, 14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER, space_after_pt=0)

    img_sus = os.path.join(WORKSPACE_DIR, "images", "charts", "fig_gform_sus_breakdown.png")
    if os.path.exists(img_sus):
        s11.shapes.add_picture(img_sus, Inches(0.6), Inches(2.7), width=Inches(5.6))
        tb = s11.shapes.add_textbox(Inches(0.6), Inches(6.1), Inches(5.6), Inches(0.5))
        format_para(tb.text_frame.paragraphs[0], "Figure 6.2: System Usability Scale (SUS) 10-Item Breakdown (Mean = 89.04)", FONT_BODY, 10, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    img_feat = os.path.join(WORKSPACE_DIR, "images", "charts", "fig_gform_feature_ratings.png")
    if os.path.exists(img_feat):
        s11.shapes.add_picture(img_feat, Inches(6.5), Inches(2.7), width=Inches(5.6))
        tb = s11.shapes.add_textbox(Inches(6.5), Inches(6.1), Inches(5.6), Inches(0.5))
        format_para(tb.text_frame.paragraphs[0], "Figure 6.3: Feature Utility & Satisfaction Ratings (Tracking: 95.4%, Focus: 92.3%)", FONT_BODY, 10, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 12: Results Analysis & Interpretation
    # -------------------------------------------------------------
    print("Building Slide 12: Results Analysis")
    s12 = prs.slides[11]
    setup_slide_header(s12, "8. Results Analysis & Hypotheses Interpretation", "CHAPTER 6: ANALYSIS")
    clean_placeholder(s12)

    c_an = add_card(s12, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9))
    tf = c_an.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    format_para(p, "HYPOTHESES VALIDATION SUMMARY", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Hypothesis H1 Confirmed: 95.4% of participants reported heightened awareness of digital habits; 89.2% demonstrated improved self-regulation.", FONT_BODY, 11, bold=True, color=C_NAVY, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Hypothesis H2 Confirmed: 93.8% reported substantial reduction in distraction interruptions during work and study sessions.", FONT_BODY, 11, bold=True, color=C_NAVY, space_after_pt=8)

    p = tf.add_paragraph()
    format_para(p, "GROUND-TRUTH STOPWATCH ACCURACY", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Timing Precision: Mean deviation of ±1.8 seconds compared to external physical stopwatch benchmarks across 1-hour sessions (99.85% tracking accuracy).", FONT_BODY, 11, color=C_NAVY, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Lightweight System Overhead: Memory consumption stabilized between 14 MB and 22 MB RAM, with <0.5% CPU utilization during background polling.", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    img_bh = os.path.join(WORKSPACE_DIR, "images", "charts", "fig_gform_behavioral_impact.png")
    if os.path.exists(img_bh):
        s12.shapes.add_picture(img_bh, Inches(6.7), Inches(1.8), width=Inches(5.7))
        tb = s12.shapes.add_textbox(Inches(6.7), Inches(5.6), Inches(5.7), Inches(0.8))
        format_para(tb.text_frame.paragraphs[0], "Figure 6.4: Self-Reported Behavioral Impact on Time Awareness and Distraction Reduction", FONT_BODY, 11, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 13: Challenges and Limitations
    # -------------------------------------------------------------
    print("Building Slide 13: Challenges & Limitations")
    s13 = prs.slides[12]
    setup_slide_header(s13, "9. Engineering Challenges & Problem Resolution", "CHAPTER 5: CHALLENGES")
    clean_placeholder(s13)

    cards_c = [
        ("1. MV3 SERVICE WORKER EPHEMERALITY",
         "Chrome MV3 terminates idle service workers after 30 seconds. In-flight session timers risk corruption. RESOLUTION: Implemented event-driven state hydration via chrome.storage.local with immediate state flushing on suspend.",
         Inches(0.6), Inches(1.8), Inches(5.5), Inches(2.2), C_BLUE),
        ("2. INDEXEDDB TRANSACTION CONTENTION",
         "Rapid tab switching caused concurrent asynchronous write collisions and lock timeouts. RESOLUTION: Engineered a serialized First-In-First-Out (FIFO) queue for batching disk transactions safely.",
         Inches(6.5), Inches(1.8), Inches(5.5), Inches(2.2), C_CYAN),
        ("3. DECLARATIVENETREQUEST MIGRATION",
         "MV3 deprecated blocking webRequest APIs. Dynamic redirect rules required schema adaptation. RESOLUTION: Created a dynamic ruleset compiler mapping user blocklists directly to local redirection headers.",
         Inches(0.6), Inches(4.3), Inches(5.5), Inches(2.3), C_AMBER),
        ("4. STUDY LIMITATIONS & GENERALIZABILITY",
         "Sample cohort (n = 65) was predominantly desktop Chromium users (Chrome, Edge, Brave). Mobile browsers and longitudinal multi-month habit shifts remain outside current research boundaries.",
         Inches(6.5), Inches(4.3), Inches(5.5), Inches(2.3), C_SLATE)
    ]
    for title, text, l, t, w, h, acc in cards_c:
        c = add_card(s13, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=6)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 14: Discussion (Refined height to avoid overlap)
    # -------------------------------------------------------------
    print("Building Slide 14: Discussion")
    s14 = prs.slides[13]
    setup_slide_header(s14, "10. Critical Discussion & Project Contributions", "CHAPTER 7: DISCUSSION")
    clean_placeholder(s14)

    c_dis = add_card(s14, Inches(0.6), Inches(1.8), Inches(6.2), Inches(4.9))
    tf = c_dis.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    format_para(p, "THEORETICAL & HCI CONTRIBUTIONS", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Validating Non-Coercive Interventions: Demonstrates that immediate visual feedback (Chart.js donuts, productivity scoring) fosters sustained behavioral reflection without punitive locks.", FONT_BODY, 11, color=C_NAVY, space_after_pt=8)
    p = tf.add_paragraph()
    format_para(p, "PRACTICAL SOFTWARE ENGINEERING IMPACT", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Debunking the Cloud Surveillance Myth: Confirms that enterprise-grade time tracking does NOT require central server telemetry or privacy compromises.", FONT_BODY, 11, color=C_NAVY, space_after_pt=8)
    p = tf.add_paragraph()
    format_para(p, "PROFESSIONAL BCS STANDARDS COMPLIANCE", FONT_HEADING, 12, bold=True, color=C_BLUE, space_after_pt=6)
    p = tf.add_paragraph()
    format_para(p, "• Upholds the British Computer Society (BCS) Code of Conduct by safeguarding public interest, ensuring total data security, and adhering to W3C open standards.", FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # Right Column: Dashboard UI Screenshot with controlled height
    img_dash = os.path.join(WORKSPACE_DIR, "images", "screenshots", "interface", "fig_ui_dashboard.png")
    if os.path.exists(img_dash):
        # 644x704: Height=4.1in gives Width=3.75in
        s14.shapes.add_picture(img_dash, Inches(7.4), Inches(1.8), height=Inches(4.1))
        tb = s14.shapes.add_textbox(Inches(7.1), Inches(6.05), Inches(4.5), Inches(0.6))
        format_para(tb.text_frame.paragraphs[0], "Figure 7.1: Interactive Analytics Dashboard (Chart.js & IndexedDB)", FONT_BODY, 10.5, bold=True, color=C_SLATE, align=PP_ALIGN.CENTER)

    # -------------------------------------------------------------
    # SLIDE 15: Future Work
    # -------------------------------------------------------------
    print("Building Slide 15: Future Work")
    s15 = prs.slides[14]
    setup_slide_header(s15, "11. Recommendations for Future Work", "CHAPTER 8: FUTURE WORK")
    clean_placeholder(s15)

    cards_fw = [
        ("1. ON-DEVICE NLP CATEGORIZATION",
         "Incorporate WebAssembly-based micro-LLMs or TensorFlow.js to semantically categorize web page content directly on-device without transmitting text to third-party APIs.",
         Inches(0.6), Inches(1.8), Inches(5.5), Inches(2.2), C_BLUE),
        ("2. CLIENT-SIDE ZERO-KNOWLEDGE SYNC",
         "Engineer end-to-end encrypted synchronization utilizing Web Cryptography API (AES-GCM-256) via personal cloud containers (WebDAV, Google Drive, iCloud).",
         Inches(6.5), Inches(1.8), Inches(5.5), Inches(2.2), C_CYAN),
        ("3. MOBILE EXTENSION COMPATIBILITY",
         "Port background worker scripts to mobile browser runtimes (Firefox for Android and Safari iOS) to track and harmonize mobile attention patterns.",
         Inches(0.6), Inches(4.3), Inches(5.5), Inches(2.3), C_GREEN),
        ("4. ADAPTIVE BIOMETRIC & AUDIO PACING",
         "Integrate adaptive Pomodoro intervals driven by passive fatigue indicators, accompanied by subtle binaural ambient audio cues to ease task transitions.",
         Inches(6.5), Inches(4.3), Inches(5.5), Inches(2.3), C_NAVY)
    ]
    for title, text, l, t, w, h, acc in cards_fw:
        c = add_card(s15, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=6)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 16: Conclusion
    # -------------------------------------------------------------
    print("Building Slide 16: Conclusion")
    s16 = prs.slides[15]
    setup_slide_header(s16, "12. Project Conclusions & Core Takeaways", "CHAPTER 7: CONCLUSION")
    clean_placeholder(s16)

    cards_con = [
        ("OVERALL PROJECT OUTCOME & ARTEFACT SUCCESS",
         "Successfully designed, implemented, and validated TabTime—an open-source, production-ready browser extension operating under Manifest V3 that delivers real-time time tracking, productivity analytics, and focus management with 100% on-device privacy.",
         Inches(0.6), Inches(1.8), Inches(11.5), Inches(1.4), C_BLUE),
        ("DEFINITIVE RESOLUTION OF RESEARCH QUESTION",
         "Demonstrated that non-coercive behavioral nudges paired with immediate visual analytics significantly enhance user temporal awareness (95.4%) and reduce online distractions (93.8%), validating both core research hypotheses (H1 & H2).",
         Inches(0.6), Inches(3.45), Inches(11.5), Inches(1.4), C_CYAN),
        ("ACADEMIC & INDUSTRY SIGNIFICANCE",
         "Achieved a top-tier System Usability Scale (SUS) score of 89.04/100 (Grade A), proving that rigorous privacy-by-design principles can coexist with high-precision temporal tracking without server reliance.",
         Inches(0.6), Inches(5.1), Inches(11.5), Inches(1.4), C_GREEN)
    ]
    for title, text, l, t, w, h, acc in cards_con:
        c = add_card(s16, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.15)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=4)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 17: Ethics Consideration
    # -------------------------------------------------------------
    print("Building Slide 17: Ethics Consideration")
    s17 = prs.slides[16]
    setup_slide_header(s17, "13. Ethical Considerations & Regulatory Governance", "ETHICS & GOVERNANCE")
    clean_placeholder(s17)

    cards_eth = [
        ("YSJ ETHICAL APPROVAL",
         "Formal ethical clearance obtained under York St John University School of Science, Technology & Health research ethics framework (Module LDC6005M protocol).",
         Inches(0.6), Inches(1.8), Inches(5.5), Inches(2.2), C_BLUE),
        ("GDPR DATA PROTECTION BY DESIGN (ART. 25)",
         "Full compliance with GDPR & UK DPA 2018: zero cloud database, zero telemetry harvesting, and local client-side storage isolation within browser IndexedDB.",
         Inches(6.5), Inches(1.8), Inches(5.5), Inches(2.2), C_GREEN),
        ("VOLUNTARY INFORMED CONSENT",
         "All 65 evaluation participants received a Participant Information Sheet (PIS) and provided explicit digital consent with an unconditional right to withdraw.",
         Inches(0.6), Inches(4.3), Inches(5.5), Inches(2.3), C_CYAN),
        ("TOTAL ANONYMITY & ZERO PII",
         "No names, IP addresses, full URL paths, or query tokens were captured. Telemetry strictly logged domain-level hostnames on the user's personal hardware.",
         Inches(6.5), Inches(4.3), Inches(5.5), Inches(2.3), C_NAVY)
    ]
    for title, text, l, t, w, h, acc in cards_eth:
        c = add_card(s17, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=6)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 18: References
    # -------------------------------------------------------------
    print("Building Slide 18: References")
    s18 = prs.slides[17]
    setup_slide_header(s18, "14. Academic References & Cited Works", "REFERENCES")
    clean_placeholder(s18)

    c_r1 = add_card(s18, Inches(0.6), Inches(1.8), Inches(5.6), Inches(4.9))
    tf1 = c_r1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.2)
    tf1.margin_top = Inches(0.2)
    p = tf1.paragraphs[0]
    format_para(p, "HARVARD-STYLE CITATIONS (PART 1)", FONT_HEADING, 11, bold=True, color=C_BLUE, space_after_pt=6)
    
    refs1 = [
        "Bandura, A. (1991) 'Social cognitive theory of self-regulation', Organizational Behavior and Human Decision Processes, 50(2), pp. 248–287.",
        "Bangor, A., Kortum, P.T. and Miller, J.T. (2008) 'An empirical evaluation of the system usability scale', Intl. Journal of Human-Computer Interaction, 24(6), pp. 574–594.",
        "British Computer Society (2022) The BCS Code of Conduct for Information Security and Computing Professionals. Swindon: BCS.",
        "Brooke, J. (1996) 'SUS: A quick and dirty usability scale', in Jordan, P.W. et al. (eds.) Usability Evaluation in Industry. London: Taylor & Francis, pp. 189–194.",
        "European Union (2016) Regulation (EU) 2016/679 (General Data Protection Regulation). Official Journal of the European Union, L 119, pp. 1–88."
    ]
    for r in refs1:
        p = tf1.add_paragraph()
        format_para(p, r, FONT_BODY, 9.5, color=C_NAVY, space_after_pt=6)

    c_r2 = add_card(s18, Inches(6.5), Inches(1.8), Inches(5.6), Inches(4.9))
    tf2 = c_r2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.2)
    tf2.margin_top = Inches(0.2)
    p = tf2.paragraphs[0]
    format_para(p, "HARVARD-STYLE CITATIONS (PART 2)", FONT_HEADING, 11, bold=True, color=C_BLUE, space_after_pt=6)
    
    refs2 = [
        "Google Chrome Developers (2024) Manifest V3 Migration Guide and declarativeNetRequest API Reference. Mountain View: Google LLC.",
        "Hevner, A.R., March, S.T., Park, J. and Ram, S. (2004) 'Design science in information systems research', MIS Quarterly, 28(1), pp. 75–105.",
        "Kaplan, S. (1995) 'The restorative benefits of nature: Toward an integrative framework', Journal of Environmental Psychology, 15(3), pp. 169–182.",
        "Mark, G., Gudith, D. and Klocke, U. (2008) 'The cost of interrupted work: More speed and stress', in Proc. of the SIGCHI Conference on Human Factors in Computing Systems, pp. 107–110.",
        "Zuboff, S. (2019) The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power. New York: PublicAffairs."
    ]
    for r in refs2:
        p = tf2.add_paragraph()
        format_para(p, r, FONT_BODY, 9.5, color=C_NAVY, space_after_pt=6)

    # -------------------------------------------------------------
    # SLIDE 19: Executive Summary
    # -------------------------------------------------------------
    print("Building Slide 19: Executive Summary")
    s19 = prs.slides[18]
    setup_slide_header(s19, "15. Executive Summary & Wrap-Up", "EXECUTIVE SUMMARY")
    clean_placeholder(s19)

    cards_es = [
        ("PROJECT PURPOSE & VALUE PROPOSITION",
         "Delivered TabTime—a lightweight, client-side browser extension empowering students and knowledge workers with millisecond-accurate time awareness, visual analytics, and non-coercive focus interventions with zero cloud dependencies.",
         Inches(0.6), Inches(1.8), Inches(5.5), Inches(2.2), C_BLUE),
        ("DESIGN SCIENCE RESEARCH METHODOLOGY",
         "Followed rigorous DSR principles combining Manifest V3 software engineering, multi-tier testing, ground-truth stopwatch benchmarks (99.85% accuracy), and empirical UAT evaluation across n = 65 participants.",
         Inches(6.5), Inches(1.8), Inches(5.5), Inches(2.2), C_CYAN),
        ("KEY EVALUATION FINDINGS",
         "Achieved a composite SUS score of 89.04/100 (Grade A usability); 95.4% time awareness improvement; 93.8% distraction reduction; ultra-low footprint (14–22 MB RAM, <0.5% CPU).",
         Inches(0.6), Inches(4.3), Inches(5.5), Inches(2.3), C_GREEN),
        ("ACADEMIC & ETHICAL CONTRIBUTIONS",
         "Pioneered a viable zero-cloud, privacy-preserving telemetry model that adheres to BCS ethical standards and proves privacy and powerful analytics can successfully unite.",
         Inches(6.5), Inches(4.3), Inches(5.5), Inches(2.3), C_NAVY)
    ]
    for title, text, l, t, w, h, acc in cards_es:
        c = add_card(s19, l, t, w, h)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        p = tf.paragraphs[0]
        format_para(p, title, FONT_HEADING, 12, bold=True, color=acc, space_after_pt=6)
        p2 = tf.add_paragraph()
        format_para(p2, text, FONT_BODY, 11, color=C_NAVY, space_after_pt=0)

    # -------------------------------------------------------------
    # SLIDE 20: Q&A (Refined layout with clean bottom logos)
    # -------------------------------------------------------------
    print("Building Slide 20: Q&A")
    s20 = prs.slides[19]
    setup_slide_header(s20, "16. Questions & Viva Voce Defense", "Q&A DEFENSE")
    clean_placeholder(s20)

    c_qa = add_card(s20, Inches(1.0), Inches(1.8), Inches(10.6), Inches(4.9), C_WHITE, C_BLUE)
    tf = c_qa.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    format_para(p, "THANK YOU FOR YOUR TIME & ATTENTION", FONT_HEADING, 26, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER, space_after_pt=8)
    
    p = tf.add_paragraph()
    format_para(p, "TAB TIME: A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management", FONT_HEADING, 16, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER, space_after_pt=14)

    p = tf.add_paragraph()
    format_para(p, "The Examination Panel is Respectfully Invited for Questions, Discussion & Technical Defense", FONT_BODY, 14, bold=False, color=C_SLATE, align=PP_ALIGN.CENTER, space_after_pt=20)

    p = tf.add_paragraph()
    format_para(p, "Candidate: [Your Name]  |  Student ID: [Student ID Number]  |  Supervisor: [Supervisor Name]", FONT_HEADING, 12, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER, space_after_pt=4)
    p = tf.add_paragraph()
    format_para(p, "BSc (Hons) Computer Science  |  School of Science, Technology & Health  |  York St John University (London)", FONT_BODY, 11, bold=False, color=C_MUTED, align=PP_ALIGN.CENTER, space_after_pt=0)

    # Logos placed cleanly at the bottom of the card with clear margins
    if os.path.exists(TABTIME_LOGO_PATH):
        s20.shapes.add_picture(TABTIME_LOGO_PATH, Inches(5.8), Inches(5.5), width=Inches(1.0))

    print(f"Saving generated presentation to: {OUTPUT_PPTX}")
    prs.save(OUTPUT_PPTX)
    print("Base presentation generated successfully!")

def apply_animations_and_export():
    print("\nStarting PowerPoint COM Automation to apply animations, transitions, and export slide previews...")
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    abs_pptx = os.path.abspath(OUTPUT_PPTX)
    prs = ppt.Presentations.Open(abs_pptx, False, False, False)
    
    PP_EFFECT_FADE_SMOOTH = 3844
    MSO_ANIM_EFFECT_FADE = 10
    MSO_ANIM_TRIGGER_AFTER_PREVIOUS = 3
    MSO_ANIM_TRIGGER_ON_PAGE_CLICK = 1
    MSO_ANIM_TRIGGER_WITH_PREVIOUS = 2

    total_slides = prs.Slides.Count
    print(f"Applying transitions & animations to {total_slides} slides...")
    
    for i in range(1, total_slides + 1):
        slide = prs.Slides(i)
        
        # 1. Slide Transition (Smooth Fade on all slides)
        slide.SlideShowTransition.EntryEffect = PP_EFFECT_FADE_SMOOTH
        slide.SlideShowTransition.Duration = 0.5
        
        # 2. Shape Animations
        shape_count = slide.Shapes.Count
        if i == 1:
            for s_idx in range(1, min(shape_count + 1, 8)):
                shp = slide.Shapes(s_idx)
                if shp.HasTextFrame and shp.TextFrame.HasText:
                    eff = slide.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, MSO_ANIM_TRIGGER_AFTER_PREVIOUS)
                    eff.Timing.Duration = 0.4
        elif i in [2, 3]:
            for s_idx in range(1, shape_count + 1):
                shp = slide.Shapes(s_idx)
                if shp.HasTable:
                    eff = slide.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, MSO_ANIM_TRIGGER_AFTER_PREVIOUS)
                    eff.Timing.Duration = 0.5
        else:
            # Slides 4-20
            for s_idx in range(1, shape_count + 1):
                shp = slide.Shapes(s_idx)
                if shp.Name == "Title 1" or (shp.HasTextFrame and shp.TextFrame.HasText and s_idx == 1):
                    eff = slide.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, MSO_ANIM_TRIGGER_AFTER_PREVIOUS)
                    eff.Timing.Duration = 0.4
                    break
            
            for s_idx in range(1, shape_count + 1):
                shp = slide.Shapes(s_idx)
                if shp.Name == "Title 1" or shp.Type == 9 or "Connector" in shp.Name or "Straight Connector" in shp.Name:
                    continue
                if shp.Type in [1, 13, 19] or shp.HasTable or shp.HasTextFrame:
                    trigger = MSO_ANIM_TRIGGER_AFTER_PREVIOUS if s_idx <= 3 else MSO_ANIM_TRIGGER_ON_PAGE_CLICK
                    eff = slide.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, trigger)
                    eff.Timing.Duration = 0.4
                    
        # 3. Export Slide as High-Res PNG Image
        preview_img = os.path.join(PREVIEW_DIR, f"slide_{i:02d}.png")
        slide.Export(os.path.abspath(preview_img), "PNG", 1920, 1080)
        print(f"  Slide {i:02d} animated and exported to: {os.path.basename(preview_img)}")

    prs.Save()
    prs.Close()
    ppt.Quit()
    print(f"\nAll slides successfully animated and saved to: {OUTPUT_PPTX}")
    print(f"Slide preview images saved in: {PREVIEW_DIR}")

if __name__ == "__main__":
    build_presentation()
    apply_animations_and_export()
