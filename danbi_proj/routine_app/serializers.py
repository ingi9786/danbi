from rest_framework import serializers
from .models import Routine, RoutineDay, RoutineResult
from django.contrib.auth import get_user_model

# read_only는 api출력(응답)에는 포함되나, 입력(요청)에는 포함되지 않게하는 속성 > 그니까 요청시 따로 함수 등에서 필요하다면 넣어줘야겠지?
# 따라서 create에는 필요 없겠지? 
# writeonly는 반대 필드를 입력에는쓰고 출력에 안쓰게 하는 속성 (응답에 안보임)
# day = serializers.DateField(initial = datetime.date.today)

# required=False로 둬서 필요에 따라 입력 받도록 설정? 
class ResultSerializer(serializers.ModelSerializer):
    # routine_result_id = serializers.IntegerField(required=False)

    class Meta:
        model = RoutineResult
        fields = ["result",] # "routine_result_id", "routine"    
        # read_only_fields = ('routine', )
        

class DaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    result = ResultSerializer()

    class Meta:
        model = RoutineDay 
        fields = ["id", "day", "routine", "result"]
        read_only_fields = ("routine", )
        
# 이걸로 현재 조회가 가능한데, POST를 통한 create를 하기 싫으면 days, result에 required=False로 두자.
# 
class RoutineSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True) # readonly 해서 serializer까지 days가 못들어왔음 request.data까진 왔는데
    # result = ResultSerializer(many=True) # day에서 result를 참조하게 함으로써 필요가 없어짐. 
    # account = serializers.SerializerMethodField(name="_get_userid")

    class Meta:
        model = Routine
        fields = [
            "routine_id", "title", "category",
            "goal", "is_alarm", "days", 
        ] # "result", "account"
    
    # https://stackoverflow.com/questions/22988878/pass-extra-arguments-to-serializer-class-in-django-rest-framework
    # def _get_userid(self, obj):
    #     user_id = self.context.get("user_id")
    #     if user_id:
    #         return obj.
    #     return False
    
    # POST를 이용한 create까지 지원하려면 커스텀 create가 필요
    def create(self, validated_data):
        # days, result는 routine모델의 필드가 아닌 prop이니까 validated data에서 뺴야한다.
        # result = validated_data.pop("result")
        days = validated_data.pop("days")

        db = get_user_model()
        test_user = db.objects.get(id=10)
        # uid = validated_data.pop 작성 중 근데 이거 아닌듯
        routine = Routine.objects.create(**validated_data, account=test_user) 
    
        for day in days:
            RoutineDay.objects.create(**day, routine=routine) # day도 JSON(dict)로 입력했을테니까 + routine객체
        # for res in result:
        #     RoutineResult.objects.create(**res, routine=routine)
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
        # result = validated_data.pop('result')
        for day in days:
            if 'id' in day.keys():  #  id가 있고
                if RoutineDay.objects.filter(id=day["id"]):
                    d = RoutineDay.objects.get(id=day["id"])
                    d.day = day.get("day", d.day)
                    d.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
                    d.save()
                else:
                    continue
                
        # for res in result:
        #     print(res.keys())
        #     if 'routine_result_id' in res.keys():  #  id가 있고
        #         if RoutineResult.objects.filter(routine_result_id=res["routine_result_id"]):
        #             r = RoutineResult.objects.get(routine_result_id=res["routine_result_id"])
        #             r.result = res.get("result", r.result)
        #             r.routine = Routine.objects.filter(routine_id=instance.routine_id).first()
        #             r.save()
        #         else:
        #             continue
        return instance

            
        
        

'''
"days" : [
    {"day": "월"},
    {"day": "수"}   
]
'''