from django.contrib.auth.models import User
from rest_framework import serializers


# auth user model을 수정없이 사용하므로 field명 변경없이 
# method만 정의한다. 
class UserRegisterSerializer(serializers.ModelSerializer):
    def create(self, request, data):
        user = User.objects.create_user(
            email    = data["email"],
            password = data["password"]
        )
        user.save()
        return user

    class Meta:
        model   = User
        exclued = "password"