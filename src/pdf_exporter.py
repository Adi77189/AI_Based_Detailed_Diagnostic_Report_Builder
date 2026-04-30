# ---------------- CREATE FINAL PDF REPORT ---------------- #
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

OUTPUT_PATH = "outputs/reports/DDR_Report.pdf"


def create_pdf(
    summary,
    area_obs,
    root_causes,
    severity,
    severity_reason,
    actions,
    notes,
    missing
):
    # Ensure output directory exists
    os.makedirs("outputs/reports", exist_ok=True)

    c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
    width, height = A4

    y = height - 50

    # ---------- HELPERS ---------- #
    def new_page():
        nonlocal y
        c.showPage()
        y = height - 50

    def write_line(text, bold=False, gap=14):
        nonlocal y

        if y < 60:
            new_page()

        c.setFont("Helvetica-Bold" if bold else "Helvetica", 10)

        # basic wrapping for long lines
        max_chars = 90
        lines = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

        for line in lines:
            if y < 60:
                new_page()
            c.drawString(50, y, line)
            y -= gap

    def draw_image(img_path, img_width=200, img_height=140):
        nonlocal y

        if not os.path.exists(img_path):
            write_line("   Image Not Available")
            return

        try:
            img = ImageReader(img_path)

            # pagination check
            if y - img_height < 60:
                new_page()

            c.drawImage(
                img,
                60,
                y - img_height,
                width=img_width,
                height=img_height
            )

            y -= (img_height + 10)

        except Exception:
            write_line("   Image Not Available")

    # ---------- TITLE ---------- #
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, y, "Detailed Diagnostic Report (DDR)")
    y -= 30

    # ---------- SECTION 1 ---------- #
    write_line("1. Property Issue Summary", True)
    write_line(summary)
    y -= 10

    # ---------- SECTION 2 (UPDATED) ---------- #
    write_line("2. Area-wise Observations", True)

    if not area_obs:
        write_line("Not Available")
    else:
        for obs in area_obs:
            text = obs.get("text", "Not Available")
            images = obs.get("images", [])

            write_line("- " + text)

            if images and images != ["Image Not Available"]:
                for img_path in images:
                    draw_image(img_path)
            else:
                write_line("   Image Not Available")

            y -= 5

    y -= 10

    # ---------- SECTION 3 ---------- #
    write_line("3. Probable Root Cause", True)

    if root_causes and root_causes != ["Not Available"]:
        for r in root_causes:
            if isinstance(r, tuple):
                write_line(f"- {r[0]}: {r[1]}")
            else:
                write_line("- " + str(r))
    else:
        write_line("Not Available")

    y -= 10

    # ---------- SECTION 4 ---------- #
    write_line("4. Severity Assessment", True)
    write_line("Severity Level: " + str(severity))
    write_line("Reason: " + str(severity_reason))
    y -= 10

    # ---------- SECTION 5 ---------- #
    write_line("5. Recommended Actions", True)

    if actions:
        for a in actions:
            write_line("- " + a)
    else:
        write_line("Not Available")

    y -= 10

    # ---------- SECTION 6 ---------- #
    write_line("6. Additional Notes", True)

    for n in notes:
        write_line("- " + n)

    y -= 10

    # ---------- SECTION 7 ---------- #
    write_line("7. Missing or Unclear Information", True)

    for m in missing:
        write_line("- " + m)

    # ---------- SAVE ---------- #
    c.save()

    print(f"\n PDF Report Generated → {OUTPUT_PATH}")