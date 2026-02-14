# Reads pdf
import fitz  # PyMuPDF
import os

def read_pdf(file_path):
    text = ""

    try:
        doc = fitz.open(file_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()

        doc.close()

    except Exception as e:
        print("Error reading PDF:", e)

    return text


if __name__ == "__main__":
    sample_path = "C:\\Users\\Asus\Downloads\\ai_ddr_builder\\data\\inspection_reports\\Inspection_1.pdf"
    extracted_text = read_pdf(sample_path)

    print("\n========= EXTRACTED TEXT =========\n")
    print(extracted_text[:2000])  # print first 2000 characters only