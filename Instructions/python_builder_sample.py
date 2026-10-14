"""
Mconnect Publisher - Academic Courseware, Exam PDF, TTS & Thumbnail Builder
Generates professional course outlines, exam papers, CATs, TTS scripts, and thumbnails matching the Mconnect design system.
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas

# Base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "m_logo.png")
WATERMARK_PATH = os.path.join(ASSETS_DIR, "m_watermark.png")


def ensure_watermark():
    """Ensure faint watermark image exists for PDF drawing."""
    if not os.path.exists(WATERMARK_PATH) and os.path.exists(LOGO_PATH):
        im = Image.open(LOGO_PATH).convert("RGBA")
        alpha = im.split()[3]
        alpha = alpha.point(lambda p: int(p * 0.08))  # 8% opacity
        im.putalpha(alpha)
        im.save(WATERMARK_PATH)


# ---------------------------------------------------------
# Numbered Canvas for Two-Pass Total Page Count & Headers
# ---------------------------------------------------------
class MconnectCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.header_info = {
            "course_header": "COURSE CODE: TITLE",
            "system_sub": "Academic Revision & Courseware Output System",
            "doc_type": "SPECIAL / SUPPLEMENTARY EXAMINATION",
            "footer_left": "Department of Academic Excellence",
            "logo_path": LOGO_PATH,
            "watermark_path": WATERMARK_PATH,
        }

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        page_w, page_h = A4
        margin_x = 36  # 0.5 inch margins
        top_y = page_h - 28
        bot_y = 28

        # 1. Background Watermark (Center of Page)
        wm_path = self.header_info.get("watermark_path")
        if wm_path and os.path.exists(wm_path):
            wm_size = 280
            wm_x = (page_w - wm_size) / 2
            wm_y = (page_h - wm_size) / 2
            self.drawImage(wm_path, wm_x, wm_y, width=wm_size, height=wm_size, mask='auto', preserveAspectRatio=True)

        # 2. Running Header
        logo_path = self.header_info.get("logo_path")
        logo_size = 26
        header_text_x = margin_x
        if logo_path and os.path.exists(logo_path):
            self.drawImage(logo_path, margin_x, top_y - logo_size + 4, width=logo_size, height=logo_size, mask='auto', preserveAspectRatio=True)
            header_text_x = margin_x + logo_size + 8

        # Left Header Titles
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#006633"))
        self.drawString(header_text_x, top_y - 8, self.header_info.get("course_header", ""))

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(header_text_x, top_y - 19, self.header_info.get("system_sub", "Academic Revision & Courseware Output System"))

        # Right Header Tag
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#0f3d24"))
        self.drawRightString(page_w - margin_x, top_y - 12, self.header_info.get("doc_type", "OFFICIAL STUDY MATERIAL"))

        # Separator Line below Header
        self.setStrokeColor(colors.HexColor("#006633"))
        self.setLineWidth(0.75)
        self.line(margin_x, top_y - 25, page_w - margin_x, top_y - 25)

        # 3. Running Footer
        self.setStrokeColor(colors.HexColor("#d1d5db"))
        self.setLineWidth(0.5)
        self.line(margin_x, bot_y + 12, page_w - margin_x, bot_y + 12)

        # Left Footer (Department / Faculty)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6b7280"))
        self.drawString(margin_x, bot_y, self.header_info.get("footer_left", ""))

        # Right Footer (Page X of Y)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - margin_x, bot_y, page_str)


# ---------------------------------------------------------
# 1. Clean PDF Generator
# ---------------------------------------------------------
def generate_mconnect_pdf(data, output_path):
    """Compiles a complete publication-ready PDF according to Mconnect layout."""
    ensure_watermark()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    margin = 36
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=54,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'MconnectTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0a2e1d"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'MconnectSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#374151"),
        spaceAfter=10
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#111827")
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#374151")
    )

    section_heading = ParagraphStyle(
        'MconnectSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#006633"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    question_title = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#006633"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_text = ParagraphStyle(
        'MconnectBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )

    subpart_text = ParagraphStyle(
        'MconnectSubpart',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        leftIndent=14,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(data.get("title", ""), title_style))
    story.append(Paragraph(data.get("subtitle", ""), subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#006633"), spaceAfter=10, spaceBefore=2))

    # Metadata Grid Box
    meta_rows = data.get("meta", [])
    if meta_rows:
        table_data = []
        for row in meta_rows:
            c1_label, c1_val, c2_label, c2_val = row
            table_data.append([
                Paragraph(f"<b>{c1_label}</b> {c1_val}", meta_val),
                Paragraph(f"<b>{c2_label}</b> {c2_val}", meta_val)
            ])

        avail_w = A4[0] - 2 * margin
        col_w = avail_w / 2.0

        t = Table(table_data, colWidths=[col_w, col_w])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 14))

    # Instructions Block (for Exams)
    if data.get("instructions"):
        story.append(Paragraph("Instructions", section_heading))
        story.append(Paragraph(data["instructions"], body_text))
        story.append(Spacer(1, 8))

    # Exam Questions
    questions = data.get("questions", [])
    for idx, q in enumerate(questions):
        q_elements = []
        q_elements.append(Paragraph(q["title"], question_title))
        for part in q.get("parts", []):
            q_elements.append(Paragraph(part, subpart_text))
        q_elements.append(Spacer(1, 18))
        story.append(KeepTogether(q_elements))

    # Notes / Outlines Sections & Tables
    for sec in data.get("sections", []):
        story.append(Paragraph(sec["title"], section_heading))
        if "content" in sec:
            story.append(Paragraph(sec["content"], body_text))
        if "bullets" in sec:
            for b in sec["bullets"]:
                story.append(Paragraph(f"• {b}", subpart_text))
        if "table" in sec:
            t_data = sec["table"]
            avail_w = A4[0] - 2 * margin
            widths = [avail_w * w for w in sec.get("col_ratios", [0.35, 0.65])]
            formatted_data = []
            for r_idx, r in enumerate(t_data):
                row_cells = []
                for c in r:
                    style = meta_label if r_idx == 0 else body_text
                    row_cells.append(Paragraph(c, style))
                formatted_data.append(row_cells)
            
            t = Table(formatted_data, colWidths=widths)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#006633")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))

    def make_canvas(*args, **kwargs):
        c = MconnectCanvas(*args, **kwargs)
        c.header_info["course_header"] = data.get("course_code", "") + ": " + data.get("title", "").split(":")[-1].strip().upper()
        c.header_info["doc_type"] = data.get("header_tag", "OFFICIAL STUDY MATERIAL")
        c.header_info["footer_left"] = data.get("department", "Academic Revision Series")
        return c

    doc.build(story, canvasmaker=make_canvas)
    print(f"Generated clean PDF: {output_path}")


# ---------------------------------------------------------
# 2. TTS Natural Lecturer Script Generator
# ---------------------------------------------------------
def generate_tts_script(data, output_path):
    """
    Produces a natural, interactive audio lecture script using dynamic
    {firstname} and {nowtime} variables for personalized playback.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    title = data.get("title", "Course Revision")
    course_code = data.get("course_code", "")
    subtitle = data.get("subtitle", "")
    instructions = data.get("instructions", "Answer the required questions.")

    lines = []
    # Opening
    lines.append(f"Good {{nowtime}} {{firstname}}, welcome to this {title} revision session.")
    lines.append("")
    lines.append(f"We are revising the {subtitle}. {instructions} As we move through each question, listen for the small hint that tells you how to organise your answer. A strong academic answer defines key terms, identifies fundamental principles, explains them clearly, and illustrates with concise, relevant examples.")
    lines.append("")

    # If exam questions are present
    questions = data.get("questions", [])
    for q in questions:
        q_title = q.get("title", "")
        parts = q.get("parts", [])
        lines.append(f"{q_title} asks you to address several key components.")
        for p in parts:
            lines.append(f"For {p[:2].upper()}, focus on structuring your arguments logically. Explain the underlying principles, reference relevant authorities or frameworks, and distinguish primary definitions from practical applications.")
        lines.append("")

    # If sections (notes) are present
    sections = data.get("sections", [])
    for sec in sections:
        s_title = sec.get("title", "")
        s_content = sec.get("content", "")
        lines.append(f"Next, let's explore {s_title}.")
        if s_content:
            lines.append(f"Key takeaway for this module: {s_content[:300]}...")
        lines.append("")

    if data.get("custom_tts_text"):
        full_text = data["custom_tts_text"]
    else:
        # Closing exam tip with warm encouragement and wishing luck
        lines.append(f"Alright {{firstname}}, that brings us to the end of our session today—let's wrap it up. Final exam tip, {{firstname}}: always follow the marks. A ten-mark answer requires a clear definition followed by several well-explained analytical points, while a five-mark question requires precision and brevity. Use headings, number your points, and add a short concrete illustration or example where it earns clarity.")
        lines.append("")
        lines.append(f"Take a deep breath, trust the preparation you've put in, and go into your examination with confidence. Wishing you the absolute best of luck in your paper—you've got this! Have a wonderful {{nowtime}}, and keep your reasoning organized.")
        full_text = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Generated TTS script: {output_path}")
    return full_text


