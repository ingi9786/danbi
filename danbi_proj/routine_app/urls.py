
from .views import register_view, login_view, registerView
from django.urls import path

# from rest_framework import routers
# from shortener.urls.apis import *

# router = routers.DefaultRouter()
# router.register(r'urls', UrlListView)

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'', registerView)

urlpatterns = [
    path("register", register_view, name="register_view"),
    path("login", login_view, name="login_view"),
]
