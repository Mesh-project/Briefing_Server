from django.urls import path

from api import views

urlpatterns = [
    path('users/', views.user_list),
]