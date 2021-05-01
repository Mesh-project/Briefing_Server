from django.urls import path

from api import views

urlpatterns = [
    path('user_test/', views.user_list), # 사용자 전체 정보 확인하는 테스트용 api
    path('signin/', views.SignIn.as_view()), # 로그인
    path('signup/', views.SignUp.as_view()), # 회원가입
    # path('history/<int:pk>/',views.history_list),
    # path('analysis/', views.analysis_view),
    path('ex/', views.ex),
]