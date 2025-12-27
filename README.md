# Legal Document Analyzer (English → Easy English → Urdu)

A Python-based tool that analyzes legal PDF documents, extracts important clauses, simplifies them into easy English, and translates the summaries into Urdu using Hugging Face Transformer models.

---

## ✨ Features

- 📄 Read legal PDF documents
- ⚖️ Detect whether a document is legal in nature
- 🧩 Extract key legal clauses:
  - Termination
  - Liability
  - Confidentiality
  - Governing Law
  - Indemnity
  - Arbitration
  - Payment
- 🧠 Simplify complex legal language into easy English
- 🌐 Translate simplified text into Urdu
- 🔇 Clean CLI output (warnings suppressed)

---

## 🗂 Project Structure

```
.
├── legal_analyzer.py
├── requirements.txt
├── media/
│   └── legal_document.pdf
│   └── non_legal_document.pdf
├── env/                  # virtual environment (not committed)
└── README.md
```

---

## 🛠 Requirements

- Python **3.9 – 3.11**
- Recommended (3.11)
- macOS / Linux / Windows (CPU-only supported)

---

## 📦 Installation

### 1️⃣ Create & activate virtual environment

```bash
python -m venv env
source env/bin/activate   # macOS / Linux
env\Scripts\activate      # Windows
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```txt
numpy==1.26.4
spacy==3.8.0
torch==2.2.2
transformers==4.39.3
sentencepiece
sacremoses
PyPDF2
python-docx
```

---

## ▶️ Usage

1. Place your legal PDF file in the `media/` folder:

```bash
media/legal_document.pdf
```

2. Run the analyzer:

```bash
python legal_analyzer.py
```

---

## ✅ Example Output

```text
✅ LEGAL DOCUMENT SUMMARY

--- TERMINATION ---
Easy English:
Either party may terminate this Agreement by giving thirty (30) days written notice.

Easy Urdu:
کوئی بھی فریق تیس (30) دن کا تحریری نوٹس دے کر اس معاہدے کو ختم کر سکتا ہے۔
```

---

## ⚠️ Notes & Limitations

- PDFs must contain **extractable text** (not scanned images)
- Clause detection relies on keyword and heading patterns
- Urdu translation quality depends on model limitations
- Not a substitute for professional legal advice

---

## 🔇 Suppressed Warnings

The project suppresses:
- Hugging Face `resume_download` deprecation warnings
- Transformer verbosity
- Tokenization suggestions

This ensures clean CLI output.

---

## 🚀 Future Improvements

- Better clause segmentation (spaCy-based)
- Support for scanned PDFs (OCR)
- CLI arguments (`--file`, `--lang`, `--quiet`)
- Web API (FastAPI)
- Additional languages
- Improved Urdu legal translation models

---

## 📜 Disclaimer

This tool is for **educational and informational purposes only**  
and does **not constitute legal advice**.

---

## 🧑‍💻 Author

Built with Python, Hugging Face Transformers, and PyTorch.

---

## 📄 License

MIT License
