# File: data_loader.py
import json

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_quran_data():
    quran = load_json('quran.json')
    word_by_word_arabic = load_json('quran_word_by_word_arabic.json')
    word_by_word_english = load_json('english-wbw-translation.json')
    sahih_translation = load_json('en-sahih-international-simple.json')

    compiled_data = []

    for surah in quran:
        surah_id = surah['id']
        for verse in surah['verses']:
            ayah_id = verse['id']
            ayah_key = f"{surah_id}:{ayah_id}"
            
            # Build word-by-word list
            words = []
            word_index = 1
            while f"{ayah_key}:{word_index}" in word_by_word_arabic:
                words.append({
                    'arabic': word_by_word_arabic[f"{ayah_key}:{word_index}"],
                    'english': word_by_word_english[f"{ayah_key}:{word_index}"]
                })
                word_index += 1

            compiled_data.append({
                'surah': surah_id,
                'ayah': ayah_id,
                'arabic': verse['text'],
                'words': words,
                'sahih_international': sahih_translation[ayah_key]['t']
            })

    return {'ayahs': compiled_data}