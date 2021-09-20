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

def script_predict(sentence):
    X_train = []
    okt = Okt()

    temp_X = []
    print("xxxxxxxxxxx")
    print(sentence)

    temp_X = okt.morphs(sentence, stem=True)  # 토큰화
    print("yyyyyyyyyyyy")
    temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
    X_train.append(temp_X)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    print("555555555")

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

    def sentiment_predict(encoded):
        # print(encoded)
        pad_new = pad_sequences(encoded, maxlen=30)  # 패딩
        score = float(loaded_model.predict(pad_new))  # 예측
        if (score > 0.5):
            # print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100)) #1
            return predict_list.append("{:.2f}% 긍정".format(score * 100))#predict_list.append("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
        else:
            # print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100)) #0
            return predict_list.append("{:.2f}% 부정".format(score * 100))#predict_list.append("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))

    for i in range(len(X_train)):
        print(i)
        if (i == len(X_train)):
            break
        if(sentiment_predict((X_train[i:i+1])) is not None):
            predict_list.append(sentiment_predict(X_train[i:i + 1]))


    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(predict_list)