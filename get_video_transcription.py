from youtube_transcript_api import YouTubeTranscriptApi

video_id = "R-lcz83U0WI"

#transcript=YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
#transcript_fulltxt = transcript.translate('fr').fetch()
#print(transcript_fulltxt)

srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])

txt=""
for i in srt:
    txt+=(i['text'])
print(txt)