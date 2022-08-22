
from .views import main_view, register_view, login_view, logout_view
from django.urls import path

# from rest_framework import routers
# from shortener.urls.apis import *

# router = routers.DefaultRouter()
# router.register(r'urls', UrlListView)

urlpatterns = [
    path("", main_view, name="main_view"),
    path("register", register_view, name="register_view"),
    path("login", login_view, name="login_view"),
    path("logout", logout_view, name='logout_view')
]
