# File: text_normalizer.py
import re

def normalize_arabic(text):
    diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = diacritics.sub('', text)
    return text.strip()