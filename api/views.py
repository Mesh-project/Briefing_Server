from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from api.models import user
from api.serializers import UserSerializer


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = user.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return JsonResponse({'data' : serializer.data}, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'message': '성공입니다.', 'data': data}, status=200)
        return JsonResponse(serializer.errors, status=400)

