# # 파일불러오기
# ## 파일 읽기
# file = open('news.txt', 'r', encoding='UTF8')
# text1 = file.read()
# file.close()
#
# # 전처리
# import re
#
# def cleanText(readData):
#     text = re.sub('[-=+,#/\?:^$.@*\※~&%ㆍ!』\'…》]', '', readData)
#     return text
#
# # 문장 분리
# from konlpy.tag import Kkma
#
# kkma = Kkma()  # 꼬꼬마는 중복을 제거한다.
# list_sentence = kkma.sentences(text1)
#
# # split함수 이용한 문장 분리
# split_text = cleanText(text1).split('\n')
#
# # *TF - IDF모델 생성
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# # https://chan-lab.tistory.com/24
# tf_idf = TfidfVectorizer()
# tf_idf.fit(split_text)  # 단어를 학습시킴
# tf_idf.vocabulary_  # 단어사전을 출력
# sorted(tf_idf.vocabulary_.items())  # 단어사전 정렬
#
# matrix = tf_idf.fit_transform(split_text)
# tf_idf_mat = tf_idf.transform(split_text).toarray()
# sent_graph = np.dot(tf_idf_mat, tf_idf_mat.T)
#
# # 그래프 생성
#
# class Rank(object):
#     def get_ranks(self, graph, d=0.85):  # d = damping factor
#         A = graph
#         matrix_size = A.shape[0]
#         for id in range(matrix_size):
#             A[id, id] = 0  # diagonal 부분을 0으로
#             link_sum = np.sum(A[:, id])  # A[:, id] = A[:][id]
#             if link_sum != 0:
#                 A[:, id] /= link_sum
#             A[:, id] *= -d
#             A[id, id] = 1
#
#         B = (1 - d) * np.ones((matrix_size, 1))
#         ranks = np.linalg.solve(A, B)  # 연립방정식 Ax = b
#         return {idx: r[0] for idx, r in enumerate(ranks)}
#
#
# rank = Rank()
# res = rank.get_ranks(sent_graph)
# sort_res = sorted(res, key=lambda i: res[i], reverse=True)
# print(sort_res)
# for i in range(0, 5):
#     print(split_text[sort_res[i]])