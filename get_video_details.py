# verifie que l'URL entré en paramètres soit une URL youtube et retourne l'ID de la vidéo
# retourne les détails de la vidéo grâce à l'api youtube et les stocke dans un fichier json
#on peut aussi obtenir les statistiques mais on ne les veux pas ici

from googleapiclient.discovery import build  # type: ignore
import json

def get_video_id(url):
    if 'youtube.com' in url:
        index = url.find('=')
        video_id=url[index+1:]
        return video_id
    else:
        print('URL Youtube non valide')


url="https://www.youtube.com/watch?v=GoAVkSDOXM0"
video_id=get_video_id((url))

def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey='...')
    #request = youtube.videos().list(part='snippet,statistics', id=video_id)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    return response

details = get_video_details(video_id)
#print(details)



def export_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

file_name = 'video_' + video_id + '.json'

export_to_json(details, file_name)

print(f"Details exported to {file_name} file.")
