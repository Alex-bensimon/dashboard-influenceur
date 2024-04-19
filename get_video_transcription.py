from youtube_transcript_api import YouTubeTranscriptApi

video_id = "R-lcz83U0WI"

print(YouTubeTranscriptApi.get_transcript(video_id, languages=['fr']))

