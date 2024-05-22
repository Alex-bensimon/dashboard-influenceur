from transformers import pipeline
import json
from tqdm import tqdm
import re
import warnings
warnings.filterwarnings("ignore")

with open('nouveau_fichier.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


extrac = pipeline("token-classification", model="yanekyuk/camembert-keyword-extractor")

try:
    # Pour chaque vidéo
    for video in tqdm(data, desc="Traitement des transcriptions"): 
        # Récupérer la transcription
        transcription = video.get("transcript", []) 
        if isinstance(transcription, list) == True:
            # Concaténer les sous-groupes de transcription s'ils existent
            transcription = ' '.join(transcription)
        # Vérifier si la transcription est vide
        if transcription is None or len(transcription) == 0:
            # Si la transcription est vide, définir le résumé comme None
            video["key"] = None
        else : 
            key_word = set() #pas de doublons
            key_phrase = extrac(transcription)
            for key in key_phrase :
                word = key["word"].lower()
                cleaned_word = re.sub(r'^[^\w]+', '', word)  # enlever les caractères non-alphabétiques au début
                key_word.add(cleaned_word)
            key_word_l = list(key_word)
        # Ajouter les mots clés à la vidéo
        video["keyword"] = key_word_l if key_word_l else None
except Exception as e:
    print("Une erreur s'est produite :", e)

# Enregistrer les données dans un fichier JSON
with open('key_word.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
