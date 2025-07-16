# main.py

import os
import json
from extractor import extract_title, extract_headings

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        output_path = os.path.join(OUTPUT_DIR, pdf_file.replace(".pdf", ".json"))

        print(f"Processing: {pdf_file}")

        title = extract_title(pdf_path)
        headings = extract_headings(pdf_path)

        result = {
            "title": title,
            "outline": headings
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
