import fitz  
import os


def read_pdf(file_path):
    """
    Basic text extractor (kept for backward compatibility)
    """
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


def read_pdf_with_images(file_path, output_dir="outputs/images"):
    """
    Advanced PDF reader:
    - Extracts text page-by-page
    - Extracts images page-by-page
    - Saves images locally

    Returns:
    [
        {
            "page_num": int,
            "text": str,
            "image_paths": [str, str]
        }
    ]
    """

    results = []

    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        doc = fitz.open(file_path)

        for page_num in range(len(doc)):
            page = doc[page_num]

            # ---- Extract text ----
            page_text = page.get_text()

            # ---- Extract images ----
            image_paths = []
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # Create unique filename
                    image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)

                    # Save image
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)

                    image_paths.append(image_path)

                except Exception as img_error:
                    print(f"Error extracting image on page {page_num + 1}: {img_error}")

            # ---- Append structured result ----
            results.append({
                "page_num": page_num + 1,
                "text": page_text,
                "image_paths": image_paths if image_paths else ["Image Not Available"]
            })

        doc.close()

    except Exception as e:
        print("Error reading PDF with images:", e)

    return results


# ---------------- TEST ----------------
if __name__ == "__main__":
    sample_path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\inspection_reports\Inspection_2.pdf"

    print("\n========= BASIC TEXT =========\n")
    extracted_text = read_pdf(sample_path)
    print(extracted_text[:1000])

    print("\n========= PAGE-WISE DATA =========\n")
    data = read_pdf_with_images(sample_path)

    for page in data:
        print(f"\n--- Page {page['page_num']} ---")
        print("Text Preview:", page["text"][:200])
        print("Images:", page["image_paths"])