# File: matcher.py
from fuzzywuzzy import fuzz
from text_normalizer import normalize_arabic
from difflib import SequenceMatcher


def find_matching_ayah(arabic_fragment, quran_data):
    normalized_fragment = normalize_arabic(arabic_fragment)
    best_match = None
    highest_score = 0

    for ayah in quran_data['ayahs']:
        normalized_ayah = normalize_arabic(ayah['arabic'])
        score = fuzz.partial_ratio(normalized_fragment, normalized_ayah)
        if score > highest_score:
            best_match = ayah
            highest_score = score

    return best_match, highest_score


def find_fragment_positions(arabic_fragment, ayah):
    fragment_words = normalize_arabic(arabic_fragment).split()
    ayah_words = [normalize_arabic(word['arabic']) for word in ayah['words']]

    for i in range(len(ayah_words) - len(fragment_words) + 1):
        if ayah_words[i:i + len(fragment_words)] == fragment_words:
            return i, i + len(fragment_words) - 1

    return None, None


def find_best_si_match(literal_english, si_translation):
    tokens = si_translation.split()
    target = literal_english.split()
    best_match = ""
    highest_ratio = 0

    for i in range(len(tokens) - len(target) + 1):
        window = tokens[i:i + len(target)]
        ratio = SequenceMatcher(None, ' '.join(target), ' '.join(window)).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = ' '.join(window)

    return best_match, highest_ratio


# File: main.py
from data_loader import load_quran_data
from matcher import find_matching_ayah, find_fragment_positions, find_best_si_match

quran_data = load_quran_data()

# Example Input
arabic_fragment = input("Enter Arabic Fragment: ")

matched_ayah, confidence = find_matching_ayah(arabic_fragment, quran_data)

if matched_ayah:
    start_idx, end_idx = find_fragment_positions(arabic_fragment, matched_ayah)
    if start_idx is not None:
        literal_english = ' '.join([matched_ayah['words'][i]['english'] for i in range(start_idx, end_idx + 1)])
        best_si_segment, match_score = find_best_si_match(literal_english, matched_ayah['sahih_international'])

        print(f"\nArabic Fragment: {arabic_fragment}")
        print(f"Matched Ayah: {matched_ayah['arabic']}")
        print(f"Sahih International: {matched_ayah['sahih_international']}")
        print(f"Literal English: {literal_english}")
        print(f"Approximate SI Segment: {best_si_segment} (Confidence: {match_score * 100:.2f}%)")

    else:
        print("\nCould not locate fragment positions in Ayah.")
else:
    print("\nNo matching Ayah found.")
