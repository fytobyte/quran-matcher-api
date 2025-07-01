# quran_matcher_api

# File: api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_quran_data
from matcher import find_matching_ayah, find_fragment_positions, find_best_si_match

app = FastAPI()

# Enable CORS for all origins (Adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

quran_data = load_quran_data('quran_dataset.json')

@app.post("/match")
async def match_fragment(request: Request):
    data = await request.json()
    arabic_fragment = data.get("fragment")

    if not arabic_fragment:
        return {"error": "No fragment provided."}

    matched_ayah, confidence = find_matching_ayah(arabic_fragment, quran_data)

    if matched_ayah:
        start_idx, end_idx = find_fragment_positions(arabic_fragment, matched_ayah)
        if start_idx is not None:
            literal_english = ' '.join([
                matched_ayah['words'][i]['english'] for i in range(start_idx, end_idx + 1)
            ])

            best_si_segment, match_score = find_best_si_match(literal_english, matched_ayah['sahih_international'])

            return {
                "arabic_fragment": arabic_fragment,
                "matched_ayah": matched_ayah['arabic'],
                "sahih_international": matched_ayah['sahih_international'],
                "literal_english": literal_english,
                "approx_si_segment": best_si_segment,
                "confidence_score": match_score
            }

        return {"error": "Fragment located in Ayah, but word positions not found."}

    return {"error": "No matching Ayah found."}


# To run the server:
# uvicorn api:app --reload
