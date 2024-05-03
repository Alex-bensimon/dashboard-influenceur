import langchain
import json
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

# Charger les transcriptions depuis le fichier JSON
with open('UCjlxqqxeG5HtvKR5zX88Y1w.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialiser l'API Langchain
langchain.set_api_key("CLE API")

# Longueur maximale autorisée pour le modèle
max_model_length = 512

# Traiter chaque vidéo
for video in tqdm(data, desc="Traitement des transcriptions"):

    # Récupérer la transcription
    transcription = video.get("transcript", [])

    # Vérifier si la transcription est vide
    if transcription is None or len(transcription) == 0:
        # Si la transcription est vide, définir le résumé comme None
        video["summary"] = None
        continue

    # Diviser la transcription en mots
    words = transcription.split()

    # Diviser les mots en segments de taille inférieure ou égale à max_model_length
    segments = []
    i = 0
    while i < len(words):
        current_segment = []
        current_length = 0
        while i < len(words) and current_length + len(words[i].split()) <= max_model_length:
            current_segment.append(words[i])
            current_length += len(words[i].split())
            i += 1
        segments.append(current_segment)

    # Générer le résumé pour chaque segment de transcription
    summaries = []
    for segment in segments:
        # Convertir le segment de mots en chaîne de caractères
        segment_text = ' '.join(segment)

        # Générer le résumé pour le segment avec une longueur maximale réduite
        input_length = len(segment)
        max_length = min(40, round(input_length / 2), max_model_length)
        summary = langchain.summarize(segment_text, max_length=max_length, min_length=0)
        summaries.append(summary[0]["summary_text"])

    # Ajouter les résumés à la vidéo
    video["summary"] = ' '.join(summaries) if summaries else None

# Enregistrer les données résumées dans un fichier JSON
with open('influenceur.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
