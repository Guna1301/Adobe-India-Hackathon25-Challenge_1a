import re

def extract_heading_candidates(blocks, title_text=None):
    print("Extracting heading candidates...")
    if not blocks:
        return []


    blocks.sort(key=lambda b: (b["page"], b["y"]))

    all_sizes = sorted({round(b["font_size"], 2) for b in blocks}, reverse=True)
    top_font_sizes = all_sizes[1:5]

    def looks_like_url(text):
        return "http" in text.lower() or re.search(r"\bwww\.[^\s]+\.\w+", text.lower()) or ".com" in text.lower()

    def looks_like_address(text):
        return bool(re.search(r"\d{2,5} [A-Z ]+", text)) or bool(re.search(r"[A-Z]{2} \d{5}", text))

    def looks_like_disclaimer(text):
        return "(" in text or "waiver" in text.lower() or "required" in text.lower()

    def looks_like_date(text):
        patterns = [
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? \d{4}\b",
            r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*,? \d{4}\b",
            r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
            r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b"
        ]
        return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)

    def is_valid_heading(text):
        if not text or len(text) > 50:
            return False
        if looks_like_url(text):
            return False
        if looks_like_address(text):
            return False
        if looks_like_disclaimer(text):
            return False
        if looks_like_date(text):
            return False
        return True

    candidates = []

    for i, block in enumerate(blocks):
        text = block["text"].strip()
        if not text or len(text.split()) > 12:
            continue

        if title_text and text.strip().lower() == title_text.strip().lower():
            continue

        font_size = round(block["font_size"], 2)
        bold = block["bold"]
        y = block["y"]

        spacing_above = y - blocks[i - 1]["y"] if i > 0 else None
        spacing_below = blocks[i + 1]["y"] - y if i < len(blocks) - 1 else None
        isolated = (spacing_above and spacing_above > 15) and (spacing_below and spacing_below > 15)

        is_large_font = font_size in top_font_sizes
        is_emphasized = bold or text.isupper() or text.istitle()
        is_short = len(text.split()) <= 6
        very_large = font_size >= 26

        if (
            (is_large_font and is_emphasized) or 
            (is_large_font and is_short) or 
            (bold and font_size >= 12 and isolated) or 
            very_large 
        ):
            if is_valid_heading(text):
                candidates.append({
                    **block,
                    "font_size": font_size
                })
    # print(candidates)
    return candidates