# ---------------------------------------------------------
# 3. Thumbnail Card & Image Generation Prompt
# ---------------------------------------------------------
def generate_thumbnail_prompt(data, output_prompt_path):
    """
    Generates a high-impact, modern YouTube-style educational course thumbnail prompt.
    The AI has full creative freedom to specify custom_thumbnail_prompt.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_prompt_path)), exist_ok=True)
    
    if data.get("custom_thumbnail_prompt"):
        prompt = data["custom_thumbnail_prompt"]
        with open(output_prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Generated custom thumbnail prompt: {output_prompt_path}")
        return prompt

    code = data.get("course_code", "CSC 215")
    title = data.get("title", "Course").split(":")[-1].strip()
    tag = data.get("header_tag", "FINAL EXAM")
    school = data.get("school", data.get("department", "School of Science and Aerospace Studies"))

    lower_title = title.lower()
    lower_code = code.lower()

    if any(k in lower_title or k in lower_code for k in ["program", "comput", "software", "csc", "linux", "system"]):
        subject_visual = "an authentic Kali Linux terminal window with root@kali shell commands, process memory buffer overflow diagrams, and C assembly compilation code"
        action_hook = "CRACK THE CODE!"
        subject_highlight = "KALI LINUX LAB!"
        sec_tool = "a secondary computer monitor displaying the Kali Linux desktop with the iconic dragon logo"
    elif any(k in lower_title or k in lower_code for k in ["law", "pss", "crime", "legal"]):
        subject_visual = "an interactive legal case analysis board displaying Actus Reus and Mens Rea diagrams, penal code citations, and Supreme Court precedent flowcharts"
        action_hook = "CRACK THE CASE!"
        subject_highlight = "COURTROOM PRECEDENT REVIEW!"
        sec_tool = "a secondary desktop screen displaying digital evidence transcripts and scales of justice emblem"
    elif any(k in lower_title or k in lower_code for k in ["math", "calculus", "mat", "algebra", "stat"]):
        subject_visual = "glowing 3D mathematical coordinate plots, calculus derivatives, Taylor series proofs, and matrix transformations"
        action_hook = "MASTER THE FORMULAS!"
        subject_highlight = "FINAL EXAM CRUNCH!"
        sec_tool = "a secondary screen showing dynamic mathematical simulation software"
    elif any(k in lower_title or k in lower_code for k in ["social", "swk", "psych", "health"]):
        subject_visual = "an interactive clinical counseling flowchart with family systems genograms and assessment models"
        action_hook = "CRACK THE CASE STUDY!"
        subject_highlight = "CLINICAL PRACTICE LAB!"
        sec_tool = "a secondary screen showing counseling session diagnostic notes"
    else:
        subject_visual = "an interactive high-tech academic diagram with modular concept maps and key revision frameworks"
        action_hook = "ACE YOUR EXAM!"
        subject_highlight = "COMPREHENSIVE MASTERCLASS!"
        sec_tool = "a secondary screen showing digital courseware notes and learning metrics"

    prompt = (
        f"A punchy, cinematic, modern YouTube educational course thumbnail in 16:9 aspect ratio for university course '{code}: {title} - {tag}'. "
        f"Foreground features an energetic, professional university lecturer with a headset microphone, passionately teaching and gesturing with a digital stylus toward a giant glowing smartboard. "
        f"The smartboard clearly displays authentic {subject_visual}. "
        f"In the background, a modern university computer lab and lecture hall with attentive undergraduate students working on laptops. {sec_tool}. "
        f"Top-left corner features a crisp university school badge for '{school}' with '{code}'. "
        f"Top-right corner features bold, high-contrast YouTube-style typography with drop shadow: "
        f"\"{title.upper()} EXAM!\" in large white bold letters, "
        f"\"{action_hook}\" in bold condensed white, and "
        f"\"{subject_highlight}\" in vibrant neon electric yellow, followed by \"TUTORIAL & COMPLETE REVIEW\". "
        f"Cinematic indoor studio lighting, teal and dark blue ambient glow, sharp depth of field, photorealistic, 8k resolution, ultra-detailed render."
    )

    with open(output_prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Generated thumbnail prompt: {output_prompt_path}")
    return prompt


def generate_thumbnail_image(data, output_img_path):
    """
    Renders an elegant, high-resolution 16:9 banner/thumbnail card using PIL
    so a publication image is immediately ready on disk.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_img_path)), exist_ok=True)
    width, height = 1280, 720
    im = Image.new("RGBA", (width, height), (10, 40, 24, 255))
    draw = ImageDraw.Draw(im)

    # Draw stylish gradient-like emerald background circles
    draw.ellipse([(-100, -100), (600, 600)], fill=(0, 102, 51, 80))
    draw.ellipse([(700, 200), (1400, 900)], fill=(0, 120, 60, 60))
    draw.rounded_rectangle([(40, 40), (width - 40, height - 40)], radius=24, outline=(0, 150, 75, 180), width=3)

    # Paste Logo if available
    if os.path.exists(LOGO_PATH):
        logo_im = Image.open(LOGO_PATH).convert("RGBA").resize((130, 130), Image.Resampling.LANCZOS)
        im.paste(logo_im, (80, 80), mask=logo_im)

    # Text headers
    code = data.get("course_code", "PSS 314")
    title = data.get("title", "").split(":")[-1].strip()
    subtitle = data.get("subtitle", "")
    header_tag = data.get("header_tag", "SPECIAL EXAMINATION")

    # Try standard system fonts or default
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 68)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 26)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_large = font_title = font_sub = font_badge = ImageFont.load_default()

    # Brand badge
    draw.rounded_rectangle([(230, 95), (580, 140)], radius=12, fill=(0, 102, 51, 220))
    draw.text((250, 105), "MCONNECT COURSEWARE", fill=(220, 255, 220, 255), font=font_badge)

    # Course Code
    draw.text((80, 240), code, fill=(52, 211, 153, 255), font=font_large)

    # Course Title
    draw.text((80, 330), title, fill=(255, 255, 255, 255), font=font_title)

    # Subtitle / Session
    draw.text((80, 410), subtitle, fill=(209, 213, 219, 255), font=font_sub)

    # Bottom Tag Badge
    draw.rounded_rectangle([(80, 560), (480, 620)], radius=16, fill=(0, 102, 51, 255), outline=(52, 211, 153, 255), width=2)
    draw.text((110, 578), f"• {header_tag} •", fill=(255, 255, 255, 255), font=font_sub)

    # Save image as RGB JPEG / PNG
    rgb_im = im.convert("RGB")
    rgb_im.save(output_img_path, quality=95)
    print(f"Generated thumbnail image: {output_img_path}")


