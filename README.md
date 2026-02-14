# AI DDR Builder

AI DDR Builder is an Applied AI system that automatically generates a **Detailed Diagnostic Report (DDR)** from building inspection and thermal imaging PDF documents.

## What it does

The system reads two technical reports, extracts defects, correlates visible and hidden issues, determines root cause and severity, and produces a client-friendly report in PDF format.

## Workflow

Inspection PDF + Thermal PDF
→ OCR (for scanned reports)
→ Text Cleaning
→ Observation Extraction (NLP)
→ Thermal Analysis
→ Reasoning Engine
→ Severity Assessment
→ DDR PDF Report

## Technologies

* Python
* spaCy (NLP)
* Tesseract OCR
* PyMuPDF
* pdf2image
* ReportLab

## Dataset

This project does not use a traditional machine learning dataset.
Instead, it works on real-world unstructured documents.

The input consists of two types of PDF files:

Inspection Reports – Contain on-site observations written by engineers such as cracks, leakage, corrosion, electrical issues, and structural defects.

Thermal Imaging Reports – Generated from infrared thermography surveys. These reports identify hidden problems such as insulation failure, air leakage, moisture patterns, thermal bridging, and energy loss.

## Output

The generated DDR includes:

* Property Issue Summary
* Area-wise Observations
* Root Cause Analysis
* Severity Assessment
* Recommended Actions
* Additional Notes

## Run the Project

```bash
python main.py
```

Final report will be saved in:

```
output/reports/DDR_Report.pdf
```
