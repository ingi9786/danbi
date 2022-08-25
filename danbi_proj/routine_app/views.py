from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .form import RegisterForm, LoginForm
from django.contrib.auth import get_user_model



def main_view(request):
    return render(request, "main.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = {
                "msg"    : "Registered Success!",
                "status" : "USER_REGISTER_OK"
            }
        return render(request, "main.html", {"message":message})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            user_id = request.user.id
            print(user_id)
            message = {
                "msg"    : "Login Success!",
                "status" : "USER_LOGIN_OK"
            }
            return render(request, "main.html", {"message":message})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form":form})


def logout_view(request):
    logout(request)
    message = {
        "msg"    : "User is logged out.",
        "status" : "LOGOUT_DONE"
    }
    return render(request, "main.html", {"message":message})
