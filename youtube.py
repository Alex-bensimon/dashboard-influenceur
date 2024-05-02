#vérifie si les données de la chaine demandée ont déjé été ingérées, si non crée le fichier ou le met à jour
#fait la liste de toutes les vidéos d'une chaine youtube, récupères ses informations et les stocke dans un fichier json

from googleapiclient.discovery import build # type: ignore
import json
import os
from youtube_transcript_api import YouTubeTranscriptApi

#How to Bitcoin channel id: UCjlxqqxeG5HtvKR5zX88Y1w

channel_id=input("Taper l'ID de la chaine youtube : ")


def file_exist(nom_fichier):
    return os.path.isfile(nom_fichier)

chemin_complet = rf"{channel_id}.json"
nom_complet=channel_id+".json"

def get_video_transcription(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        for transcript in transcript_list:
            # Choisir la transcription française si elle est disponible
            if transcript.language_code == 'fr':
                transcription = transcript.fetch()
                txt=""
                for i in transcription:
                    txt+=(i['text'])
                return txt

        # Si aucune transcription française n'est disponible, choisir l'anglais s'il est disponible
        for transcript in transcript_list:
            if transcript.language_code == 'en':
                transcription = transcript.fetch()
                txt=""
                for i in transcription:
                    txt+=(i['text'])
                return txt

        # Si aucune des deux langues n'est disponible, choisir la langue disponible
        transcription = transcript_list[0].fetch()
        txt=""
        for i in transcription:
            txt+=(i['text'])
        return txt

    except Exception as e:
        print(f"Erreur lors de la récupération de la transcription pour la vidéo {video_id}: {str(e)}")
        return None

def get_video_list(channel_id):
    youtube = build('youtube', 'v3', developerKey='...')

    list_videos = []

    request_playlist = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response_playlist = request_playlist.execute()

    playlist_id = response_playlist['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': 50
    }

    while True:
        request = youtube.playlistItems().list(**params)
        response = request.execute()

        video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
        videos_info = youtube.videos().list(part='snippet', id=','.join(video_ids)).execute()

        for video_info in videos_info['items']:
            video_id = video_info['id']
            video_transcript = get_video_transcription(video_id)
            video_info['transcript'] = video_transcript        
        
        list_videos.extend(videos_info['items'])

        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
        else:
            break

    return list_videos

 
def export_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if file_exist(chemin_complet):
    print(f"Le fichier '{nom_complet}' existe.")
    maj = input("Voulez vous le mettre à jour ? [y/n] ")
    if maj == "y":
        print(f"Patientez pendant la mis à jour. Cela peut prendre quelques instants.")
        list_videos=get_video_list(channel_id)
        export_to_json(list_videos, nom_complet)
        print(f"Le fichier '{nom_complet}' a été mis à jour.")
    
else:
    print(f"Le fichier '{nom_complet}' n'existe pas.\nPatientez pendant sa création. Cela peut prendre quelques instants.")
    list_videos=get_video_list(channel_id)
    export_to_json(list_videos, nom_complet)
    print(f"Le fichier '{nom_complet}' a été créé.")
