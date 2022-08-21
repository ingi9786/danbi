from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .serializers import UserRegisterSerializer, UserLoginSerializer

# from django.contrib.auth.models import User
from .models import Myuser

# Create your views here.
def register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            res = {
                "msg"   : "Registered Success!",
                "status": "USER_REGISTER_OK"
            }
            return JsonResponse(res)

# 로그인도 post로 하니까
def login_view(request):
    if request.method == "GET":
        serializer = UserLoginSerializer()
        email = request.GET.get("email")
        password = request.GET.get("password")
        user = authenticate(email=email, password=password)
        # login(request, user, backend='routine_app.routine_auth.UserBackend')
        login(request, user)
        data = {'로그인': '성공'}
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    res = {
        "msg"   : "User is logged out.",
        "status": "LOGOUT_DONE"
    }
    return JsonResponse(res)
