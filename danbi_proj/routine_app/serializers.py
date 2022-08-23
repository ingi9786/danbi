from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult

# read_only는 api출력(응답)에는 포함되나, 입력(요청)에는 포함되지 않게하는 속성
# 따라서 create에는 필요 없겠지? 
# writeonly는 반대 필드를 입력에는쓰고 출력에 안쓰게 하는 속성 (응답에 안보임)
# day = serializers.DateField(initial = datetime.date.today)

# 유튜브 양놈 안경잡이
# class RoutineCreateSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100, required=True)
#     category = serializers.ChoiceField(choices=["MIRACLE", "HOMEWORK"], allow_blank=False)
#     goal = serializers.CharField(max_length=300, blank=True) 
#     is_alarm = serializers.BooleanField(default=False)
#     days = serializers.MultipleChoiceField(required=True, write_only=True)
#     # _days = serializers.SerializerMethodField('_get_days')
    
#     # def _get_days(self, routine_obj):
#     #     day = RoutineDay.objects.filter(routine_id= routine_obj.id)


# # 유튭 빠박이 7시간
# class RoutineReviewSerializer(serializers.Serializer):
#     days = serializers.SerializerMethodField()
#     class meta:
#         model = Routine
#         fields = ["title", "category", "goal", "is_alarm", "days"]
    
#     def _get_days(self, obj):
#         r_id = obj.id
#         obj.u


# routine create랑 확인 하는 거랑 다르게 가는 건 맞을듯 이건 중첩 serializer
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = "__all__"

    read_only_fields = ('routine')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = '__all__'
    
    read_only_fields = ('routine')
    

class RoutineSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    result = ResultSerializer(many=True, read_only=True)
    class Meta:
        model = Routine
        # fields = ["title", "category", "goal", "is_alarm", "days"]
        fields = "__all__"
        
        