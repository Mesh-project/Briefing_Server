# import pandas as pd
# import numpy as np
# import re
# from tensorflow.python.keras.preprocessing.text import Tokenizer
# from tensorflow.python.keras.preprocessing.sequence import pad_sequences
#
# train_data = pd.read_table('/Users/ksb/PycharmProjects/briefing_Server/api/ratings_train.txt')
# test_data = pd.read_table('/Users/ksb/PycharmProjects/briefing_Server/api/ratings_test.txt')
#
# #train_data에 혹시 데이터에 중복이 있지는 않은지 확인해보기
# train_data['document'].nunique(), train_data['label'].nunique()
#
# #총 150,000개의 샘플이 존재하는데 document열에서 중복을 제거한 샘플의 개수가 146,182개라는 것은 약 4,000개의 중복 샘플이 존재한다는 의미입니다.
# #label 열은 0 또는 1의 값만을 가지므로 2가 출력되었습니다. 중복 샘플을 제거해보겠습니다.
# train_data.drop_duplicates(subset=['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
#
# #Null 값을 가진 샘플을 제거하겠습니다.
# train_data = train_data.dropna(how = 'any')
#
# # 우선 한글이 아니라 영어의 경우를 상기해보겠습니다. 영어의 알파벳들을 나타내는 정규 표현식은 [a-zA-Z]입니다.
# # 이 정규 표현식은 영어의 소문자와 대문자들을 모두 포함하고 있는 정규 표현식으로 이를 응용하면 영어에 속하지 않는 구두점이나 특수문자를 제거할 수 있습니다.
# # 예를 들어 알파벳과 공백을 제외하고 모두 제거하는 전처리를 수행하는 예제는 다음과 같습니다.
# text = 'do!!! you expect... people~ to~ read~ the FAQ, etc. and actually accept hard~! atheism?@@'
# re.sub(r'[^a-zA-Z ]', '', text) #알파벳과 공백을 제외하고 모두 제거
#
# #위의 범위 지정을 모두 반영하여 train_data에 한글과 공백을 제외하고 모두 제거하는 정규 표현식을 수행해봅시다.
# train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
#
# # train_data에 빈 값을 가진 행이 있다면 Null 값으로 변경하도록 하고, 다시 한 번 Null 값이 존재하는지 확인해보겠습니다.
# train_data['document'].replace('', np.nan, inplace=True)
#
# #Null 샘플들은 레이블이 긍정일 수도 있고, 부정일 수도 있습니다. 사실 아무런 의미도 없는 데이터므로 제거해줍니다.
# train_data = train_data.dropna(how = 'any')
#
# #샘플 개수가 또 다시 줄어서 이제 145,791개가 남았습니다. 테스트 데이터에 지금까지 진행했던 전처리 과정들을 동일하게 진행합니다.
# test_data.drop_duplicates(subset = ['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
# test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
# test_data['document'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
# test_data = test_data.dropna(how='any') # Null 값 제거
#
# #토큰화
#
# #이제 토큰화를 해보겠습니다. 토큰화 과정에서 불용어를 제거하겠습니다.
# # 불용어는 정의하기 나름인데, 한국어의 조사, 접속사 등의 보편적인 불용어를 사용할 수도 있겠지만 결국 풀고자 하는 문제의 데이터를 지속 검토하면서 계속해서 추가하는 경우 또한 많습니다.
# # 실제 현업인 상황이라면 일반적으로 아래의 불용어보다 더 많은 불용어를 사용하기도 합니다.
# stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
#
# #여기서는 위 정도로만 불용어를 정의하고, 토큰화를 위한 형태소 분석기는 KoNLPy의 Okt를 사용합니다. 잠시 Okt를 복습해봅시다.
# from konlpy.tag import Okt
#
# okt = Okt()
# okt.morphs('와 이런 것도 영화라고 차라리 뮤직비디오를 만드는 게 나을 뻔', stem = True)
#
#
# #Okt는 위와 같이 KoNLPy에서 제공하는 형태소 분석기입니다.
# # Okt는 위와 같이 KoNLPy에서 제공하는 형태소 분석기입니다.
# # 한국어을 토큰화할 때는 영어처럼 띄어쓰기 기준으로 토큰화를 하는 것이 아니라, 주로 형태소 분석기를 사용한다고 언급한 바 있습니다.
# # stem = True를 사용하면 일정 수준의 정규화를 수행해주는데,
# # 예를 들어 위의 예제의 결과를 보면 '이런'이 '이렇다'로 변환되었고 '만드는'이 '만들다'로 변환된 것을 알 수 있습니다.
#
# # 이제 train_data에 형태소 분석기를 사용하여 토큰화를 하면서 불용어를 제거하여 X_train에 저장합니다.
# X_train = []
# for sentence in train_data['document']:
#     temp_X = []
#     temp_X = okt.morphs(sentence, stem=True)  # 토큰화
#     temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
#     X_train.append(temp_X)
#
# # 형태소 토큰화가 진행된 것을 볼 수 있습니다. 테스트 데이터에 대해서도 동일하게 토큰화를 해줍니다.
# X_test = []
# for sentence in test_data['document']:
#     temp_X = []
#     temp_X = okt.morphs(sentence, stem=True)  # 토큰화
#     temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
#     X_test.append(temp_X)
#
# # 정수 인코딩
#
# # 이제 기계가 텍스트를 숫자로 처리할 수 있도록 훈련 데이터와 테스트 데이터에 정수 인코딩을 수행해야 합니다.
# # 우선, 훈련 데이터에 대해서 단어 집합(vocaburary)을 만들어봅시다.
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(X_train)
#
# threshold = 3
# total_cnt = len(tokenizer.word_index)  # 단어의 수
# rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
# total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
# rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합
#
# # 단어가 43,000개가 넘게 존재합니다.
# # 각 정수는 전체 훈련 데이터에서 등장 빈도수가 높은 순서대로 부여되었기 때문에, 높은 정수가 부여된 단어들은 등장 빈도수가 매우 낮다는 것을 의미합니다.
# # 여기서는 빈도수가 낮은 단어들은 자연어 처리에서 배제하고자 합니다.
# # 등장 빈도수가 3회 미만인 단어들이 이 데이터에서 얼만큼의 비중을 차지하는지 확인해봅시다.
# # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
# for key, value in tokenizer.word_counts.items():
#     total_freq = total_freq + value
#
#     # 단어의 등장 빈도수가 threshold보다 작으면
#     if (value < threshold):
#         rare_cnt = rare_cnt + 1
#         rare_freq = rare_freq + value
#
# # 등장 빈도가 threshold 값인 3회 미만. 즉, 2회 이하인 단어들은 단어 집합에서 무려 절반 이상을 차지합니다.
# # 하지만, 실제로 훈련 데이터에서 등장 빈도로 차지하는 비중은 상대적으로 매우 적은 수치인 1.87%밖에 되지 않습니다.
# # 아무래도 등장 빈도가 2회 이하인 단어들은 자연어 처리에서 별로 중요하지 않을 듯 합니다.
# # 그래서 이 단어들은 정수 인코딩 과정에서 배제시키겠습니다.
# # 등장 빈도수가 2이하인 단어들의 수를 제외한 단어의 개수를 단어 집합의 최대 크기로 제한하겠습니다.
# # 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
# # 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
# vocab_size = total_cnt - rare_cnt + 2
#
# # 이제 단어 집합의 크기는 19,417개입니다.
# # 이를 케라스 토크나이저의 인자로 넘겨주면, 케라스 토크나이저는 텍스트 시퀀스를 숫자 시퀀스로 변환합니다.
# # 이러한 정수 인코딩 과정에서 이보다 큰 숫자가 부여된 단어들은 OOV로 변환하겠습니다.
# # 다시 말해 정수 1번으로 할당합니다. (정수 인코딩 챕터 참고!)
# tokenizer = Tokenizer(vocab_size, oov_token='OOV')
# tokenizer.fit_on_texts(X_train)
# X_train = tokenizer.texts_to_sequences(X_train)
# X_test = tokenizer.texts_to_sequences(X_test)
#
# # 각 샘플 내의 단어들은 각 단어에 대한 정수로 변환된 것을 확인할 수 있습니다.
# # 굳이 확인하지는 않겠지만, 이제 단어의 개수는 19,417개로 제한되었으므로 0번 단어 ~ 19,416번 단어까지만 사용합니다.
# # (0번 단어는 패딩을 위한 토큰, 1번 단어는 OOV를 위한 토큰입니다.)
# # 다시 말해 19,417 이상의 정수는 더 이상 훈련 데이터에 존재하지 않습니다.
#
# # 이제 train_data에서 y_train과 y_test를 별도로 저장해줍니다.
# y_train = np.array(train_data['label'])
# y_test = np.array(test_data['label'])
#
# # 빈 샘플(empty samples) 제거
#
# # 전체 데이터에서 빈도수가 낮은 단어가 삭제되었다는 것은 빈도수가 낮은 단어만으로 구성되었던 샘플들은 이제 빈(empty) 샘플이 되었다는 것을 의미합니다.
# # 빈 샘플들은 어떤 레이블이 붙어있던 의미가 없으므로 빈 샘플들을 제거해주는 작업을 하겠습니다.
# # 각 샘플들의 길이를 확인해서 길이가 0인 샘플들의 인덱스를 받아오겠습니다.
# drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
#
# # 빈 샘플들을 제거
# X_train = np.delete(X_train, drop_train, axis=0)
# y_train = np.delete(y_train, drop_train, axis=0)
#
#
# # 패딩
#
# # 가장 긴 리뷰의 길이는 72이며, 그래프를 봤을 때 전체 데이터의 길이 분포는 대체적으로 약 11내외의 길이를 가지는 것을 볼 수 있습니다.
# # 모델이 처리할 수 있도록 X_train과 X_test의 모든 샘플의 길이를 특정 길이로 동일하게 맞춰줄 필요가 있습니다.
# # 특정 길이 변수를 max_len으로 정합니다. 대부분의 리뷰가 내용이 잘리지 않도록 할 수 있는 최적의 max_len의 값은 몇일까요?
# # 전체 샘플 중 길이가 max_len 이하인 샘플의 비율이 몇 %인지 확인하는 함수(below_threshold_len())를 만듭니다.
# def below_threshold_len(max_len, nested_list):
#     cnt = 0
#     for s in nested_list:
#         if (len(s) <= max_len):
#             cnt = cnt + 1
#     print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s' % (max_len, (cnt / len(nested_list)) * 100))
#
#
# # 위의 분포 그래프를 봤을 때, max_len = 30이 적당할 것 같습니다. 이 값이 얼마나 많은 리뷰 길이를 커버하는지 확인해봅시다.
# max_len = 30
# below_threshold_len(max_len, X_train)
#
# # 전체 훈련 데이터 중 약 94%의 리뷰가 30이하의 길이를 가지는 것을 확인했습니다. 모든 샘플의 길이를 30으로 맞추겠습니다.
# X_train = pad_sequences(X_train, maxlen=max_len)
# X_test = pad_sequences(X_test, maxlen=max_len)
#
# # LSTM으로 네이버 영화 리뷰 감성 분류하기
#
# # 모델을 만들어봅시다. 우선 필요한 도구들을 가져옵니다.
# from tensorflow.keras.layers import Embedding, Dense, LSTM
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
#
# # 임베딩 벡터의 차원은 100으로 정했고, 리뷰 분류를 위해서 LSTM을 사용합니다.
# model = Sequential()
# model.add(Embedding(vocab_size, 100))
# model.add(LSTM(128))
# model.add(Dense(1, activation='sigmoid'))
#
# # 검증 데이터 손실(val_loss)이 증가하면, 과적합 징후므로 검증 데이터 손실이 4회 증가하면 학습을 조기 종료(Early Stopping)합니다.
# # 또한, ModelCheckpoint를 사용하여 검증 데이터의 정확도(val_acc)가 이전보다 좋아질 경우에만 모델을 저장합니다.
# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
# mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
#
# # 에포크는 총 15번을 수행하겠습니다. 또한 훈련 데이터 중 20%를 검증 데이터로 사용하면서 정확도를 확인합니다.
# model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
# history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)
#
# # 조기 종료 조건에 따라서 9번째 에포크에서 훈련이 멈춥니다.
# # 훈련이 다 되었다면 이제 테스트 데이터에 대해서 정확도를 측정할 차례입니다.
# # 훈련 과정에서 검증 데이터의 정확도가 가장 높았을 때 저장된 모델인 'best_model.h5'를 로드합니다.
# loaded_model = load_model('best_model.h5')
# #print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_test, y_test)[1]))