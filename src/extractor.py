import spacy
from src.cleaner import clean_text
import re

nlp = spacy.load("en_core_web_sm")

ISSUE_KEYWORDS = [
    "crack", "leak", "leakage", "damp", "moisture", "stain",
    "corrosion", "rust", "overheat", "overheating", "hot spot",
    "insulation failure", "damage", "defect", "fault",
    "seepage", "mold", "fungus", "condensation",
    "loose connection", "burn", "charring", "discoloration"
]

OBSERVATION_VERBS = [
    "observed", "detected", "found", "noticed",
    "identified", "present", "visible", "seen"
]


def is_valid_observation(sentence):
    s = sentence.lower()

    if len(s) < 30:
        return False

    ignore_words = [
        "stop", "repair", "should", "must", "arrange",
        "recommend", "keep", "check", "provide",
        "take action", "periodic inspection"
    ]

    if any(word in s for word in ignore_words):
        return False

    has_issue = any(k in s for k in ISSUE_KEYWORDS)
    has_verb = any(v in s for v in OBSERVATION_VERBS)

    return has_issue and has_verb


def refine_sentence(sentence):
    sentence = sentence.strip()
    lower = sentence.lower()

    core_issues = ISSUE_KEYWORDS

    positions = [lower.find(word) for word in core_issues if lower.find(word) != -1]

    if positions:
        sentence = sentence[min(positions):]

    sentence = sentence.lstrip(" :-_.,;")
    sentence = sentence[:1].upper() + sentence[1:]

    return sentence


#  UPDATED FUNCTION
def extract_observations(pages_data):
    """
    pages_data format:
    [
        {
            "page_num": 1,
            "text": "...",
            "image_paths": [...]
        }
    ]
    """

    observations = []

    for page in pages_data:
        page_num = page["page_num"]
        text = clean_text(page["text"])
        images = page["image_paths"]

        doc = nlp(text)

        for sent in doc.sents:
            sentence = sent.text.strip()

            if is_valid_observation(sentence):
                cleaned = refine_sentence(sentence)

                observations.append({
                    "page": page_num,
                    "observation": cleaned,
                    "images": images if images else ["Image Not Available"]
                })

    #  Remove duplicates (based on observation text)
    unique = {}
    for obs in observations:
        key = obs["observation"]
        if key not in unique:
            unique[key] = obs

    return list(unique.values())


# ---------------- TEST ----------------
if __name__ == "__main__":
    from src.reader import read_pdf_with_images

    file_path = r"C:\Users\Asus\Downloads\ai_ddr_builder\data\inspection_reports\inspection_demo.pdf"

    pages = read_pdf_with_images(file_path)
    issues = extract_observations(pages)

    print("\n======= STRUCTURED OBSERVATIONS =======\n")

    for i, issue in enumerate(issues, 1):
        print(f"{i}. Page {issue['page']}")
        print("   Issue:", issue["observation"])
        print("   Images:", issue["images"])