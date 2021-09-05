## 파일 읽기
# file = open('news.txt', 'r',encoding='UTF8')
# text1 = file.read()
# file.close()
import datetime

import boto3
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from konlpy.tag import Twitter

from briefing_Server.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def word_stt(text):
    text1 = text
    twitter = Twitter()
    words = twitter.nouns(text1)

    print(words)

    # 조사 제거
    words = [n for n in words if len(n) > 1]

    from collections import Counter

    word_count = Counter(words)

    print("zzzzzzzzzz")

    top20 = dict(word_count.most_common(20))

    print("yyyyyyyyyyy")

    wordcloud = WordCloud(
        font_path = '/home/ubuntu/mesh/api/NanumGothic.ttf',
        background_color='white',
        width=1500, height=1000,
        max_font_size=500).generate_from_frequencies(top20)

    print("xxxxxxxxxxxxxx")

    plt.imshow(wordcloud)
    plt.axis('off')
    # plt.show()

    plt.savefig("a.png")

    bucket = boto3.resource('s3')
    print(str(bucket))

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # name = "stt_sample"
    # data_buffer = io.BytesIO(voice_stt)
    print(str(bucket))
    # print(str(voice_stt))
    print("어렵다어렵다 어렵다어렵다")
    #datetime.datetime.now().date()) + str(datetime.datetime.now().hour)
    #print(datetime.datetime.now().date() + str(datetime.datetime.now().hour))
    str_png = str(datetime.datetime.now().date()) + str(datetime.datetime.now().hour) + ".png"
    s3_client.upload_file("a.png", "meshstt", str_png)


    return [str_png, [words[0],words[1],words[2]]]






