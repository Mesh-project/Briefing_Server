# 파일불러오기
## 파일 읽기
# file = open('news.txt', 'r', encoding='UTF8')
# text1 = file.read()
# file.close()

# *TF - IDF모델 생성
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# 문장 분리
from konlpy.tag import Kkma, Okt


def Topic(readData):
    text = re.sub('[-=+,#/\?:^$@*\※~&%ㆍ!』\'…》]', '', readData)
    text = text.split('.')

    print(text)
    print("text 출력 완료 ")

    print(text)
    print("list_sentence 출력 완료 ")

    tf_idf = TfidfVectorizer()
    tf_idf.fit(text)  # 단어를 학습시킴

    print("단어 학습중???")

    tf_idf.vocabulary_  # 단어사전을 출력
    sorted(tf_idf.vocabulary_.items())  # 단어사전 정렬

    print("과연 될까???")

    matrix = tf_idf.fit_transform(text)
    tf_idf_mat = tf_idf.transform(text).toarray()
    sent_graph = np.dot(tf_idf_mat, tf_idf_mat.T)

    rank = Rank()
    res = rank.get_ranks(sent_graph)
    sort_res = sorted(res, key=lambda i: res[i], reverse=True)
    print(sort_res)

    topic_result = ""

    if len(sort_res) < 2:
        print(text[sort_res[0]])
        topic_result = text[sort_res[0]]
    elif len(sort_res) < 3:
        for i in range(0, 2):
            print(text[sort_res[i]])
            topic_result = topic_result+text[sort_res[i]]+"."+"\n"
    else:
        for i in range(0, 2):
            print(text[sort_res[i]])
            topic_result = topic_result+text[sort_res[i]]+"."+"\n"

    for i in range(0, 10):
        print(text[sort_res[i]])
        topic_result_predict = topic_result + text[sort_res[i]] + "." + "\n"

    return [topic_result, topic_result_predict]

# 그래프 생성

class Rank(object):
    def get_ranks(self, graph, d=0.85):  # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0  # diagonal 부분을 0으로
            link_sum = np.sum(A[:, id])  # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1

        B = (1 - d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)  # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}