# ---------------------------------------------------------
# Default Reference Sample Data (PSS 314)
# ---------------------------------------------------------
PSS314_SAMPLE = {
    "doc_type": "exam",
    "header_tag": "SPECIAL / SUPPLEMENTARY EXAMINATION",
    "course_code": "PSS314",
    "title": "Criminal Law",
    "descriptor": "Special_Supplementary_Examination_March_2024",
    "subtitle": "Special / Supplementary Examination - March 2024",
    "department": "Department of History, Political Science & Public Administration",
    "meta": [
        ("Department:", "History, Political Science & Public Administration", "Course Code:", "PSS 314"),
        ("Examination:", "Special / Supplementary", "Exam Date:", "March 2024"),
        ("School / Faculty:", "School of Arts and Social Sciences (SASS)", "Academic Year:", "Not specified"),
        ("Semester:", "Not specified", "Time Allowed:", "Not specified")
    ],
    "instructions": "Answer Question One and any other three questions.",
    "questions": [
        {
            "title": "Question 1 (25 Marks)",
            "parts": [
                "a) Define criminal law and give the distinctions between criminal law and civil law. (10 marks)",
                "b) Explain the various purposes of criminal law. (10 marks)",
                "c) What are the parties to a criminal offence? (5 marks)"
            ]
        },
        {
            "title": "Question 2 (15 Marks)",
            "parts": [
                "a) State and briefly explain the various sources of criminal law. (10 marks)",
                "b) Discuss the essential elements of a crime. (5 marks)"
            ]
        },
        {
            "title": "Question 3 (15 Marks)",
            "parts": [
                "a) Explain the defences in criminal responsibility. (10 marks)",
                "b) Define murder and explain the categories of murder. (5 marks)"
            ]
        },
        {
            "title": "Question 4 (15 Marks)",
            "parts": [
                "a) Define suicide and discuss the types of suicide. (5 marks)",
                "b) Define assault and explain the various types of assault. (10 marks)"
            ]
        },
        {
            "title": "Question 5 (15 Marks)",
            "parts": [
                "a) Define stalking and indicate the circumstances that amount to stalking. (5 marks)",
                "b) State and briefly explain the various typologies of stalkers. (10 marks)"
            ]
        },
        {
            "title": "Question 6 (15 Marks)",
            "parts": [
                "a) Explain the motivation of cyber stalkers. (10 marks)",
                "b) Explain the various ways in which one can prevent cyber stalking. (5 marks)"
            ]
        },
        {
            "title": "Question 7 (15 Marks)",
            "parts": [
                "a) Define rape and briefly discuss the forms of rape. (10 marks)",
                "b) Briefly discuss the criminalisation process in Kenya. (5 marks)"
            ]
        }
    ]
}


