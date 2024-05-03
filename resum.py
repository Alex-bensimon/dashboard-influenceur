import json
import re
from transformers import pipeline
from tqdm import tqdm

# Fonction pour décoder les échappements Unicode
def decode_unicode(text):
    def decode_match(match):
        return chr(int(match.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', decode_match, text)

def group_text(text, group_length=11985):
    groups = []
    for i in range(0, len(text), group_length):
        groups.append(text[i:i+group_length])
    return groups

# Charger le fichier JSON
with open('UCjlxqqxeG5HtvKR5zX88Y1w.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dictionnaire pour stocker les résumés de chaque vidéo
summaries_dict = {}

# Si les données sont stockées dans une liste
if isinstance(data, list):
    summarizer = pipeline("summarization")
        
    # Boucle à travers chaque élément de la liste
for video_data in tqdm(data, desc="Traitement des transcriptions"):
    if 'snippet' in video_data and 'transcript' in video_data:
        snippet = video_data['snippet']
        transcript = video_data['transcript']

        title = snippet.get('title', 'N/A')

            # Générer un résumé uniquement si la transcription est disponible
        if transcript:
                # Diviser le texte en segments plus petits
            segment_length = 512
            segments = [transcript[i:i+segment_length] for i in range(0, len(transcript), segment_length)]

                # Utiliser un modèle de résumé NLP pour générer un résumé pour chaque segment
            summaries = []
            for segment in segments:
                summary = summarizer(segment, max_length=150, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])

                # Combiner les résumés
            combined_summary = ' '.join(summaries)

                # Stocker le résumé dans le dictionnaire
            summaries_dict[title] = combined_summary

# Écrire le dictionnaire dans un fichier JSON
with open('summaries.json', 'w') as outfile:
    json.dump(summaries_dict, outfile, indent=4)

print("Les résumés ont été stockés dans le fichier 'summaries.json'.")