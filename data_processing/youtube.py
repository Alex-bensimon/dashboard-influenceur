import os
import json
from tqdm import tqdm
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import re

class YouTubeProcessor:
    def __init__(self, api_key):
        self.api_key = api_key

    def decode_unicode(self, text):
        if text is None:
            return ""
        return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), text)

    def group_text(self, text, group_length=11985):
        groups = []
        for i in range(0, len(text), group_length):
            groups.append(text[i:i+group_length])
        return groups

    def get_video_transcription(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            for transcript in transcript_list:
                # Récupérer la première transcription disponible
                transcription = transcript.fetch()
                txt = "".join(i['text'] for i in transcription)
                # Découper la transcription en segments de textes (décodés)
                if len(txt) > 11985:
                    return self.group_text(self.decode_unicode(txt))
                else:
                    return self.decode_unicode(txt)
                
            # Si aucune transcription n'est disponible
            print(f"Aucune transcription disponible pour la vidéo {video_id}")
            return None
        
        except Exception as e:
            #print(f"Erreur lors de la récupération de la transcription pour la vidéo {video_id}: {str(e)}")
            return None

    def get_video_list_yt(self, channel_id):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
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
                list_videos.append(video_info)

            if 'nextPageToken' in response:
                params['pageToken'] = response['nextPageToken']
            else:
                break
            
        return list_videos

    def get_video_list_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
                return existing_data
        except FileNotFoundError:
            return []

    def add_videos_to_json(self, filename, videos):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(videos, json_file, indent=4, ensure_ascii=False)

    def update_video_list(self, channel_id, filename):
        existing_videos = self.get_video_list_json(filename)
        existing_video_ids = {video['id'] for video in existing_videos}
        new_videos = self.get_video_list_yt(channel_id)
        new_unique_videos = [video for video in new_videos if video['id'] not in existing_video_ids]
        if new_unique_videos:
            for video_info in tqdm(new_unique_videos, desc="Récupération des transcriptions"):
                video_transcript = self.get_video_transcription(video_info['id'])
                video_info['transcript'] = video_transcript
            updated_videos = existing_videos + new_unique_videos
            self.add_videos_to_json(filename, updated_videos)
            print(f"{len(new_unique_videos)} nouvelles vidéos ajoutées au fichier '{filename}'.")
        else:
            print("Aucune nouvelle vidéo trouvée.")

