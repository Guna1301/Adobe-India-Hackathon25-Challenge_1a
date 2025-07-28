#  Adobe India Hackathon 2025 - Challenge 1A

## Problem Statement

Given a set of PDFs, extract a structured outline that includes:

* **Title of the document**
* **Headings (outline)** with accurate `level`, `text`, and `page` info

The goal is to return a JSON structure similar to:

```json
{
  "title": "...",
  "outline": [
    {"level": 1, "text": "Introduction", "page": 1},
    {"level": 2, "text": "Background", "page": 2},
    ...
  ]
}
```

---

##  My Approach

### 1. **Modular Pipeline**

I built a clean modular pipeline with the following key files:

| File                    | Responsibility                                                     |
| ----------------------- | ------------------------------------------------------------------ |
| `pdf_loader.py`         | Loads PDF and extracts raw text + layout                           |
| `heading_extractor.py`  | Detects potential headings based on layout and font heuristics     |
| `heading_classifier.py` | Uses rules or ML to classify which blocks are real headings        |
| `title_detector.py`     | Identifies the main document title                                 |
| `json_writer.py`        | Combines outputs and saves as structured JSON                      |
| `process_pdfs.py`       | Orchestrates the above to process all PDFs                         |
| `check_accuracy.py`     | Compares outputs against ground-truth JSON and calculates accuracy |

---

## 🔍 Techniques Used

* **PyMuPDF (fitz)** for fine-grained layout parsing (bbox, font size, bold)
* **Heuristic heading detection** using font size, bold, and position
* **Rule-based heading classification** (can extend to ML-based in future)
* **Smart title extraction** using first page largest bold text
* **JSON generation** to mimic expected evaluation format
* **Accuracy checker** to verify level-wise and text-wise match

---

## Folder Structure

```
project-root/
├── input/                # Raw PDF files
├── output/               # Generated JSON outputs
├── expectedoutputs/      # Ground truth JSONs
├── check_accuracy.py     # Accuracy evaluation script
├── process_pdfs.py       # Main pipeline entry
├── heading_classifier.py
├── heading_extractor.py
├── title_detector.py
├── json_writer.py
├── pdf_loader.py
├── requirements.txt
├── Dockerfile
└── README.md (you are here)
```

---

## Docker Usage

### Dockerfile:

```dockerfile
FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY process_pdfs.py .
CMD ["python", "process_pdfs.py"]
```

### Steps to Run:

```bash
# 1. Build the Docker image
docker build -t adobe-pdf-parser .

# 2. Run the container
# Make sure to mount your folders if you want access to inputs/outputs
# Example:
docker run --rm -v "$PWD/input:/app/input" -v "$PWD/output:/app/output" adobe-pdf-parser
```

---

## 📈 Accuracy Checking

We use a custom script to compare:

* Title correctness
* Outline structure (level, text, page)

### Command:

```bash
python check_accuracy.py
```

### Output:

Shows file-by-file scores and average overall accuracy.

---

## 🔧 Future Improvements

* Improve title detection with NLP or language models
* Add fuzzy matching to allow partial heading matches
* Switch to a simple lightweight ML model for heading classification
* Streamline Docker to support bulk folders with mounted volumes

---

## Why This Works Well

* Fully modular, easy to extend or modify
* Cleanly separated concerns
* Works inside Docker with limited libraries (PyMuPDF only)
* Fast, accurate, and interpretable

---

## Contribution

Built by **Kotipalli Guna Sai** for Adobe India Hackathon 2025.

Reach out: [LinkedIn](https://www.linkedin.com/in/guna-sai-3673592ba/) | [GitHub](https://github.com/Guna1301)