# Load rich benchmark lecture text from samples/P0048_text.txt if available
p0048_file = os.path.join(SCRIPT_DIR, "samples", "P0048_text.txt")
if os.path.exists(p0048_file):
    with open(p0048_file, "r", encoding="utf-8") as f:
        base_tts = f.read().strip()
    # Add real human lecturer wrap up and wishing good luck
    lecture_wrap = (
        "\n\nAlright {firstname}, that brings us to the end of our Criminal Law revision session today—let's wrap it up. "
        "Take a deep breath, review your notes on these principles, and trust the preparation you've put in. "
        "Wishing you the absolute best of luck in your upcoming examination—you've got this! "
        "Have a wonderful {nowtime}, and keep your legal reasoning sharp and organized."
    )
    PSS314_SAMPLE["custom_tts_text"] = base_tts + lecture_wrap


def clear_input_folder(input_dir=None):
    """Removes all processed files from Input folder (Rule 11)."""
    if input_dir is None:
        input_dir = os.path.join(PROJECT_DIR, "Input")
    if os.path.exists(input_dir):
        cleared_count = 0
        for fname in os.listdir(input_dir):
            fpath = os.path.join(input_dir, fname)
            try:
                if os.path.isfile(fpath) or os.path.islink(fpath):
                    os.unlink(fpath)
                    cleared_count += 1
                elif os.path.isdir(fpath):
                    import shutil
                    shutil.rmtree(fpath)
                    cleared_count += 1
            except Exception as e:
                print(f"  [WARN] Could not remove {fpath}: {e}")
        print(f"[PURGE] Cleared {cleared_count} file(s) from Input/ directory.")


