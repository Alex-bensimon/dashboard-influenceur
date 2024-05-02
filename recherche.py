from sentence_transformers import SentenceTransformer
import json
from tqdm import tqdm
import sys
import warnings
warnings.filterwarnings("ignore")

# Rediriger le flux de sortie vers la console
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

with open('test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

model = SentenceTransformer("BAAI/bge-m3")

sentence = ["est-ce qu'on peut croire en l'hyperbitcoinisation"]
liste_vid=[]

try:
    # Pour chaque vidéo
    for video in tqdm(data, desc="Traitement des transcriptions"): 
        
        # Récupérer le titre
        title = video.get("snippet", {}).get("localized", {}).get("title", "")
        # Récupérer la transcription
        transcription = video.get("summary", []) 

        if transcription is None or len(transcription) == 0:
            pass
        else :
            
            embeddings_1 = model.encode(sentence)
            embeddings_2 = model.encode(transcription)
            similarity = embeddings_1 @ embeddings_2.T
            if similarity>0.5 :
                liste_vid.append(title)
                liste_vid.append(similarity)
                #print(similarity)
                #print(title)
                #print(transcription)
    print(liste_vid)
except Exception as e:
    print("Une erreur s'est produite :", e)












