# Combine all Files from src Folder and act as Project Manager
from src.reader import read_pdf
from src.extractor import extract_observations
from src.thermal_extractor import extract_thermal_findings
from src.ocr_reader import ocr_read_pdf
from src.ddr_generator import (
    generate_summary,
    generate_area_observations,
    generate_root_cause,
    generate_severity,
    generate_recommendations,
    generate_additional_notes,
    generate_missing_info
)
from src.pdf_exporter import create_pdf
# -------- FILE PATHS --------
inspection_path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\inspection_reports\Inspection_2.pdf"
thermal_path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\thermal_reports\Thermal_2.pdf"


# -------- INSPECTION --------
inspection_text = read_pdf(inspection_path)
inspection_obs = extract_observations(inspection_text)


# -------- THERMAL --------
thermal_text = read_pdf(thermal_path)

# if no readable text -> OCR
if len(thermal_text.strip()) < 200:
    print("Using OCR for thermal report...")
    thermal_text = ocr_read_pdf(thermal_path)

thermal_obs = extract_thermal_findings(thermal_text)


# -------- DDR GENERATION --------
summary = generate_summary(inspection_obs, thermal_obs)
area_obs = generate_area_observations(inspection_obs)
root_causes = generate_root_cause(inspection_obs, thermal_obs)
severity, severity_reason = generate_severity(root_causes)
actions = generate_recommendations(root_causes)
notes = generate_additional_notes()
missing = generate_missing_info(inspection_obs, thermal_obs)


# -------- PRINT REPORT --------
print("\n================ DDR REPORT ================\n")

print("1. PROPERTY ISSUE SUMMARY:\n", summary, "\n")

print("2. AREA-WISE OBSERVATIONS:")
for o in area_obs:
    print("-", o)

print("\n3. PROBABLE ROOT CAUSE:")
for r in root_causes:
    print("-", r[0], ":", r[1])

print("\n4. SEVERITY ASSESSMENT:")
print("Severity Level:", severity)
print("Reason:", severity_reason)

print("\n5. RECOMMENDED ACTIONS:")
for a in actions:
    print("-", a)

print("\n6. ADDITIONAL NOTES:")
for n in notes:
    print("-", n)

print("\n7. MISSING OR UNCLEAR INFORMATION:")
for m in missing:
    print("-", m)

# -------- EXPORT TO PDF --------
create_pdf(
    summary,
    area_obs,
    root_causes,
    severity,
    severity_reason,
    actions,
    notes,
    missing
)