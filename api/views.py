import json

import bcrypt as bcrypt
from django.http import JsonResponse, HttpResponse
import jwt

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from api.info import video_info
from api.models import user
from api.serializers import UserSerializer
from briefing_Server.settings import SECRET_KEY

# 로그인
# test용 로그인 (user_id: "test", user_pw: "1234")
class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if user.objects.filter(user_id=data["user_id"]).exists():
                user_data = user.objects.get(user_id=data["user_id"])

                if bcrypt.checkpw(data['user_pw'].encode('UTF-8'), user_data.user_pw.encode('UTF-8')):
                    token = jwt.encode({'user_id' : user_data.user_id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'success' : True, 'message' : "성공입니다.","token": token}, status=200)
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
                return JsonResponse({"message" : "EXISTS_ID"}, status=400)

            user.objects.create(
                user_id = data['user_id'],
                user_pw = bcrypt.hashpw(data['user_pw'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
            ).save()
            return JsonResponse({"success" : True, "message" : "성공입니다","data" : data}, status=200)
        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status=400)


# 아래코드들은
# 예시로 적어둔 api로 참고용으로만 사용후 수정 예정
# jwt 토큰 생성 전에 짜둔 코드로 토큰 관련해서 코드 구현하지 않았음.

# 사용자 리스트 (실제 앱에서 쓸 API는 아님. 테스트용으로 구현했으며, 추후 삭제 예정)
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = user.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse({'data' : serializer.data}, status=200)


# 사용자별 영상 분석 기록 리스트 + 히스토리에서 아이템 클릭시 상세화면 정보를 보내줄 api 구현 필요
# @csrf_exempt
# def history_list(request, pk):
#     obj = model_analysis.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = AnalysisSerializer(obj)
#         # DB에 저장되는 부분이 아니라 즉각적으로 분석하고 바로 클라이언트에 보내줄 데이터(일시적인 데이터)
#         comment_data = {
#             'bad_comment': [
#                 "못생겼다.", "재미없다. 이딴 거 할 시간에 잠이나 자라.", "멍청하게 생김", "이러니까 나라가 망하지 ㅉㅉ"
#             ],
#             'good_comment': [
#                 "영상 재밌게 보고 갑니다.", "유익한 정보인 것 같아요.", "아직도 살만한 세상이네요."
#             ],
#             'english_comment' : [
#                 "this is very funny video.", "I think that is not good"
#             ],
#             'chinese_comment' : [
#                 "中國語", "玩得很尽兴"
#             ],
#             'etc_comment' : [
#                 "とても陽気", "أهلا"
#             ]
#         }
#         return JsonResponse({'data' : serializer.data, 'comment_data' : comment_data}, status=200)



# 영상 url을 통한 분석 데이터 저장 및 결과값 return
# @csrf_exempt
# def analysis_view(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#
#         analysis_data = {
#             'user_idx' : data.get('user_idx'),
#             'url' : data.get('url'),
#             'title' : "크롤링한 제목",
#             'thumbnail' : "https://onaliternote.files.wordpress.com/2016/11/wp-1480230666843.jpg",
#             'channel_name' : "크롤링한 채널명",
#             'video_time' : "01:00:00",
#             'video_date' : "2021.01.01",
#             'topic' : "주제 분석 결과",
#             'graph_language' : "50,30,10,10",
#             'graph_bad_comment' : "65,35"
#         }
#         #DB에 저장되는 부분이 아니라 즉각적으로 분석하고 바로 클라이언트에 보내줄 데이터(일시적인 데이터)
#         comment_data = {
#             'bad_comment' : [
#                 "못생겼다.", "재미없다. 이딴 거 할 시간에 잠이나 자라.", "멍청하게 생김", "이러니까 나라가 망하지 ㅉㅉ"
#             ],
#             'good_comment' : [
#                 "영상 재밌게 보고 갑니다.", "유익한 정보인 것 같아요.", "아직도 살만한 세상이네요."
#             ]
#         }
#         serializer = AnalysisSerializer(data=analysis_data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({
#                 'success': True,
#                 'message': '성공입니다.',
#                 'data': analysis_data,
#                 'comment_data' : comment_data
#             }, status=200)
#     return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def ex(request):
    if request.method == 'POST':
        url_data = JSONParser().parse(request)
        crawling_data = video_info(url_data.get('url'))

        # info_data = {
        #     'title' : crawling_data.title,
        #     'author' : crawling_data.author,
        #     'published' : crawling_data.published,
        #     'thumnail' : crawling_data.thumbnail,
        #     'time' : crawling_data.time
        # }

        return JsonResponse({'success' : True, 'message' : '성공입니다.', 'data':crawling_data}, status=200)