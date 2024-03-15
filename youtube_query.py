from googleapiclient.discovery import build


def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey='...')
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    return response

video_id = 'naCO-WK8vsQ'
details = get_video_details(video_id)
print(details)