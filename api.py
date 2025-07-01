from fastapi import FastAPI
from data_loader import load_quran_data
from matcher import find_matching_ayah, find_fragment_positions, find_best_si_match

app = FastAPI()
quran_data = load_quran_data()

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/match")
async def match_fragment(arabic_fragment: str):
    matched_ayah, confidence = find_matching_ayah(arabic_fragment, quran_data)
    if matched_ayah:
        start_idx, end_idx = find_fragment_positions(arabic_fragment, matched_ayah)
        if start_idx is not None:
            literal_english = ' '.join([matched_ayah['words'][i]['english'] for i in range(start_idx, end_idx + 1)])
            best_si_segment, match_score = find_best_si_match(literal_english, matched_ayah['sahih_international'])
            return {
                "arabic_fragment": arabic_fragment,
                "matched_ayah": matched_ayah['arabic'],
                "sahih_international": matched_ayah['sahih_international'],
                "literal_english": literal_english,
                "approximate_si_segment": best_si_segment,
                "confidence": match_score
            }
        else:
            return {"error": "Could not locate fragment positions in Ayah."}
    else:
        return {"error": "No matching Ayah found."}
