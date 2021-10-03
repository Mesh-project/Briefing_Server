from __future__ import print_function
import json
import urllib
from ast import literal_eval

import datetime

from docutils.nodes import comment

from api.comment_model import comment_predict
from django.http import JsonResponse

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# from api.comment import comment_predict

from api.info import video_info
from api.models import user, analysis
from api.script_predict import script_predict
from api.serializers import UserSerializer, AnalysisSerializer
from urllib import request


import time
import boto3

# 로그인
# test용 로그인 (user_id: "test", user_pw: "1234")
from api.s3 import stt_mp4
from api.topic import Topic
from api.word_cloud import word_stt
from briefing_Server.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if user.objects.filter(user_id=data["user_id"]).exists():
                user_data = user.objects.get(user_id=data["user_id"])

                if data['user_pw'] == user_data.user_pw:
                    return JsonResponse({'success' : True, 'message' : "성공", "user_idx" : user_data.user_idx}, status=200)
                return JsonResponse({'success' : False, 'message' : "Wrong Password"}, status=401)
            return JsonResponse({'success' : False,'message' : "No ID"},status=400)
        except KeyError:
            return JsonResponse({'success' : False, 'message' : "INVALID_KEYS"}, status=400)

# 회원가입
class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if user.objects.filter(user_id=data["user_id"]).exists():
                return JsonResponse({"status" : 400,"message" : "EXISTS_ID"}, status=400)

            user.objects.create(
                user_id = data['user_id'],
                user_pw = data['user_pw']
            ).save()
            return JsonResponse({"status" : 200,"message" : "성공","data" : data}, status=200)
        except KeyError:
            return JsonResponse({"status" : 400,'message': "INVALID_KEYS"}, status=400)


# 아래코드들은
# 예시로 적어둔 api로 참고용으로만 사용후 수정 예정
# jwt 토큰 생성 전에 짜둔 코드로 토큰 관련해서 코드 구현하지 않았음.

# 사용자 리스트 (실제 앱에서 쓸 API는 아님. 테스트용으로 구현했으며, 추후 삭제 예정)
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = user.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse({"status" : 200, 'data' : serializer.data}, status=200)

@csrf_exempt
def get_history(request, user_index):
    if request.method == 'GET':

        index_data = analysis.objects.filter(user_idx=user_index).values()
        serializer = AnalysisSerializer(index_data, many=True)
        return JsonResponse({"status" : 200, 'data' : serializer.data}, status=200)

@csrf_exempt
def get_history_detail(request, history_idx):
    if request.method == 'GET':
        index_data = analysis.objects.filter(analysis_idx=history_idx).values()
        serializer = AnalysisSerializer(index_data, many=True)
        return JsonResponse({"status": 200, 'data': serializer.data[0]}, status=200)