def search_materials(query, doc_type=None, api_base=None):
    """Queries backend for matching materials (Rule 11.2)."""
    import requests
    if api_base is None:
        api_base = os.environ.get("MCONNECT_API_URL", "http://localhost:5000")
    url = f"{api_base}/api/v1/materials/search"
    params = {"q": query, "status": "approved", "limit": 10, "page": 1}
    if doc_type:
        params["type"] = doc_type
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"  [API] Search returned status {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        print(f"  [API] Backend unreachable at {api_base}: {e}")
        return None


def publish_material(data, pdf_path, thumbnail_path=None, tts_path=None, api_base=None):
    """Publishes deliverables directly via POST /api/v1/dashboard/materials/publish (Rule 11)."""
    import requests
    if api_base is None:
        api_base = os.environ.get("MCONNECT_API_URL", "http://localhost:5000")
    url = f"{api_base}/api/v1/dashboard/materials/publish"

    doc_type = data.get("doc_type", "past_paper")
    type_map = {
        "exam": "past_paper",
        "past_paper": "past_paper",
        "cat": "cat",
        "notes": "notes",
        "revision": "revision",
        "course_outline": "notes"
    }
    mapped_type = type_map.get(doc_type.lower(), "past_paper")

    exam_year = 2024
    for word in (data.get("subtitle", "") + " " + data.get("descriptor", "")).split():
        if word.isdigit() and len(word) == 4:
            exam_year = int(word)
            break

    payload = {
        "title": data.get("title", "Academic Material"),
        "type": mapped_type,
        "school": data.get("school", data.get("department", "School of Arts and Social Sciences")),
        "department": data.get("department", "Academic Department"),
        "unitCode": data.get("course_code", "GEN101"),
        "unitName": data.get("title", "").split(":")[-1].strip(),
        "courseCode": data.get("course_code", "GEN101"),
        "academicYear": data.get("academic_year", f"{exam_year}/{exam_year+1}"),
        "semester": data.get("semester", "Semester 1"),
        "examYear": exam_year,
        "description": f"Official {mapped_type} for {data.get('course_code')} {data.get('title')}"
    }

    files = {}
    opened_files = []
    try:
        if os.path.exists(pdf_path):
            f_pdf = open(pdf_path, "rb")
            opened_files.append(f_pdf)
            files["file"] = f_pdf

        if thumbnail_path and os.path.exists(thumbnail_path):
            f_thumb = open(thumbnail_path, "rb")
            opened_files.append(f_thumb)
            files["thumbnail"] = f_thumb

        if tts_path and os.path.exists(tts_path):
            f_tts = open(tts_path, "rb")
            opened_files.append(f_tts)
            files["ttsFile"] = f_tts

        print(f"\n[PUBLISH] Attempting upload to: {url}")
        print(f"  • Title: {payload['title']} | Type: {payload['type']} | Code: {payload['unitCode']}")

        response = requests.post(url, data=payload, files=files, timeout=10)
        if response.status_code in (200, 201):
            res_json = response.json()
            mtid = res_json.get("mtid") or res_json.get("data", {}).get("mtid", "Assigned")
            print(f"[PUBLISH SUCCESS] Material published! MTID: {mtid}")
            return res_json
        else:
            print(f"[PUBLISH FAILED] HTTP {response.status_code}: {response.text[:300]}")
            return None
    except Exception as e:
        print(f"[PUBLISH OFFLINE] Could not connect to {url}: {e}")
        print("  (Deliverables are safely stored in Output/ for future sync)")
        return None
    finally:
        for f in opened_files:
            try:
                f.close()
            except Exception:
                pass


