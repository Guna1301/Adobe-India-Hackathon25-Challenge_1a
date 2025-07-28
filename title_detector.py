import re

import re
from datetime import datetime

import re
from datetime import datetime

def looks_like_title(text):
    text = text.strip()

    # Length constraints
    if len(text) < 5 or len(text) > 80:
        return False

    # Filter out unwanted words
    if any(word in text.lower() for word in ["rsvp", "waiver", "visit"]):
        return False

    # URLs or domains
    if re.search(r"\.com|www\.|http", text.lower()):
        return False

    # Address patterns
    if re.match(r"\d{1,5} [A-Za-z ]+|[A-Z]{2} \d{5}", text):
        return False

    # Date patterns (MM/DD/YYYY, YYYY-MM-DD, 01 Jan 2024, etc.)
    date_patterns = [
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",      # 01/01/2024 or 1-1-2024
        r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",        # 2024-01-01
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b",  # Jan 1, 2024
        r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b"     # 01 Jan 2024
    ]

    for pattern in date_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return False

    return True



def detect_title(blocks, page_width=595, page_height=842):
    print("Detecting title...")
    # print(blocks)
    first_page_blocks = [
        b for b in blocks 
        if b["page"] == 1 
        and looks_like_title(b["text"])
        and b["y"] < page_height / 2  
    ]

    if not first_page_blocks:
        return ""

    max_font = max(b["font_size"] for b in first_page_blocks)

    candidates = [b for b in first_page_blocks if b["font_size"] == max_font]

    for block in candidates:
        text = block["text"].strip()
        x = block["x"]
        font_size = block["font_size"]
        text_width = len(text) * font_size * 0.3
        center_of_text = x + text_width / 2
        if abs(center_of_text - page_width / 2) < 100:
            return text

    return candidates[0]["text"].strip()