@csrf_exempt
def get_analysis(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        url_data_analysis = data.get('url')#.split('=') #JSONParser().parse(request)
        url_data_analysis=url_data_analysis[32:]#=url_data_analysis.replace("https://www.youtube.com/watch?v=","")
        print(url_data_analysis)

        idx_data = data['user_idx']
        crawling_data = video_info(url_data_analysis)

        voice_stt = stt_mp4(data.get('url'))
        print("jkljkljlk")
        file_name = voice_stt.default_filename
        voice_stt.download()

        bucket = boto3.resource('s3')
        print(str(bucket))

        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        s3_client.upload_file(file_name, "meshstt", "video.mp3")

        # 삭제 만들 예정
        # os.remove('../'+file_name)

        transcribe = boto3.client('transcribe')
        job_name = str(datetime.datetime.now().date()) + str(datetime.datetime.now().hour) + str(
            datetime.datetime.now().minute)
        job_uri = "s3://meshstt/video.mp3"

        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp4',
            LanguageCode='ko-KR'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                break
            print("Not ready yet...")
            time.sleep(5)

        # Transcribe 결과가 저장된 웹주소
        save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

        # 웹서버 결과 파이썬으로 불러오기
        load = urllib.request.urlopen(save_json_uri)
        confirm = load.status
        rst = load.read().decode('utf-8')

        # 문자열을 딕셔너리로 변환 후 결과 가져오기
        transcribe_text = literal_eval(rst)['results']['transcripts'][0]['transcript']

        # word cloud 생성
        word= word_stt(transcribe_text)
        word_cloud = word[0]
        top_word = word[1]


        print(transcribe_text)


        topic_all = Topic(transcribe_text)
        topic_result = topic_all[0]
        a = script_predict(topic_all[1])

        print(a[0])

        analysis.user_idx = idx_data

        analysis.objects.create(
            user_idx=idx_data,
            url=data['url'],
            title=crawling_data.get('title'),
            thumbnail=crawling_data.get('thumbnail'),
            channel_name=crawling_data.get('author'),
            video_time=crawling_data.get('video_time'),
            topic=topic_result,
            script=transcribe_text,
            wordcloud="https://meshstt.s3.ap-northeast-2.amazonaws.com/" + word_cloud,
            topword= top_word,
            script_predict = a[0]
        ).save()
        info_data = {
            'user_idx' : idx_data,
            'url' : data['url'],
            'analysis_date' : "2020-01-01",
            'title' : crawling_data.get('title'),
            'thumbnail' : crawling_data.get('thumbnail'),
            'channel_name': crawling_data.get('author'),
            'video_time' : crawling_data.get('video_time'),
            'topic' : topic_result,
            'script' : transcribe_text,
            'wordcloud' : "https://meshstt.s3.ap-northeast-2.amazonaws.com/" + word_cloud,
            'topword' : top_word,
            'script_predict' : a[0]
        }
        return JsonResponse({"status" : 200, 'message' : '성공', 'data':info_data}, status=200)


@csrf_exempt
def get_comment(request):
    if request.method == 'POST':
        url_data = JSONParser().parse(request)
        comment = comment_predict(url_data.get('url')) # 객체 받아와짐

        # comment_predict(url_data.get('url')).

    return JsonResponse({'success': True,
                         'message': 'Success.',
                         'count': comment.get('comment_count'),
                         'korean_data': comment.get('korean_dict'),
                         # 'english_dict': comment.get('english_dict'),
                         'etc_data' : comment.get('etc_dict')},
                        status=200)

@csrf_exempt
def s3_stt(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print("12121212121212121212121")

        voice_stt = stt_mp4(data.get('url'))
        print("jkljkljlk")
        file_name = voice_stt.default_filename
        voice_stt.download()

        bucket = boto3.resource('s3')
        print(str(bucket))

        s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )

        print(str(bucket))
        print("어렵다어렵다 어렵다어렵다")
        s3_client.upload_file(file_name, "meshstt","video.mp3")

        print("1111111111111")

        print(boto3)

        print(boto3.client('transcribe'))

        transcribe = boto3.client('transcribe')

        print("222222222")

        job_name = str(datetime.datetime.now().date())+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)

        print("33333333333333333")

        job_uri = "s3://meshstt/video.mp3"

        print("4444444444")

        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp4',
            LanguageCode='ko-KR'
        )

        print("55555555")

        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                break
            print("Not ready yet...")
            time.sleep(5)

        # Transcribe 결과가 저장된 웹주소
        save_json_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

        # 웹서버 결과 파이썬으로 불러오기
        load = urllib.request.urlopen(save_json_uri)
        rst = load.read().decode('utf-8')

        # 문자열을 딕셔너리로 변환 후 결과 가져오기
        transcribe_text = literal_eval(rst)['results']['transcripts'][0]['transcript']

        print(transcribe_text)

        # topic = Topic(transcribe_text)
        # # print(str(topic))


        return JsonResponse({'success': True, 'message': '성공입니다.', 'crawling_data' : transcribe_text}, status=200)
