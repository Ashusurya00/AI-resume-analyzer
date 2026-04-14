"""
Enterprise PDF Report Generator
Produces a branded, multi-section PDF report using ReportLab.
"""

import os
import datetime
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4

# ── Brand Colors ─────────────────────────────────────────────────────────────
C_DARK      = colors.HexColor("#0d0f1a")
C_SURFACE   = colors.HexColor("#131629")
C_BLUE      = colors.HexColor("#5b8af0")
C_GOLD      = colors.HexColor("#f0b429")
C_TEAL      = colors.HexColor("#3dd6c0")
C_ROSE      = colors.HexColor("#f05b7a")
C_TEXT      = colors.HexColor("#1a1a2e")
C_MUTED     = colors.HexColor("#6b7280")
C_BORDER    = colors.HexColor("#e5e7eb")
C_BG_LIGHT  = colors.HexColor("#f8fafc")
C_BG_BLUE   = colors.HexColor("#eff6ff")
C_BG_GREEN  = colors.HexColor("#f0fdf4")
C_BG_RED    = colors.HexColor("#fff1f2")


def _styles():
    base = getSampleStyleSheet()
    custom = {}

    custom["title"] = ParagraphStyle(
        "title", fontSize=24, fontName="Helvetica-Bold",
        textColor=C_TEXT, spaceAfter=4, alignment=TA_LEFT,
        leading=30,
    )
    custom["subtitle"] = ParagraphStyle(
        "subtitle", fontSize=11, fontName="Helvetica",
        textColor=C_MUTED, spaceAfter=16, alignment=TA_LEFT,
    )
    custom["section_header"] = ParagraphStyle(
        "section_header", fontSize=13, fontName="Helvetica-Bold",
        textColor=C_BLUE, spaceBefore=18, spaceAfter=8,
    )
    custom["body"] = ParagraphStyle(
        "body", fontSize=10, fontName="Helvetica",
        textColor=C_TEXT, leading=16, spaceAfter=6,
    )
    custom["bullet"] = ParagraphStyle(
        "bullet", fontSize=10, fontName="Helvetica",
        textColor=C_TEXT, leading=15, leftIndent=16,
        bulletIndent=6, spaceAfter=4,
    )
    custom["label_blue"] = ParagraphStyle(
        "label_blue", fontSize=9, fontName="Helvetica-Bold",
        textColor=C_BLUE,
    )
    custom["label_gold"] = ParagraphStyle(
        "label_gold", fontSize=9, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#b45309"),
    )
    custom["mono"] = ParagraphStyle(
        "mono", fontSize=9, fontName="Courier",
        textColor=colors.HexColor("#374151"), leading=14,
        backColor=colors.HexColor("#f3f4f6"),
    )
    custom["footer"] = ParagraphStyle(
        "footer", fontSize=8, fontName="Helvetica",
        textColor=C_MUTED, alignment=TA_CENTER,
    )
    return custom


