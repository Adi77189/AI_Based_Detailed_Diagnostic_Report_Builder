# AI DDR Builder

AI DDR Builder is an end-to-end Applied AI system that automatically generates a **Detailed Diagnostic Report (DDR)** from building inspection and thermal imaging PDF documents.

The system processes unstructured documents, extracts insights, correlates visible and hidden issues, and produces a **client-ready report with supporting images**.

---

##  What it does

* Reads **Inspection Reports** and **Thermal Imaging Reports**
* Supports:

  *  Digital PDFs
  *  Scanned PDFs (via OCR)
* Extracts **defects and anomalies**
* Correlates **inspection + thermal findings**
* Detects **root causes using reasoning logic**
* Assigns **severity with explanation**
* Embeds **relevant images under observations**
* Generates a **structured DDR PDF**

---

##  Workflow

Inspection PDF + Thermal PDF
→ PDF Reader (PyMuPDF) + OCR (Tesseract)
→ Page-wise Text + Image Extraction
→ Text Cleaning & Normalization
→ Observation Extraction (NLP)
→ Thermal Findings Extraction
→ Reasoning Engine
→ Severity Assessment
→ DDR Generator
→ PDF Exporter (with images)

---

##  Key Features

###  Multi-Modal Processing

* Combines **text + images**
* Maps images to relevant observations

###  OCR Support

* Automatically switches to OCR if PDF text is not readable

### Intelligent Reasoning

* Links inspection issues with thermal anomalies
* Generates **probable root causes**

### Missing Data Handling

* Missing data → **"Not Available"**
* Designed for imperfect real-world documents

###  Structured Output

The DDR includes:

* Property Issue Summary
* Area-wise Observations (with images)
* Root Cause Analysis
* Severity Assessment (with reasoning)
* Recommended Actions
* Additional Notes
* Missing or Unclear Information

---

## Image Handling (Key Requirement)

* Extracts images directly from PDFs
* Places images under corresponding observations
* If no image exists → **"Image Not Available"**
* Supports:

  * Embedded PDF images
  * OCR-generated page images

---

##  Tech Stack

* Python
* spaCy (NLP)
* Tesseract OCR
* PyMuPDF (fitz)
* pdf2image
* ReportLab

---
## Project Structure
```
ai_ddr_builder/
│
├── data/
│ ├── inspection_reports/
│ ├── thermal_reports/
│
├── outputs/
│ ├── images/
│ ├── reports/
│
├── src/
│ ├── reader.py
│ ├── ocr_reader.py
│ ├── extractor.py
│ ├── thermal_extractor.py
│ ├── reasoner.py
│ ├── ddr_generator.py
│ ├── pdf_exporter.py
│
├── main.py
├── requirements.txt
└── README.md
```
---

##  Input Data

###  Inspection Reports

* Cracks, leakage, corrosion, electrical faults
* Written by engineers during site inspection

###  Thermal Reports

* Infrared thermography data
* Detects:

  * Insulation failure
  * Air leakage
  * Moisture patterns
  * Thermal bridging
  * Energy loss

---

##  Output

The generated DDR includes:

* ✔ Property Issue Summary
* ✔ Area-wise Observations (with images)
* ✔ Root Cause Analysis
* ✔ Severity Assessment
* ✔ Recommended Actions
* ✔ Additional Notes
* ✔ Missing Information

---

##  Run the Project

```bash
python main.py
```

---

## Output Location

outputs/reports/DDR_Report.pdf

---

##  Limitations

* Rule-based reasoning (can be improved using LLMs)
* Image-to-observation mapping is heuristic
* Depends on input document quality

---

## Future Improvements

* LLM-based reasoning (GPT integration)
* Web UI (Streamlit / React)
* Better confidence scoring
* Improved document understanding

---

##  Why this Project Stands Out

* Works on **real-world unstructured data**
* Combines **OCR + NLP + reasoning + vision**
* Generates **professional client-ready reports**
* Designed for **scalability and generalization**

---

##  Author

Aditya Singh Bhadauria
