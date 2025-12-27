import os
import re
from PyPDF2 import PdfReader
from transformers import pipeline

# =========================
# Load AI Models
# =========================

# Clause simplification
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# English → Urdu translation
translator = pipeline(
    "translation_en_to_ur",
    model="Helsinki-NLP/opus-mt-en-ur"
)

# Agreement type classification (zero-shot)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# =========================
# Read PDF
# =========================
def read_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ PDF file not found in media folder.")

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text.strip()

# =========================
# Legal Document Detection
# =========================
LEGAL_KEYWORDS = {
    "agreement", "whereas", "party", "liability",
    "termination", "arbitration", "jurisdiction",
    "indemnity", "governing law", "confidentiality"
}

def is_legal_document(text, threshold=3):
    text = text.lower()
    score = sum(1 for k in LEGAL_KEYWORDS if k in text)
    return score >= threshold

# =========================
# Agreement Type Detection
# =========================
AGREEMENT_TYPES = [
    "rental agreement",
    "lease agreement",
    "loan agreement",
    "banking agreement",
    "education agreement",
    "student agreement",
    "employment agreement",
    "service agreement",
    "partnership agreement",
    "non-disclosure agreement",
    "sales agreement"
]

def detect_agreement_type(text):
    snippet = text[:2000]  # limit for speed + accuracy

    result = classifier(
        snippet,
        candidate_labels=AGREEMENT_TYPES,
        multi_label=False
    )

    return {
        "type": result["labels"][0],
        "confidence": round(result["scores"][0], 2)
    }

# =========================
# Clause Extraction
# =========================
IMPORTANT_CLAUSES = [
    "termination",
    "liability",
    "indemnity",
    "confidentiality",
    "governing law",
    "arbitration",
    "payment"
]

def extract_clauses(text):
    clauses = {}

    for clause in IMPORTANT_CLAUSES:
        pattern = rf"{clause.upper()}(.+?)(?=\n[A-Z ]{{3,}}|\Z)"
        match = re.search(pattern, text, re.S)

        if match:
            clauses[clause] = match.group(1).strip()

    return clauses

# =========================
# Simplify Clause
# =========================
def simplify_clause(text):
    text = text[:1024]  # safe limit for summarization model

    summary = summarizer(
        text,
        max_length=60,
        min_length=25,
        do_sample=False
    )[0]["summary_text"]

    return summary

# =========================
# Translate to Urdu
# =========================
def translate_to_urdu(text):
    return translator(text)[0]["translation_text"]

# =========================
# Main Processing Pipeline
# =========================
def process_pdf(file_path):
    text = read_pdf(file_path)

    if not is_legal_document(text):
        raise ValueError("❌ This PDF is NOT a legal document.")

    agreement_info = detect_agreement_type(text)
    clauses = extract_clauses(text)

    if not clauses:
        raise ValueError("❌ No important legal clauses found.")

    results = {
        "agreement_type": agreement_info,
        "clauses": {}
    }

    for name, clause_text in clauses.items():
        simple_en = simplify_clause(clause_text)
        simple_ur = translate_to_urdu(simple_en)

        results["clauses"][name] = {
            "easy_english": simple_en,
            "easy_urdu": simple_ur
        }

    return results

# =========================
# Run Script
# =========================
if __name__ == "__main__":
    FILE_PATH = "media/legal_document.pdf"
    # FILE_PATH = "media/non_legal_document.pdf"

    try:
        output = process_pdf(FILE_PATH)

        print("\n✅ LEGAL DOCUMENT ANALYSIS\n")

        print(
            f"Agreement Type: {output['agreement_type']['type'].upper()} "
            f"(confidence: {output['agreement_type']['confidence']})\n"
        )

        for clause, data in output["clauses"].items():
            print(f"--- {clause.upper()} ---")
            print("Easy English:")
            print(data["easy_english"])
            print("\nEasy Urdu:")
            print(data["easy_urdu"])
            print("\n")

    except Exception as e:
        print(e)
