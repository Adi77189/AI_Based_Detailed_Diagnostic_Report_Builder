# Craete Final PDF report
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

OUTPUT_PATH = "outputs/reports/DDR_Report1.pdf"


def create_pdf(summary, area_obs, root_causes, severity, severity_reason, actions, notes, missing):

    os.makedirs("output/reports", exist_ok=True)

    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    width, height = A4

    y = height - 50

    def write_line(text, bold=False, gap=14):
        nonlocal y
        if y < 60:
            c.showPage()
            y = height - 50

        if bold:
            c.setFont("Helvetica-Bold", 11)
        else:
            c.setFont("Helvetica", 10)

        c.drawString(50, y, text)
        y -= gap

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, y, "Detailed Diagnostic Report (DDR)")
    y -= 30

    # Section 1
    write_line("1. Property Issue Summary", True)
    write_line(summary)
    y -= 10

    # Section 2
    write_line("2. Area-wise Observations", True)
    for o in area_obs:
        write_line("- " + o)
    y -= 10

    # Section 3
    write_line("3. Probable Root Cause", True)
    for r in root_causes:
        write_line(f"- {r[0]}: {r[1]}")
    y -= 10

    # Section 4
    write_line("4. Severity Assessment", True)
    write_line("Severity Level: " + severity)
    write_line("Reason: " + severity_reason)
    y -= 10

    # Section 5
    write_line("5. Recommended Actions", True)
    for a in actions:
        write_line("- " + a)
    y -= 10

    # Section 6
    write_line("6. Additional Notes", True)
    for n in notes:
        write_line("- " + n)
    y -= 10

    # Section 7
    write_line("7. Missing or Unclear Information", True)
    for m in missing:
        write_line("- " + m)

    c.save()
    print(f"\nPDF Report Generated → {OUTPUT_PATH}")