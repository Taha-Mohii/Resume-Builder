from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def generate_pdf(resume: dict, output_path: str = "output/resume.pdf"):
    page_width, page_height = A4
    left_margin = 15*mm
    right_margin = 15*mm
    usable_width = page_width - left_margin - right_margin

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=right_margin,
        leftMargin=left_margin,
        topMargin=12*mm,
        bottomMargin=12*mm
    )

    story = []

    # --- CUSTOM STYLES ---
    name_style = ParagraphStyle("name", fontSize=18, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=8)
    contact_style = ParagraphStyle("contact", fontSize=9, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=6)
    section_style = ParagraphStyle("section", fontSize=11, fontName="Helvetica-Bold", textColor=colors.HexColor("#2E4057"), spaceBefore=8, spaceAfter=3)
    body_style = ParagraphStyle("body", fontSize=9, fontName="Helvetica", spaceAfter=2, leading=13)
    bullet_style = ParagraphStyle("bullet", fontSize=9, fontName="Helvetica", leftIndent=10, spaceAfter=2, leading=13)
    job_title_style = ParagraphStyle("job_title", fontSize=10, fontName="Helvetica-Bold", spaceAfter=1)

    def add_section_title(title):
        story.append(Paragraph(title.upper(), section_style))
        story.append(Table([[""]], colWidths=[usable_width], style=TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.HexColor("#2E4057"))
        ])))
        story.append(Spacer(1, 2*mm))

    # --- HEADER ---
    header = resume["header"]
    story.append(Paragraph(header["name"], name_style))
    contact = f'{header["email"]}  |  {header["phone"]}  |  {header["location"]}'
    story.append(Paragraph(contact, contact_style))
    story.append(Spacer(1, 3*mm))

    # --- SUMMARY ---
    add_section_title("Career Objective")
    story.append(Paragraph(resume["summary"], body_style))
    story.append(Spacer(1, 2*mm))

    # --- SKILLS ---
    add_section_title("Skills")
    skills_text = "  •  ".join(resume["skills"])
    story.append(Paragraph(skills_text, body_style))
    story.append(Spacer(1, 2*mm))

    # --- EXPERIENCE ---
    add_section_title("Experience")
    for exp in resume["experience"]:
        data = [[
            Paragraph(exp["title"], job_title_style),
            Paragraph(exp.get("duration", ""), body_style)
        ]]
        t = Table(data, colWidths=[usable_width * 0.7, usable_width * 0.3])
        t.setStyle(TableStyle([
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t)
        for b in exp["bullets"]:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 2*mm))

    # --- PROJECTS ---
    add_section_title("Projects")
    for proj in resume["projects"]:
        tech = ", ".join(proj.get("tech", []))
        story.append(Paragraph(f'<b>{proj["name"]}</b> — <i>{tech}</i>', body_style))
        for b in proj["bullets"]:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 2*mm))

    # --- EDUCATION ---
    add_section_title("Education")
    for edu in resume["education"]:
        data = [[
            Paragraph(edu["degree"], job_title_style),
            Paragraph(edu["year"], body_style)
        ]]
        t = Table(data, colWidths=[usable_width * 0.7, usable_width * 0.3])
        t.setStyle(TableStyle([
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t)
        story.append(Paragraph(edu["institution"], body_style))
        story.append(Spacer(1, 2*mm))

    doc.build(story)
    print(f"PDF saved to {output_path}")