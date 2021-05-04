# import pandas
# import tokenizer as tokenizer
# from googleapiclient.discovery import build
# import pandas as pd
# import re
# import html
# import urllib.request
# from konlpy.tag import Okt
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
#
# from api.comment_model import okt, stopwords, loaded_model
#
#
# def comment_predict(video_id):
#     api_key = 'AIzaSyDmcbf1nWFgq4dsLVPa1doe12NWLUK5knc'
#     # video_id = 'V1WHgI2xM2k'
#
#     # 댓글 가져오기
#     # 댓글내용, 좋아요수, 작성자, 작성일
#     comments = list()
#     # comments=pd.DataFrame(columns=['commet', 'nickname', 'time', 'like'])
#     # comments = pd.DataFrame(comment, columns=['commet', 'nickname', 'time', 'like'])
#     api_obj = build('youtube', 'v3', developerKey=api_key)
#     response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
#
#     while response:
#         for item in response['items']:
#             comment = item['snippet']['topLevelComment']['snippet']
#             # print(comment['textDisplay']) #댓글 내용
#             comments.append(
#                 [comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
#
#             if item['snippet']['totalReplyCount'] > 0:
#                 for reply_item in item['replies']['comments']:
#                     reply = reply_item['snippet']
#                     comments.append(
#                         [reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
#
#         if 'nextPageToken' in response:
#             response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id,
#                                                      pageToken=response['nextPageToken'], maxResults=100).execute()
#         else:
#             break
#
#     df = pandas.DataFrame(comments)
#
#     comment = list()
#
#     # html 태그 제거하기
#     for row in df[0]:
#         cleaner = re.compile('<.*?>')
#
#         cleantext = re.sub(cleaner, '', row)
#         cleantext = html.unescape(cleantext)
#
#         only_BMP_pattern = re.compile("["
#                                       u"\U00010000-\U0010FFFF"  # BMP characters 이외
#                                       "]+", flags=re.UNICODE)
#
#         cleantext = only_BMP_pattern.sub(r'', cleantext)
#
#         comment.append(cleantext)
#     df[0] = comment
#
#     # 언어별 분류하기
#     def Language(row):
#         k_count = 0
#         e_count = 0
#         c_count = 0
#         j_count = 0
#         etc = 0
#
#         for c in row:
#             if ord('ㄱ') <= ord(c) <= ord('힣'):
#                 k_count += 1
#             elif ord('a') <= ord(c.lower()) <= ord('z'):
#                 e_count += 1
#             #         elif ord('一') <= ord(c.lower()) <= ord('龥'):
#             #             c_count+=1
#             else:
#                 etc += 1
#
#         if k_count >= 1:
#             sort = "한국어"
#             return sort
#         #     elif c_count>=1 :
#         #         sort = "중국어"
#         #         return sort
#         elif e_count >= 1:
#             sort = "영어"
#             return sort
#         else:
#             sort = "그외"
#             return sort
#
#     sort_comment = list()
#
#     # 각 댓글에 대해 수행
#     for row in df[0]:
#         sort_comment.append(Language(row))
#
#     df['sort'] = sort_comment
#
#     # 한국어인 댓글들만 뽑아오기
#     is_korean = df['sort'] == '한국어'
#     korean = df[is_korean]
#
#     # 리뷰 예측해보기
#
#     data_predict = pandas.DataFrame()
#
#     comment_list = list()
#     predict_list = list()
#
#     # 긍정 부정 예측
#     def sentiment_predict(new_sentence):
#         new_sentence_s = okt.morphs(new_sentence, stem=True)  # 토큰화
#         new_sentence_s = [word for word in new_sentence_s if not word in stopwords]  # 불용어 제거
#         encoded = tokenizer.texts_to_sequences([new_sentence_s])  # 정수 인코딩
#         #pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
#         pad_new = pad_sequences(encoded, maxlen=30)  # 패딩
#         score = float(loaded_model.predict(pad_new))  # 예측
#         if (score > 0.5):
#             return predict_list.append("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
#         else:
#             return predict_list.append("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))
#
#     for i in range(len(df[0])):
#         try:
#             if sentiment_predict(korean[0][i]) is not None:
#                 predict_list.append(sentiment_predict(korean[0][i]))
#         except KeyError:
#             i += i
#     # data_predict['predict'] = predict_list
#     # data_predict
#
#     korean['predict'] = predict_list
#
#     # 한국어가 아닌 댓글
#     not_korean = df['sort'] != '한국어'
#     other_language = df[not_korean]
#
#     js_korean = korean.to_json(orient='index', force_ascii=False)
#     js_other = other_language.to_json(orient='index', force_ascii=False)
#
#     return js_korean, js_other