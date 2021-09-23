## 파일 읽기
# file = open('news.txt', 'r',encoding='UTF8')
# text1 = file.read()
# file.close()
import datetime

import boto3
import numpy as np
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
        color_func=color_func,
        max_font_size=500).generate_from_frequencies(top20)

    print("xxxxxxxxxxxxxx")


    # plt.color_palette("light:#06F", as_cmap=True)

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


    print(str(bucket))

    print("어렵다어렵다 어렵다어렵다")
    #datetime.datetime.now().date()) + str(datetime.datetime.now().hour)
    #print(datetime.datetime.now().date() + str(datetime.datetime.now().hour))
    str_png = str(datetime.datetime.now().date()) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second) + ".png"
    s3_client.upload_file("a.png", "meshstt", str_png)


    return [str_png, list(top20.keys())[0] + " " + list(top20.keys())[1] + " " + list(top20.keys())[2] + " " + list(top20.keys())[3] + " " + list(top20.keys())[4]]

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return ("hsl({:d},{:d}%, {:d}%)".format(np.random.randint(212, 313), np.random.randint(26, 32),
                                            np.random.randint(45, 80)))