PROGRESS_FILE = os.path.join(PROJECT_DIR, "cloudesoft-exams_progress.txt")


def update_progress_file(course_code, progress_path=None):
    """
    Appends course_code to cloudesoft-exams_progress.txt following 
    the 10-items-per-page rule (Rule 13).
    """
    if progress_path is None:
        progress_path = PROGRESS_FILE

    code_clean = course_code.strip()
    if not os.path.exists(progress_path):
        with open(progress_path, "w", encoding="utf-8") as f:
            f.write(f"Page 1\n\t{code_clean}\n")
        print(f"[PROGRESS] Initialized {progress_path} with Page 1: {code_clean}")
        return

    with open(progress_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    pages = []
    current_page = None
    current_items = []

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("page "):
            if current_page is not None:
                pages.append((current_page, current_items))
            current_page = stripped
            current_items = []
        elif stripped:
            current_items.append(stripped)

    if current_page is not None:
        pages.append((current_page, current_items))

    if not pages:
        pages.append(("Page 1", []))

    last_page_title, last_page_items = pages[-1]

    # Check if already in active page
    if code_clean in last_page_items:
        print(f"[PROGRESS] {code_clean} is already present in {last_page_title}.")
        return

    if len(last_page_items) >= 10:
        try:
            curr_num = int(last_page_title.split()[-1])
            next_page_title = f"Page {curr_num + 1}"
        except Exception:
            next_page_title = f"Page {len(pages) + 1}"
        pages.append((next_page_title, [code_clean]))
        print(f"[PROGRESS] Page full (10 items). Started {next_page_title} with {code_clean}.")
    else:
        last_page_items.append(code_clean)
        pages[-1] = (last_page_title, last_page_items)
        print(f"[PROGRESS] Added {code_clean} to {last_page_title} (Item {len(last_page_items)}/10).")

    out_lines = []
    for p_title, items in pages:
        out_lines.append(p_title)
        for itm in items:
            out_lines.append(f"\t{itm}")
        out_lines.append("")

    result_text = "\n".join(out_lines).strip() + "\n"
    with open(progress_path, "w", encoding="utf-8") as f:
        f.write(result_text)
    print(f"[PROGRESS] Updated {progress_path} successfully.")


def build_all(data=PSS314_SAMPLE, output_dir=None, publish=False, clear_input=False, track_progress=False):
    """
    Generates all 3 deliverables following Rule 2 naming conventions:
    [CourseCode]_[CourseTitle]_[Descriptor].[ext]
    Optionally publishes to API, clears Input folder, and tracks progress.
    """
    if output_dir is None:
        output_dir = os.path.join(PROJECT_DIR, "Output")
    os.makedirs(output_dir, exist_ok=True)

    code = data.get("course_code", "Course").replace(" ", "")
    title = data.get("title", "Subject").split(":")[-1].strip().replace(" ", "_")
    descriptor = data.get("descriptor", "").strip().replace(" ", "_")
    if not descriptor:
        subtitle = data.get("subtitle", "")
        descriptor = "".join([c if c.isalnum() else "_" for c in subtitle]).strip("_")

    base_name = f"{code}_{title}_{descriptor}" if descriptor else f"{code}_{title}"

    pdf_out = os.path.join(output_dir, f"{base_name}.pdf")
    tts_out = os.path.join(output_dir, f"{base_name}_tts.txt")
    img_out = os.path.join(output_dir, f"{base_name}_thumbnail.jpg")
    prompt_out = os.path.join(output_dir, f"{base_name}_thumbnail_prompt.txt")

    generate_mconnect_pdf(data, pdf_out)
    generate_tts_script(data, tts_out)
    generate_thumbnail_prompt(data, prompt_out)
    generate_thumbnail_image(data, img_out)

    print("\n[SUCCESS] Mconnect Publisher generated all 3 deliverables into:", output_dir)
    print(f"  • PDF:       {pdf_out}")
    print(f"  • TTS:       {tts_out}")
    print(f"  • Thumbnail: {img_out}")

    # Optional Publishing (Rule 11)
    if publish:
        pub_result = publish_material(data, pdf_out, img_out, tts_out)
        if pub_result:
            update_progress_file(data.get("course_code", code))

    # Optional Progress Tracking (Rule 13)
    if track_progress and not publish:
        update_progress_file(data.get("course_code", code))

    # Optional Input Purge (Rule 11)
    if clear_input:
        clear_input_folder()


if __name__ == "__main__":
    ensure_watermark()
    # Generate reference sample.pdf in Instructions directory
    sample_pdf_path = os.path.join(SCRIPT_DIR, "sample.pdf")
    generate_mconnect_pdf(PSS314_SAMPLE, sample_pdf_path)

    # CLI Flags
    do_publish = "--publish" in sys.argv
    do_clear = "--clear-input" in sys.argv
    do_demo = "--demo" in sys.argv or len(sys.argv) == 1

    if do_demo:
        build_all(PSS314_SAMPLE, publish=do_publish, clear_input=do_clear)
