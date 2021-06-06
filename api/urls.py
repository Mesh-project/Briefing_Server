from django.urls import path

from api import views

urlpatterns = [
    path('user_test/', views.user_list), # 사용자 전체 정보 확인하는 테스트용 api
    path('signin/', views.SignIn.as_view()), # 로그인
    path('signup/', views.SignUp.as_view()), # 회원가입
    path('analysis/', views.get_analysis),
    path('comment/', views.get_comment),
    path('history/<int:user_index>', views.get_history),
    path('stt/', views.s3_stt)
]