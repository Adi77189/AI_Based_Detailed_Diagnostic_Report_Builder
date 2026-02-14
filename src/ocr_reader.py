#Read Scanned Images
import pytesseract
from pdf2image import convert_from_path

# (usually auto-detected because added to PATH)
# but keep for safety
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_read_pdf(file_path):

    text = ""

    try:
        pages = convert_from_path(file_path)

        for page in pages:
            extracted = pytesseract.image_to_string(page, config="--psm 6")
            text += extracted + "\n"

    except Exception as e:
        print("OCR error:", e)

    return text