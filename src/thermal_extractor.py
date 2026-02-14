from src.reader import read_pdf
from src.cleaner import clean_text , normalize_ocr_text
import spacy
from src.ocr_reader import ocr_read_pdf

nlp = spacy.load("en_core_web_sm")

THERMAL_KEYWORDS = [
    # electrical thermography
    "hot spot", "overheating", "elevated temperature",
    "thermal anomaly", "abnormal heat", "temperature rise",

    # building thermography
    "insulation", "heat loss", "energy loss",
    "air leakage", "cold bridging", "thermal bridging",
    "cold patch", "cold spot", "moisture path",
    "incontinuity", "air infiltration"
]

THERMAL_VERBS = [
    "detected", "observed", "identified", "recorded", "measured"
]


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

    return None


import re

def extract_thermal_findings(text):

    # clean + normalize OCR
    text = clean_text(text)
    text = normalize_ocr_text(text)

    findings = set()   # set prevents duplicates automatically

    lines = text.split("\n")

    for line in lines:
        s = line.strip()

        if len(s) < 15:
            continue

        # ignore metadata
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

        # classify the fault instead of storing paragraph
        fault = classify_thermal_fault(s)

        if fault:
            findings.add(fault)

    return list(findings)

if __name__ == "__main__":

    path = "C:\\Users\\Asus\\Downloads\\ai_ddr_builder\\data\\thermal_reports\\Thermal_1.pdf"

    text = read_pdf(path)

# if pdf had no text -> use OCR
    if len(text.strip()) < 200:
        print("No readable text found, switching to OCR...")
        text = ocr_read_pdf(path)

    thermal_issues = extract_thermal_findings(text)

    print("\n======= THERMAL FINDINGS =======\n")

    for i, t in enumerate(thermal_issues, 1):
        print(f"{i}. {t}")