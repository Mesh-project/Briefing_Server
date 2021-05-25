import json

import boto3

from api.comment_model import comment_predict
from django.http import JsonResponse, HttpResponse
import jwt

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# from api.comment import comment_predict

from api.info import video_info
from api.models import user, analysis
from api.serializers import UserSerializer, AnalysisSerializer
from api.stt import stt_mp4
from briefing_Server.settings import SECRET_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


# 로그인
# test용 로그인 (user_id: "test", user_pw: "1234")
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
def get_analysis(request):
    data = json.loads(request.body)

    if request.method == 'POST':
        data = json.loads(request.body)
        url_data = data['url'] #JSONParser().parse(request)
        print(url_data)
        idx_data = data['user_idx']
        crawling_data = video_info(url_data)

        # token = request.META.get('HTTP_AUTHORIZATION')
        # id_token = request.headers['Authorization']
        # print(type(id_token))
        # print(id_token)
        #
        # byte_token = bytes(id_token, 'utf-8')
        # print(byte_token)
        #
        # dict_data = {'token' : byte_token.decode('utf-8')}
        # print(dict_data['token'])
        #
        # result = jwt.decode(dict_data['token'], SECRET_KEY, algorithms='HS256')
        #
        # print(result)
        # print(type(result))

        analysis.user_idx = idx_data

        analysis.objects.create(
            user_idx=idx_data,
            url=data['url'],
            title=crawling_data.get('title'),
            thumbnail=crawling_data.get('thumbnail'),
            channel_name=crawling_data.get('author'),
            video_time=crawling_data.get('video_time'),
            topic="한국 경제 전망이 밝아진 것은 세계 경제 회복 영향이 큰 것으로 풀이된다. "
                  "실제 OECD는 이날 올해 세계 경제성장률 전망치를 종전(42)보다 14포인트나 올려 잡았다. "
                  "OECD는 코로나19 백신 접종 확대와 주요국의 추가 재정 부양책 등으로 세계 경제 성장세가 확대될 것이라고 내다봤다. "
                  "OECD는 미국 성장률 전망치를 종전 32에서 65로 끌어올렸다. "
                  "이른바 백신 효과에 세계 경제 회복 속도가 빨라지리란 전망이 확산되고 있다"

        ).save()
        info_data = {
            'user_idx' : idx_data,
            'url' : data['url'],
            'analysis_date' : "2020-01-01",
            'title' : crawling_data.get('title'),
            'thumnail' : crawling_data.get('thumbnail'),
            'channel_name': crawling_data.get('author'),
            'video_time' : crawling_data.get('video_time'),
            'topic' : "한국 경제 전망이 밝아진 것은 세계 경제 회복 영향이 큰 것으로 풀이된다. "
                  "실제 OECD는 이날 올해 세계 경제성장률 전망치를 종전(42)보다 14포인트나 올려 잡았다. "
                  "OECD는 코로나19 백신 접종 확대와 주요국의 추가 재정 부양책 등으로 세계 경제 성장세가 확대될 것이라고 내다봤다. "
                  "OECD는 미국 성장률 전망치를 종전 32에서 65로 끌어올렸다. "
                  "이른바 백신 효과에 세계 경제 회복 속도가 빨라지리란 전망이 확산되고 있다"
        }
        return JsonResponse({"status" : 200, 'message' : '성공', 'data':info_data}, status=200)


@csrf_exempt
def get_comment(request):
    if request.method == 'POST':
        url_data = JSONParser().parse(request)
        comment = comment_predict(url_data.get('url'))

    return JsonResponse({'success': True, 'message': 'Success.', 'korean_data': comment[0].to_dict(orient='records'), 'etc_data': comment[1].to_dict(orient='records')}, status=200)


# @csrf_exempt
# def s3_stt(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         voice_stt = stt_mp4(data.get('url'))
#
#         bucket = boto3.resource('s3')
#
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id = AWS_ACCESS_KEY_ID,
#             aws_secret_access_key = AWS_SECRET_ACCESS_KEY
#         )
#
#         name = "stt_sample"
#
#         s3_client.upload_file(voice_stt, bucket, str(name))
#
#         return HttpResponse({'success': True, 'message': '성공입니다.'}, status=200)