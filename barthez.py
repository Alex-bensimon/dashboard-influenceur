from transformers import pipeline
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

with open('key_word.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


summarizer = pipeline("summarization", model="moussaKam/barthez-orangesum-abstract")

# Longueur maximale autorisée pour le modèle
max_model_length = 500

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
            video["summary"] = None
        else:
            # Diviser la transcription en mots
            words = transcription.split()
            
            # Diviser les mots en segments de taille inférieure ou égale à max_model_length
            segments = []
            i = 0
            while i < len(words):
                current_segment = []
                current_length = 0
                # Ajouter des mots au segment actuel jusqu'à ce que sa longueur atteigne la taille maximale
                while i < len(words) and current_length + len(words[i].split()) < max_model_length:
                    current_segment.append(words[i])
                    current_length += len(words[i].split())
                    i += 1
                # Ajouter le segment actuel à la liste des segments
                segments.append(current_segment)

            # Générer le résumé pour chaque segment de transcription
            summaries = []
            for segment in segments:
                # Convertir le segment de mots en chaîne de caractères
                segment_text = ' '.join(segment)
                
                # Générer le résumé pour le segment avec une longueur maximale réduite
                input_length = len(segment)
                if input_length > 30:
                    max_length = min(70, round(input_length / 2), max_model_length)
                    summary = summarizer(segment_text, max_length=max_length, min_length=0, do_sample=False)
                    summaries.append(summary[0]["summary_text"])

            # Ajouter les résumés à la vidéo
            video["summary"] = ' '.join(summaries) if summaries else None
 
except Exception as e:
    print("Une erreur s'est produite :", e)

# Enregistrer les données résumées dans un fichier JSON
with open('data_ytb.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
