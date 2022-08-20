
from .views import login_view
from django.urls import path

# from rest_framework import routers
# from shortener.urls.apis import *

# router = routers.DefaultRouter()
# router.register(r'urls', UrlListView)


urlpatterns = [
    path("login", login_view, name="login_view"),
]
