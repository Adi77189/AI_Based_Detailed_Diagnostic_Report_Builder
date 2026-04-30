import pytesseract
from pdf2image import convert_from_path
import os

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_read_pdf_with_images(file_path, output_dir="outputs/images/ocr_pages"):
    """
    Reads scanned PDF using OCR and returns structured page-wise data.

    Returns:
    [
        {
            "page_num": int,
            "text": str,
            "image_paths": [str]
        }
    ]
    """

    results = []

    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Convert PDF → images (each page)
        pages = convert_from_path(file_path)

        for i, page in enumerate(pages):
            page_num = i + 1

            # ---- Save page image ----
            image_filename = f"page_{page_num}.png"
            image_path = os.path.join(output_dir, image_filename)

            page.save(image_path, "PNG")

            # ---- OCR extraction ----
            extracted_text = pytesseract.image_to_string(page, config="--psm 6")

            # ---- Store result ----
            results.append({
                "page_num": page_num,
                "text": extracted_text.strip(),
                "image_paths": [image_path] if image_path else ["Image Not Available"]
            })

    except Exception as e:
        print("OCR error:", e)

    return results


# ---------------- TEST ----------------
if __name__ == "__main__":
    sample_path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\inspection_reports\inspection_demo.pdf"

    data = ocr_read_pdf_with_images(sample_path)

    print("\n========= OCR PAGE-WISE DATA =========\n")

    for page in data:
        print(f"\n--- Page {page['page_num']} ---")
        print("Text Preview:", page["text"][:200])
        print("Image:", page["image_paths"])