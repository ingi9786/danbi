
from .views import main_view, register_view, login_view, logout_view
from django.urls import path, include
from .apis import RoutinetList, RoutineViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'routine', RoutineViewSet, basename='routine')

urlpatterns = [
    path("", main_view, name="main_view"),
    path("register", register_view, name="register_view"),
    path("login", login_view, name="login_view"),
    path("logout", logout_view, name='logout_view'),
    path('rou', RoutinetList.as_view(), name='routine_test'),
    path('', include(router.urls))
]
