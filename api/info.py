import pafy

pafy.set_api_key('AIzaSyDmcbf1nWFgq4dsLVPa1doe12NWLUK5knc')

def video_info(url):
    video_id = url
    v = pafy.new(video_id)
    title = v.title
    author = v.author
    published = v.published
    thumbnail = v.thumb
    time = v.duration

    print(thumbnail)
    print(author)

    f = dict(user_idx=1, url = url, title = title, thumbnail = thumbnail, author = author, published = published,  video_time = time, topic = "한국 경제 전망이 밝아진 것은 세계 경제 회복 영향이 큰 것으로 풀이된다. "
                  "실제 OECD는 이날 올해 세계 경제성장률 전망치를 종전(42)보다 14포인트나 올려 잡았다. "
                  "OECD는 코로나19 백신 접종 확대와 주요국의 추가 재정 부양책 등으로 세계 경제 성장세가 확대될 것이라고 내다봤다. "
                  "OECD는 미국 성장률 전망치를 종전 32에서 65로 끌어올렸다. "
                  "이른바 백신 효과에 세계 경제 회복 속도가 빨라지리란 전망이 확산되고 있다")

    return f