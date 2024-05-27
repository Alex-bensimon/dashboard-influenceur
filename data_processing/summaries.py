from transformers import pipeline
import json
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

class Summarizer:
    def __init__(self, filename):
        self.filename = filename
        self.summarizer = pipeline("summarization", model="moussaKam/barthez-orangesum-abstract")

    def summarize(self):
        # Lecture du fichier JSON contenant les données des vidéos
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Filtrer les vidéos qui n'ont pas encore de résumés
        videos_to_update = [video for video in data if not video.get("summary")]

        # Si aucune vidéo n'a besoin de mise à jour
        if not videos_to_update:
            print("Aucune nouvelle vidéo à traiter pour les résumés.")
            return

        # Longueur maximale autorisée pour le modèle
        max_model_length = 500
        
        # Traitement des vidéos nécessitant une mise à jour des résumés
        for video in tqdm(videos_to_update, desc="Génération des résumés"):
            
            try:
                # Récupérer la transcription de la vidéo
                transcription = video.get("transcript", [])
                if isinstance(transcription, list):
                    # Concaténer les sous-groupes de transcription s'ils existent
                    transcription = ' '.join(transcription)

                # Si la transcription est vide
                if not transcription:
                    video["summary"] = None

                else:
                    # Diviser la transcription en mots
                    words = transcription.split()
                    segments = []
                    i = 0

                    # Diviser les mots en segments de taille inférieure ou égale à max_model_length
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

                    summaries = []
                    # Générer le résumé pour chaque segment de transcription
                    for segment in segments:
                        segment_text = ' '.join(segment)
                        input_length = len(segment)
                        if input_length > 30:
                            max_length = min(70, round(input_length / 2), max_model_length)
                            summary = self.summarizer(segment_text, max_length=max_length, min_length=0, do_sample=False)
                            summaries.append(summary[0]["summary_text"])

                    # Ajouter les résumés à la vidéo
                    video["summary"] = ' '.join(summaries) if summaries else None

            except Exception as e:
                print("Une erreur s'est produite :", e)

        # Enregistrer les données mises à jour dans le fichier JSON
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
