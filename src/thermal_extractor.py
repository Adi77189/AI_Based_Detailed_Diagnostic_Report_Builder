# ---------------- IMPORTS ---------------- #
from src.cleaner import clean_text, normalize_ocr_text
import spacy
from src.ocr_reader import ocr_read_pdf_with_images
from src.reader import read_pdf_with_images


# ---------------- KEYWORDS ---------------- #
THERMAL_KEYWORDS = [
    "hot spot", "overheating", "elevated temperature",
    "thermal anomaly", "abnormal heat", "temperature rise",
    "insulation", "heat loss", "energy loss",
    "air leakage", "cold bridging", "thermal bridging",
    "cold patch", "cold spot", "moisture path",
    "incontinuity", "air infiltration"
]


# ---------------- CLASSIFIER ---------------- #
def classify_thermal_fault(line):
    l = line.lower()

    if "air leakage" in l:
        return "Air Leakage Detected"

    if "insulation incontinuity" in l or "insulation discontinuity" in l:
        return "Insulation Failure Detected"

    if "thermal bridge" in l or "cold bridging" in l:
        return "Thermal Bridging Detected"

    if "energy loss" in l:
        return "Energy Loss Through Openings"

    if "damp" in l or "moisture" in l:
        return "Moisture/Dampness Pattern Detected"

    if "glazing" in l:
        return "Window/Glazing Thermal Inefficiency"

    if "hot spot" in l or "overheating" in l or "temperature rise" in l:
        return "Electrical Hotspot Detected"

    return None


# ---------------- MAIN FUNCTION ---------------- #
def extract_thermal_findings(pages_data):
    """
    Input:
    [
        {
            "page_num": int,
            "text": str,
            "image_paths": list
        }
    ]

    Output:
    [
        {
            "page": int,
            "finding": str,
            "evidence": str,
            "images": list,
            "confidence": float
        }
    ]
    """

    findings = []

    for page in pages_data:
        page_num = page.get("page_num", "Not Available")

        text = clean_text(page.get("text", ""))
        text = normalize_ocr_text(text)

        images = page.get("image_paths", ["Image Not Available"])

        lines = text.split("\n")

        for line in lines:
            s = line.strip()

            if len(s) < 15:
                continue

            # ---- IGNORE METADATA ---- #
            ignore_patterns = [
                "photo date", "file dc_", "ambient temp",
                "camera", "software", "survey accordance",
                "client", "inspection data", "weather",
                "wind speed", "certification", "report date",
                "location", "component", "item id", "status",
                "work order", "bs en", "company", "°c"
            ]

            if any(p in s.lower() for p in ignore_patterns):
                continue

            # ---- CLASSIFY ---- #
            fault = classify_thermal_fault(s)

            if fault:
                findings.append({
                    "page": page_num,
                    "finding": fault,
                    "evidence": s,
                    "images": images if images else ["Image Not Available"],
                    "confidence": round(min(1.0, 0.7 + len(s) / 200), 2)
                })

    # ---- DEDUPLICATION ---- #
    unique = {}
    for f in findings:
        key = f["finding"]
        if key not in unique:
            unique[key] = f

    return list(unique.values())


# ---------------- TEST ---------------- #
if __name__ == "__main__":

    from src.reader import read_pdf_with_images
    from src.ocr_reader import ocr_read_pdf_with_images

    path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\thermal_reports\thermal_demo.pdf"

    # ---- Try normal PDF ---- #
    pages = read_pdf_with_images(path)

    # ---- Fallback to OCR ---- #
    total_text = " ".join([p["text"] for p in pages])

    if len(total_text.strip()) < 200:
        print("No readable text → Switching to OCR...")
        pages = ocr_read_pdf_with_images(path)

    thermal_issues = extract_thermal_findings(pages)

    print("\n======= THERMAL FINDINGS =======\n")

    if not thermal_issues:
        print("Not Available")

    for i, t in enumerate(thermal_issues, 1):
        print(f"\n{i}. Page {t['page']}")
        print("   Finding:", t["finding"])
        print("   Evidence:", t["evidence"])
        print("   Images:", t["images"])
        print("   Confidence:", t["confidence"])
