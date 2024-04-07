# affiche les videos d'une chaine youtube passée en paramètres
# affiche les vidéos, réels et anciens lives
# le code en commentaire n'affiche que les vidéos (à vérifier)

from googleapiclient.discovery import build # type: ignore
import json


def get_video_list(channel_id):
    youtube = build('youtube', 'v3', developerKey='...')
    list_videos=[]

    request_playlist = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response_playlist = request_playlist.execute()

    playlist_id = response_playlist['items'][0]['contentDetails']['relatedPlaylists']['uploads']


    #remettre l'autre code ici si necéssaire

    #Récupère vraiment tout (vidéos, réels et lives terminés [même si ils ne sont plus accessibles sans le lien])
    #Les lives sont notés upcoming dans liveBroadcastContent (none pour les videos et les réels), à retirer de la liste par la suite (sur le json ???)
    #A voir si on veut les réels et voir comment différencier un réel d'une vidéo


    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': 50  
    }

    while True:
        request = youtube.playlistItems().list(**params)
        response = request.execute()

        list_videos.extend(response['items'])

        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
        else:
            break  

    print("Vidéos publiées par la chaîne :")
    for video in list_videos:
        title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        print(f"Titre : {title}, ID : {video_id}")

    print(len(list_videos))

channel_id = "UCjlxqqxeG5HtvKR5zX88Y1w"
get_video_list(channel_id)



#Ne récupère pas tout, à vérifier si c'est les réels qui ne sont pas récupérés et si les lives sont récupérés
"""
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'maxResults': 50
    }

    while True:
        request = youtube.search().list(**params)
        response = request.execute()
        list_videos.extend(response['items'])

        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
        else:
            break

    #print("Vidéos publiées par la chaîne :")
    #for video in list_videos:
        #print(video['snippet']['title'])
    print(len(list_videos))


channel_id = "UCK3inMNRNAVUleEbpDU1k2g"
get_video_list(channel_id)

"""




    