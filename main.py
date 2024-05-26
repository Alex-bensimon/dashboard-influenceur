#How to Bitcoin channel id: UCjlxqqxeG5HtvKR5zX88Y1w
#ProLearning channel id : UCHYjRLGdr85gxGfRwC8G-Gw

from data_processing.youtube import YouTubeProcessor

def main():
    # Channel ID et chemin vers le fichier JSON correspondant
    channel_id = input("Taper l'ID de la chaine youtube : ")
    chemin_complet = f"database/{channel_id}.json"

    # Création de l'instance YouTubeProcessor (class dans le fichier youtube.py qui récupère les informations et les trasncriptions)
    youtube_processor = YouTubeProcessor(api_key='...')  # Remplacez 'YOUR_API_KEY' par votre clé API
    #Lancement de l'instance pour la mise à jour du fichier
    youtube_processor.update_video_list(channel_id, chemin_complet)

if __name__ == '__main__':
    main()
