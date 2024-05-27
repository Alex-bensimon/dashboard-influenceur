#How to Bitcoin channel id: UCjlxqqxeG5HtvKR5zX88Y1w
#ProLearning channel id : UCHYjRLGdr85gxGfRwC8G-Gw

from data_processing.infos_and_transcripts import InfosxTranscripts
from data_processing.keywords import KeywordExtractor
from data_processing.summaries import Summarizer

def main():
    api_key = '...'  # Remplacez par votre clé API
    # Channel ID et chemin vers le fichier JSON correspondant
    channel_id = input("Taper l'ID de la chaine youtube : ")
    chemin_complet = f"database/{channel_id}.json"

    # Étape 1: Récupérer les vidéos et les transcriptions
    youtube_processor = InfosxTranscripts(api_key)
    youtube_processor.update_video_list(channel_id, chemin_complet)

    # Étape 2: Extraire les mots-clés
    keyword_extractor = KeywordExtractor(chemin_complet)
    keyword_extractor.extract_keywords()

    # Étape 3: Résumer les transcriptions
    summarizer = Summarizer(chemin_complet)
    summarizer.summarize()


if __name__ == '__main__':
    main()
