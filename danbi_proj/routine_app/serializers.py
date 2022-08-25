from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult
from django.contrib.auth import get_user_model
from rest_framework.response import Response



class ResultSerializer(serializers.ModelSerializer):
    # routine_result_id = serializers.IntegerField(required=False)

    class Meta:
        model = RoutineResult
        fields = ["result","routine"]
        read_only_fields = ('routine', )  # routine객체 생성 시 입력 할 필요 없이 create 로직에서 생성되게 만듬. 
        

class DaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # result = ResultSerializer()

    class Meta:
        model = RoutineDay 
        fields = ["id", "day", "routine"]
        read_only_fields = ("routine", )
        

class RoutineSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True) # readonly 해서 serializer까지 days가 못들어왔음 request.data까진 왔는데
    result = ResultSerializer(many=True) # day에서 result를 참조하게 함으로써 필요가 없어짐.
    # userid = serializers.SerializerMethodField(method_name="_get_userid", read_only=True)
    
    class Meta:
        model = Routine
        fields = [
            "routine_id", "title", "category", "goal", "is_alarm", "days", "result", "account"
        ]
    
    def create(self, validated_data):
        days = validated_data.pop("days")
        result = validated_data.pop("result")
        account = validated_data.pop("account")

        db = get_user_model()
        test_user = db.objects.get(id=10)

        routine = Routine.objects.create(**validated_data, account=test_user) 

        for day in days:
            # RoutineResult.objects.create(result='not', routine=routine)
            RoutineDay.objects.create(**day, routine=routine) # day도 JSON(dict)로 입력했을테니까 + routine객체
        for res in result:
            RoutineResult.objects.create(**res, routine=routine)
        return routine
    
    def update(self, instance, validated_data): # 1st 매개변수로 model instance를 받는다. 
        instance.routine_id = validated_data.get("routine_id", instance.routine_id)
        instance.title = validated_data.get("title", instance.title)
        instance.category = validated_data.get("category", instance.category)
        instance.goal = validated_data.get("goal", instance.goal)
        instance.is_alarm = validated_data.get("is_alarm", instance.is_alarm)
        
        db = get_user_model()
        test_user = db.objects.get(id=10)
        instance.account = test_user
        instance.save()

        days = validated_data.pop('days')
        result = validated_data.pop('result')
        for day in days:
            if 'id' in day.keys():  #  id가 있고
                if RoutineDay.objects.filter(id=day["id"]):
                    d = RoutineDay.objects.get(id=day["id"])
                    d.day = day.get("day", d.day)
                    d.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
                    d.save()
                else:
                    continue
                
        for res in result:
            print(res.keys())
            if 'routine_result_id' in res.keys():  #  id가 있고
                if RoutineResult.objects.filter(routine_result_id=res["routine_result_id"]):
                    r = RoutineResult.objects.get(routine_result_id=res["routine_result_id"])
                    r.result = res.get("result", r.result)
                    r.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
                    r.save()
                else:
                    continue
        return instance

            
        
        

'''
"days" : [
    {"day": "월"},
    {"day": "수"}   
]
'''

'''
{
    "title": "posttest",
    "category": "homework",
    "goal": "sibal",
    "is_alarm": false,
    "days": ["wed", "thu", "sat"],
    "account": 10
}
'''