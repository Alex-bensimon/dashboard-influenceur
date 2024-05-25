import json
from tqdm import tqdm
from collections import Counter

# Charger les données JSON depuis le fichier
with open('data_ytb.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialiser un compteur pour tous les mots-clés
all_keywords = Counter()

# Parcourir les vidéos et collecter les mots-clés
for video in tqdm(data, desc="Traitement des transcriptions"):
    key_words = video.get("keyword", [])
    tags = video.get("snippet", {}).get("tags", [])
    tags = [tag.lower().lstrip('#') for tag in tags]
    keys=[]
    if key_words is None or len(key_words) == 0:
        pass
    else : 
        for tag in tags :
            keys.append(tag)
        all_keywords.update(keys)

# Obtenir les 15 mots les plus fréquents sans doublons
general_key = [word for word, count in all_keywords.most_common(15)]

# Afficher la liste des mots les plus fréquents
print(general_key)
