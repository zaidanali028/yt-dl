from classes.Yt_Stuff import Yt_Stuff
from classes.Messages import Messages

messages=Messages()
messages.welcome_msg()
yt=Yt_Stuff()
yt.use_cli()
# yt_url='https://www.youtube.com/watch?v=3STiLJgarwU'
# yt=YouTube(yt_url)
# video_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
# for stream in video_audio_streams:
#     print(stream.abr)
# print(video_audio_streams)
