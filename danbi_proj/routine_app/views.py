from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .serializers import UserRegisterSerializer


# Create your views here.
def register(request):
    if request.method == "POST":
        pass
    else:
        pass

def login_view(request, user_id=None):
    if request.method == "GET":
        # serializer= UserRegisterSerializer()
        email = request.GET.get("email")
        password = request.GET.get("password")
        user = authenticate(username=email, password=password)
        login(request, user)
        data = {'로그인': '성공'}
    return JsonResponse(data)
