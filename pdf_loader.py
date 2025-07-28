import fitz

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks_data = page.get_text("dict")["blocks"]

        for block in blocks_data:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                max_font_size = 0
                bold = False
                x, y = 0, 0

                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    line_text += text + " "
                    font = span["font"]
                    size = span["size"]

                    if "Bold" in font or "bold" in font:
                        bold = True

                    max_font_size = max(max_font_size, size)
                    x, y = span["origin"]

                line_text = line_text.strip()
                if line_text:
                    blocks.append({
                        "text": line_text,
                        "font_size": round(max_font_size, 2),
                        "bold": bold,
                        "x": round(x, 2),
                        "y": round(y, 2),
                        "page": page_num + 1
                    })

    doc.close()
    return merge_multiline_blocks(blocks)

def merge_multiline_blocks(blocks, y_gap=70, font_tolerance=0.5):
    """
    Merge blocks with similar font, boldness, same page, and vertical proximity (multiline headings)
    """
    blocks.sort(key=lambda b: (b["page"], b["y"]))
    merged = []
    current = None

    for block in blocks:
        if current and block["page"] == current["page"]:
            same_font = abs(block["font_size"] - current["font_size"]) <= font_tolerance
            close_vertically = abs(block["y"] - current["y"]) <= y_gap
            same_bold = block["bold"] == current["bold"]

            if same_font and same_bold and close_vertically:
                current["text"] += " " + block["text"]
                current["y"] = min(current["y"], block["y"])  # topmost y for merged block
                continue
            else:
                merged.append(current)

        current = block

    if current:
        merged.append(current)

    return merged
