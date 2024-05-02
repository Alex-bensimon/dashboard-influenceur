import json
import re
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

# Boucler sur chaque vidéo
for video in tqdm(data, desc="Traitement des transcriptions"): 
    # Récupérer la transcription de la vidéo
    transcript = video.get('transcript', [])

    if transcript:
        # Convertir la liste de lignes en une seule chaîne de caractères
        transcript_text = ' '.join([line['text'] for line in transcript])
        
        # Déchiffrer les échappements Unicode dans la transcription
        decoded_transcript = decode_unicode(transcript_text)

        # Si la transcription est plus longue que 11985 caractères, la diviser en groupes
        if len(decoded_transcript) > 11985:
            groups = group_text(decoded_transcript)
            video['transcript'] = groups
        else:
            # Sinon, conserver la transcription telle quelle
            video['transcript'] = decoded_transcript

        
# Enregistrer le fichier modifié avec l'encodage UTF-8
with open('nouveau_fichier.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

