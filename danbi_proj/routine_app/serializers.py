# from django.contrib.auth.models import User
from .models import Myuser
from rest_framework import serializers


# auth user model을 수정없이 사용하므로 field명 안건들이고 method만 정의한다.
# 회원가입은 직렬화 이후에 model을 저장해야하므로 create를 재정의한거임.

# def create(self, validated_data):
    # return Snippet.objects.create(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    username  = serializers.CharField()
    email     = serializers.EmailField(required=True)
    password  = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email    = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"msg": "Passwords do not match"})
        return attrs

    # # 따로 만들어서 validators param =[] 으로 줄까?
    # def validate_email():
    #     pass
    
    # def validate_password():
    #     pass
    
    # class Meta:
    #     model = User
    #     field = "__all__"


        

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = ["email", "password"]

    