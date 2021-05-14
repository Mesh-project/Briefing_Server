import pandas
from django.http import HttpResponse
from googleapiclient.discovery import build
import pandas as pd
import re
import html
from konlpy.tag import Okt
from rest_framework.utils import json
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.saving.save import load_model

loaded_model = load_model('best_model.h5')
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

def comment_predict(video_id):
    api_key = 'AIzaSyDmcbf1nWFgq4dsLVPa1doe12NWLUK5knc'
    # video_id = 'V1WHgI2xM2k'

    # 댓글 가져오기
    # 댓글내용, 좋아요수, 작성자, 작성일
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(
                [comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])

            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append(
                        [reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])

        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id,
                                                     pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break

    df = pandas.DataFrame(comments)

    comment = list()

    # html 태그 제거하기
    for row in df[0]:
        cleaner = re.compile('<.*?>')

        cleantext = re.sub(cleaner, '', row)
        cleantext = html.unescape(cleantext)

        only_BMP_pattern = re.compile("["
                                      u"\U00010000-\U0010FFFF"  # BMP characters 이외
                                      "]+", flags=re.UNICODE)

        cleantext = only_BMP_pattern.sub(r'', cleantext)

        comment.append(cleantext)
    df[0] = comment

    # 언어별 분류하기
    def Language(row):
        k_count = 0
        e_count = 0
        etc = 0

        for c in row:
            if ord('가') <= ord(c) <= ord('힣') or ord('ㄱ') <= ord(c) <= ord('ㅎ'):
                k_count += 1
            elif ord('a') <= ord(c.lower()) <= ord('z'):
                e_count += 1
            else:
                etc += 1

        if k_count >= 1:
            sort = "한국어"
            return sort
        elif e_count >= 1:
            sort = "영어"
            return sort
        else:
            sort = "그외"
            return sort

    sort_comment = list()

    # 각 댓글에 대해 수행
    for i in df[0]:
        sort_comment.append(Language(i))

    df['sort'] = sort_comment

    # 한국어인 댓글들만 뽑아오기
    is_korean = df['sort'] == '한국어'
    korean = df[is_korean]

    okt = Okt()

    #데이터 정제
    korean[0].nunique(), korean[1].nunique(), korean['sort'].nunique()
    text = 'do!!! you expect... people~ to~ read~ the FAQ, etc. and actually accept hard~! atheism?@@'
    re.sub(r'[^a-zA-Z ]', '', text)  # 알파벳과 공백을 제외하고 모두 제거

    korean[0] = korean[0].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    korean[0].replace('', pandas.np.nan, inplace=True)
    korean = korean.dropna(how='any')

    X_train = []
    for sentence in korean[0]:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        X_train.append(temp_X)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    threshold = 3
    total_cnt = len(tokenizer.word_index)  # 단어의 수
    rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합
    vocab_size = total_cnt - rare_cnt + 2

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if (value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    X_train = tokenizer.texts_to_sequences(X_train)
    drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
    X_train = pandas.np.delete(X_train, drop_train, axis=0)

    # 리뷰 예측해보기
    predict_list = list()

    print("koren 길이")
    print(len(korean))

    def sentiment_predict(encoded):
        # print(encoded)
        pad_new = pad_sequences(encoded, maxlen=30)  # 패딩
        score = float(loaded_model.predict(pad_new))  # 예측
        if (score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100)) #1
            return predict_list.append("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100)) #0
            return predict_list.append("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))



    print("===============================")
    for i in range(len(X_train)):
        print(i)
        if (i == len(X_train)):
            break
        if(sentiment_predict((X_train[i:i+1])) is not None):
            predict_list.append(sentiment_predict(X_train[i:i + 1]))

    print("///////////////")
    print(len(predict_list))
    korean['predict'] = predict_list


    print("+++++++++++++++++++++++++++++++++++++")
    print(len(korean['predict']))

    # 한국어가 아닌 댓글
    not_korean = df['sort'] != '한국어'
    other_language = df[not_korean]

    js_korean = korean.to_json(orient='index', force_ascii=False)
    js_other = other_language.to_json(orient='index', force_ascii=False)

    comment_array = [korean, other_language]

    print(comment_array)
    return comment_array