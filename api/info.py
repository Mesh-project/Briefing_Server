import pafy

pafy.set_api_key('AIzaSyDmcbf1nWFgq4dsLVPa1doe12NWLUK5knc')

def video_info(url):
    video_id = url
    v = pafy.new(video_id)
    title = v.title
    author = v.author
    published = v.published
    thumnail = v.thumb
    time = v.duration

    f = dict(title = title, author = author, published = published, thumnail = thumnail, time = time)

    return f