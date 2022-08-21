from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .serializers import UserRegisterSerializer, UserLoginSerializer

from django.contrib.auth.models import User

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
        serializer= UserLoginSerializer()
        email = request.GET.get("email")
        password = request.GET.get("password")
        user = authenticate(username=email, password=password)
        login(request, user, backend='routine_app.routine_auth.UserBackend')
        data = {'로그인': '성공'}
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    res = {
        "msg"   : "User is logged out.",
        "status": "LOGOUT_DONE"
    }
    return JsonResponse(res)



#############
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

class registerView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        # POST METHOD
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            res = {
                "msg"   : "Registered Success!",
                "status": "USER_REGISTER_OK"
            }
            return JsonResponse(res)