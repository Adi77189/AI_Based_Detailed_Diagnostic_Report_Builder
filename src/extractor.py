# Find Issues
import spacy
import re
from src.cleaner import clean_text

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

# sentences to ignore
IGNORE_WORDS = [
    "recommend", "arrange", "repair", "should be",
    "must be", "remediation", "timeframe", "priority",
    "category", "recorded", "inspection to be",
    "check properly", "take action"
]

def is_valid_observation(sentence):
    s = sentence.lower()

    # ignore short sentences
    if len(s) < 30:
        return False

    # ignore recommendations
    ignore_words = [
        "stop", "repair", "should", "must", "arrange",
        "recommend", "keep", "check", "provide",
        "take action", "periodic inspection"
    ]
    for word in ignore_words:
        if word in s:
            return False

    # must contain issue keyword
    has_issue = any(k in s for k in ISSUE_KEYWORDS)

    # must contain observation verb (VERY IMPORTANT)
    has_verb = any(v in s for v in OBSERVATION_VERBS)

    return has_issue and has_verb

def refine_sentence(sentence):

    sentence = sentence.strip()
    lower = sentence.lower()

    # issue keywords that should begin the real observation
    core_issues = [
        "leak", "leakage", "crack", "corrosion", "rust",
        "overheat", "hot spot", "moisture", "damp",
        "seepage", "mold", "damage", "fault", "burn",
        "charring", "loose connection", "insulation"
    ]

    # find earliest occurrence of an issue keyword
    start_positions = []

    for word in core_issues:
        pos = lower.find(word)
        if pos != -1:
            start_positions.append(pos)

    # if we found a keyword → cut everything before it
    if start_positions:
        start = min(start_positions)
        sentence = sentence[start:]

    # remove leftover junk characters
    sentence = sentence.lstrip(" :-_.,;")

    # Capitalize first letter
    sentence = sentence[:1].upper() + sentence[1:]

    return sentence

def extract_observations(text):
    text = clean_text(text)
    doc = nlp(text)
    observations = []

    for sent in doc.sents:
        sentence = sent.text.strip()

        if is_valid_observation(sentence):
            cleaned_sentence = refine_sentence(sentence)
            observations.append(cleaned_sentence)

    # remove duplicates
    observations = list(set(observations))

    return observations


if __name__ == "__main__":
    from reader import read_pdf

    file_path = "C:\\Users\\Asus\\Downloads\\ai_ddr_builder\\data\\inspection_reports\\Inspection_2.pdf"
    text = read_pdf(file_path)

    issues = extract_observations(text)

    print("\n======= CLEAN OBSERVATIONS =======\n")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")