# utils.py

import re

def clean_text(text):
    """
    Cleans the text by:
    - Stripping leading/trailing whitespaces
    - Replacing multiple spaces with single space
    - Ensuring special characters are retained correctly
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text
