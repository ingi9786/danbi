from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult



class ResultSerializer(serializers.ModelSerializer):
    # routine_result_id = serializers.IntegerField(required=False)

    class Meta:
        model = RoutineResult
        fields = ["result","routine"]
        read_only_fields = ('routine', )
        

class DaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # result = ResultSerializer()

    class Meta:
        model = RoutineDay 
        fields = ["id", "day", "routine"]
        read_only_fields = ("routine", )
        

class RoutineSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True)
    result = ResultSerializer(many=True)

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
        user_obj = db.objects.get(id=account.id)

        routine = Routine.objects.create(**validated_data, account=user_obj) 

        for day in days:
            RoutineDay.objects.create(**day, routine=routine)
        for res in result:
            RoutineResult.objects.create(**res, routine=routine)
        return routine
    
    def update(self, instance, validated_data):
        instance.routine_id = validated_data.get("routine_id", instance.routine_id)
        instance.title      = validated_data.get("title", instance.title)
        instance.category   = validated_data.get("category", instance.category)
        instance.goal       = validated_data.get("goal", instance.goal)
        instance.is_alarm   = validated_data.get("is_alarm", instance.is_alarm)

        account = validated_data.get("account")
        db = get_user_model()
        user_obj = db.objects.get(id=account.id)
        instance.account = user_obj
        instance.save()

        days = validated_data.pop('days')
        result = validated_data.pop('result')
         
        for day in days:
            if 'id' in day.keys():
                if RoutineDay.objects.filter(id=day["id"]):
                    d = RoutineDay.objects.get(id=day["id"])
                    d.day = day.get("day", d.day)
                    d.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
                    d.save()
                else:
                    continue
                
        for res in result:
            if 'routine_result_id' in res.keys():
                if RoutineResult.objects.filter(routine_result_id=res["routine_result_id"]):
                    r = RoutineResult.objects.get(routine_result_id=res["routine_result_id"])
                    r.result = res.get("result", r.result)
                    r.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
                    r.save()
                else:
                    continue
        return instance