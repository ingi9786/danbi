from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult
from django.contrib.auth import get_user_model

# read_only는 api출력(응답)에는 포함되나, 입력(요청)에는 포함되지 않게하는 속성 > 그니까 요청시 따로 함수 등에서 필요하다면 넣어줘야겠지?
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
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RoutineDay 
        fields = ["id", "day", "routine"]  # __all__ 헷갈림. 
        read_only_fields = ("routine", )


# required=False로 둬서 필요에 따라 입력 받도록 설정? 
class ResultSerializer(serializers.ModelSerializer):
    routine_result_id = serializers.IntegerField(required=False)

    class Meta:
        model = RoutineResult
        fields = ["routine_result_id", "result", "routine"]    
        read_only_fields = ('routine', )
    
# 이걸로 현재 조회가 가능한데, POST를 통한 create를 하기 싫으면 days, result에 required=False로 두자.
# 
class RoutineSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True) # readonly 해서 serializer까지 days가 못들어왔음 request.data까진 왔는데
    result = ResultSerializer(many=True)
    # account = 

    class Meta:
        model = Routine
        fields = ["title", "category", "goal", "is_alarm", "days", "result"]
    
    # def _get_userid(self, obj):
    #     user_id = self.context.get("user_id")
    #     if user_id:
    #         return obj.
    #     return False
    
    # POST를 이용한 create까지 지원하려면 커스텀 create가 필요
    def create(self, validated_data):
        # days, result는 routine모델의 필드가 아닌 prop이니까 validated data에서 뺴야한다.
        print(validated_data)
        result = validated_data.pop("result")
        days = validated_data.pop("days")

        db = get_user_model()
        test_user = db.objects.get(id=10)
        # or 
        
        
        routine = Routine.objects.create(**validated_data, account=test_user) 
    
        for day in days:
            RoutineDay.objects.create(**day, routine=routine) # day도 JSON(dict)로 입력했을테니까 + routine객체
        for res in result:
            RoutineResult.objects.create(**res, routine=routine)
        return routine
    
    # 동시에 PUT을 이용해서 update기능 지원하려면 customizing
    def update(self, instance, validated_data): # 1st 매개변수로 model instance를 받는다. 
        days = validated_data.pop('days')
        result = validated_data.pop('result')
        instance.title = validated_data.get("title", instance.title)
        instance.title = validated_data.get("category", instance.category)
        instance.title = validated_data.get("goal", instance.goal)
        instance.title = validated_data.get("is_alarm", instance.is_alarm)
        instance.save()
'''
"days" : [
    {"day": "월"},
    {"day": "수"}   
]
'''