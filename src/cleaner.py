import re

def clean_text(raw_text):

    text = raw_text

    # join lines
    text = text.replace("\n", " ")

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # remove priority codes like P1, P2
    text = re.sub(r"\bP[0-9]\b", "", text)

    # remove weeks/timeframes
    text = re.sub(r"\b[0-9]+\s*WEEKS?\b", "", text, flags=re.IGNORECASE)

    # remove finding numbers like E-13, E-24
    text = re.sub(r"\b[A-Z]-\s?[0-9]+\b", "", text)

    # remove headings
    headings = [
        "FINDING", "CATEGORY", "REMEDIATION", "PRIORITY",
        "TRANSFORMER ROOM", "DISTRIBUTION BOARD & PANEL"
    ]

    for h in headings:
        text = re.sub(h, "", text, flags=re.IGNORECASE)

    # remove leftover colons
    text = re.sub(r":", "", text)
    # remove electrical ratings like 500 KVA, 230V, 11KV
    text = re.sub(r"\b[0-9]+\s?(kva|kv|v|amp|amps)\b", "", text, flags=re.IGNORECASE)

    return text

def normalize_ocr_text(text):
    """
    Converts messy OCR output into usable line-wise data
    """

    # convert Windows line endings
    text = text.replace("\r", "\n")

    # remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # remove long spaces
    text = re.sub(r"[ \t]+", " ", text)

    # break sentences properly
    text = text.replace(" .", ".\n")
    text = text.replace(" - ", "\n")

    return text