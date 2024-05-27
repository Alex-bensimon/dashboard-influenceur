from transformers import pipeline
import json
from tqdm import tqdm
import re
import warnings

warnings.filterwarnings("ignore")

class KeywordExtractor:
    def __init__(self, filename):
        self.filename = filename
        self.extrac = pipeline("token-classification", model="yanekyuk/camembert-keyword-extractor")
    
    def extract_keywords(self):
        # Lecture du fichier JSON contenant les données des vidéos
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Filtrer les vidéos qui n'ont pas encore de mots-clés
        videos_to_update = [video for video in data if not video.get("keyword")]

        # Si aucune vidéo n'a besoin de mise à jour
        if not videos_to_update:
            print("Aucune nouvelle vidéo à traiter pour les mots-clés.")
            return

        try:
            # Traitement des vidéos nécessitant une mise à jour des mots-clés
            for video in tqdm(videos_to_update, desc="Génération des mots clés"):
                # Récupérer la transcription de la vidéo
                transcription = video.get("transcript", [])
                if isinstance(transcription, list):
                    # Concaténer les sous-groupes de transcription s'ils existent
                    transcription = ' '.join(transcription)

                # Si la transcription est vide
                if not transcription:
                    video["keyword"] = None

                else:
                    key_word = set() #Pas de doublons
                    key_phrase = self.extrac(transcription)
                    for key in key_phrase:
                        word = key["word"].lower()
                        cleaned_word = re.sub(r'^[^\w]+', '', word)  # Nettoyage des caractères non-alphabétiques au début
                        key_word.add(cleaned_word)
                    key_word_l = list(key_word)
                    # Ajouter les mots clés à la vidéo
                    video["keyword"] = key_word_l if key_word_l else None

        except Exception as e:
            print("Une erreur s'est produite :", e)

        # Enregistrer les données mises à jour dans le fichier JSON
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
