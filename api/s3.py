from pytube import YouTube
# from urllib.request import URLError, HTTPError

def stt_mp4(url):
    print("stt_mp4 함수 입장")
    yt = YouTube(url)
    print("1234123412341234123412341")
    print(str(yt))
    #yt = YouTube('https://www.youtube.com/watch?v=l5Lel9-ldOk')

    voice_file = yt.streams.filter(only_audio=True).first()#.download(output_path='test', filename="hi")
    #print(str(voice_file.default_filename))
    # voice_file.default_filename = 'hi'




    print(type(voice_file))

    #yt = YouTube('https://www.youtube.com/watch?v=l5Lel9-ldOk').streams.first()

    return voice_file