def generate_pdf(
    topic: str,
    analysis: dict,
    match_result: dict,
    resume_sections: dict[str, bool],
    output_dir: str = "outputs",
) -> str:
    """Generate a branded PDF report. Returns the file path."""

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in topic)[:40]
    filename = os.path.join(output_dir, f"resume_report_{safe_name}_{ts}.pdf")
    Path(output_dir).mkdir(exist_ok=True)

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch,
    )
    S = _styles()
    story = []

    # ── Cover Header ─────────────────────────────────────────────────────────
    now = datetime.datetime.now().strftime("%B %d, %Y · %H:%M")
    fit  = analysis.get("fit_level", "—")
    ats  = analysis.get("ats_score", 0)
    score = match_result.get("overall_score", 0)

    story.append(Paragraph("NEXUS Resume Intelligence Report", S["title"]))
    story.append(Paragraph(f"Generated: {now}", S["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=C_BLUE, spaceAfter=14))

    # ── Score Summary Table ────────────────────────────────────────────────────
    fit_color = C_TEAL if "Strong" in fit else (C_GOLD if "Moderate" in fit else C_ROSE)
    score_color = C_TEAL if score >= 70 else (C_GOLD if score >= 40 else C_ROSE)
    ats_color   = C_TEAL if ats   >= 70 else (C_GOLD if ats   >= 40 else C_ROSE)

    summary_data = [
        [
            Paragraph("<b>Skill Match</b>", S["body"]),
            Paragraph("<b>ATS Score</b>", S["body"]),
            Paragraph("<b>Job Fit</b>", S["body"]),
        ],
        [
            Paragraph(f"<font color='#{_hex(score_color)}'><b>{score}%</b></font>", ParagraphStyle("x", fontSize=22, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(f"<font color='#{_hex(ats_color)}'><b>{ats}/100</b></font>",  ParagraphStyle("x2", fontSize=22, fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(f"<font color='#{_hex(fit_color)}'><b>{fit}</b></font>",      ParagraphStyle("x3", fontSize=14, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        ],
    ]
    t = Table(summary_data, colWidths=[2.1*inch, 2.1*inch, 2.8*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_BG_LIGHT),
        ("BACKGROUND", (0,1), (-1,1), colors.white),
        ("BOX",        (0,0), (-1,-1), 1, C_BORDER),
        ("INNERGRID",  (0,0), (-1,-1), 0.5, C_BORDER),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # ── Overall Impression ───────────────────────────────────────────────────
    impression = analysis.get("overall_impression", "")
    if impression:
        story.append(Paragraph("Overall Impression", S["section_header"]))
        story.append(Paragraph(impression, S["body"]))

    # ── Resume Sections Detected ─────────────────────────────────────────────
    story.append(Paragraph("Resume Sections Detected", S["section_header"]))
    sec_data = [[
        Paragraph(f"{'✓' if found else '✗'}  {section}",
                  ParagraphStyle("si", fontSize=9, fontName="Helvetica-Bold" if found else "Helvetica",
                                 textColor=C_TEAL if found else C_ROSE))
        for section, found in resume_sections.items()
    ]]
    sec_t = Table(sec_data, colWidths=[1.0*inch]*7)
    sec_t.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOX", (0,0), (-1,-1), 0.5, C_BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.5, C_BORDER),
        ("BACKGROUND", (0,0), (-1,-1), C_BG_LIGHT),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(sec_t)

    # ── Strengths ────────────────────────────────────────────────────────────
    strengths = analysis.get("strengths", [])
    if strengths:
        story.append(Paragraph("✅  Key Strengths", S["section_header"]))
        for s in strengths:
            story.append(Paragraph(f"• {s}", S["bullet"]))

    # ── Gaps & Weaknesses ─────────────────────────────────────────────────────
    weaknesses = analysis.get("weaknesses", [])
    if weaknesses:
        story.append(Paragraph("⚠️  Gaps & Weaknesses", S["section_header"]))
        for w in weaknesses:
            story.append(Paragraph(f"• {w}", S["bullet"]))

    # ── Missing Skills ────────────────────────────────────────────────────────
    missing = match_result.get("priority_missing", [])
    if missing:
        story.append(Paragraph("❌  Priority Missing Skills", S["section_header"]))
        skill_text = "  •  ".join(missing)
        story.append(Paragraph(skill_text, S["body"]))

    # ── Matched Skills ────────────────────────────────────────────────────────
    matched = match_result.get("matched_skills", [])
    if matched:
        story.append(Paragraph("✓  Matched Skills", S["section_header"]))
        story.append(Paragraph("  •  ".join(matched), S["body"]))

    # ── Improvement Suggestions ───────────────────────────────────────────────
    suggestions = analysis.get("improvement_suggestions", [])
    if suggestions:
        story.append(Paragraph("💡  Improvement Suggestions", S["section_header"]))
        for i, s in enumerate(suggestions, 1):
            story.append(Paragraph(f"{i}.  {s}", S["bullet"]))

    # ── Bullet Rewrites ───────────────────────────────────────────────────────
    rewrites = analysis.get("bullet_rewrites", [])
    if rewrites:
        story.append(Paragraph("✏️  Suggested Bullet Rewrites", S["section_header"]))
        for rw in rewrites:
            orig = rw.get("original", "")
            impr = rw.get("improved", "")
            if orig and impr:
                story.append(Paragraph(f"<b>Before:</b> {orig}", S["mono"]))
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"<b>After:</b>  {impr}", ParagraphStyle(
                    "mono2", fontSize=9, fontName="Courier",
                    textColor=colors.HexColor("#065f46"),
                    backColor=colors.HexColor("#ecfdf5"), leading=14,
                )))
                story.append(Spacer(1, 10))

    # ── Final Recommendation ──────────────────────────────────────────────────
    rec = analysis.get("final_recommendation", "")
    if rec:
        story.append(Paragraph("📋  Final Recommendation", S["section_header"]))
        story.append(Paragraph(rec, S["body"]))

    # ── Footer ───────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Generated by NEXUS Resume Intelligence Platform · nexus.ai",
        S["footer"],
    ))

    doc.build(story)
    return filename


def _hex(color) -> str:
    """Convert ReportLab color to hex string without '#'."""
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return f"{r:02x}{g:02x}{b:02x}"
