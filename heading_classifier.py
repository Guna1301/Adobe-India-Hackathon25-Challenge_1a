def classify_headings(candidates, title_text=None):
    sizes = sorted({b["font_size"] for b in candidates}, reverse=True)
    max_size = sizes[0] if sizes else None
    sizes = sizes[1:]

    level_map = {}
    if len(sizes) >= 1:
        level_map[sizes[0]] = "H1"
    if len(sizes) >= 2:
        level_map[sizes[1]] = "H2"
    if len(sizes) >= 3:
        level_map[sizes[2]] = "H3"
    if len(sizes) >= 4:
        level_map[sizes[3]] = "H4"

    outline = []
    for block in candidates:
        size = block["font_size"]
        text = block["text"].strip()
        page = block["page"]

        # Skip ONLY if it's the title text on the first page
        # if page == 1 and title_text and text.lower() == title_text.strip().lower():
        #     continue

        # Treat max size as H1 if not the title on page 1
        if size == max_size:
            continue
        else:
            level = level_map.get(size)

        if level:
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return outline
