import fitz  # PyMuPDF
import re
import numpy as np
from constants import TITLE_TOP_AREA_PERCENTAGE, MIN_HEADING_LENGTH
from utils import clean_text

# Patterns
date_pattern = re.compile(r"^(0?[1-9]|[12][0-9]|3[01])[\s\-\/](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-\/]\d{2,4}$", re.I)
numbered_pattern = re.compile(r'^\d+(\.\d+)*\s+.+')
toc_dot_leader_pattern = re.compile(r'\.{2,}')

def extract_title(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    blocks = page.get_text("dict")["blocks"]
    candidates = []
    page_height = page.rect.height

    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    y0 = span["bbox"][1]
                    if y0 < page_height * TITLE_TOP_AREA_PERCENTAGE:
                        candidates.append({
                            "text": clean_text(span["text"]),
                            "font_size": span["size"],
                            "y0": y0
                        })

    if candidates:
        candidates.sort(key=lambda x: x["font_size"], reverse=True)
        return candidates[0]["text"]
    else:
        title = doc.metadata.get("title")
        return title if title else "Untitled Document"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    all_font_sizes = []

    # First pass: collect font sizes for median body size calculation
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    all_font_sizes.append(span["size"])

    median_size = np.median(all_font_sizes) if all_font_sizes else 0

    # Second pass: heading detection
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                max_size = 0
                font_name = ""
                for span in line.get("spans", []):
                    text = clean_text(span["text"])
                    if not text:
                        continue
                    line_text += " " + text if line_text else text
                    if span["size"] > max_size:
                        max_size = span["size"]
                        font_name = span["font"]

                if not line_text:
                    continue

                stripped_line = line_text.strip()

                # ➡️ Exclude dates
                if date_pattern.match(stripped_line):
                    continue

                # ➡️ Exclude TOC entries with dot leaders
                if toc_dot_leader_pattern.search(stripped_line):
                    continue

                # ➡️ Numbered heading detection
                if numbered_pattern.match(stripped_line):
                    headings.append({
                        "level": detect_level(stripped_line),
                        "text": stripped_line,
                        "page": page_num
                    })
                    continue

                # ➡️ Colon-ending headings
                if stripped_line.endswith(":"):
                    headings.append({
                        "level": "H1",  # Can refine to H2/H3 if needed
                        "text": stripped_line,
                        "page": page_num
                    })
                    continue

                # ➡️ Heuristic detection: large font or bold font
                if (
                    max_size >= 1.2 * median_size or
                    "bold" in font_name.lower()
                ):
                    if len(stripped_line) < MIN_HEADING_LENGTH:
                        continue
                    headings.append({
                        "level": "H1",
                        "text": stripped_line,
                        "page": page_num
                    })

    return headings

def detect_level(text):
    count_dots = text.count(".")
    if count_dots == 0:
        return "H1"
    elif count_dots == 1:
        return "H2"
    else:
        return "H3"
