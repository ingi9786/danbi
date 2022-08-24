from .models import Routine, RoutineDay, RoutineResult
from .serializers import RoutineSerializer, DaySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RoutinetList(APIView):
    """
    List all routines, or create a new routine.
    """
    def post(self, request, format=None):
        print(request.data)
        # user_id = request.user.id
        user_id = 10
        serializer = RoutineSerializer(data=request.data) # context={"user_id":user_id}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get test >  http://127.0.0.1:8000/rou 
    def get(self, request, format=None):
        r = Routine.objects.filter(routine_id=1)
        serializer = RoutineSerializer(r, many=True)
        return Response(serializer.data)
    

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import JSONRenderer


class RoutineViewSet(viewsets.GenericViewSet):
    serializer_class = RoutineSerializer
    lookup_field = 'routine_id'
    
    # 유저와 get으로 들어온 유저id로 필터된 routine쿼리셋
    def get_queryset(self):
        uid = self.request.user.id
        return Routine.objects.filter(account=uid)

    @renderer_classes([JSONRenderer])
    def create(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = { "msg"    : "You have successfully created the routine.",
                    "status" : "ROUTINE_CREATE_OK_201" }
            return Response(
                {
                    "data"   : serializer.data,
                    "message": msg
                })
    
    @renderer_classes([JSONRenderer])
    def retrieve(self, request, routine_id=None):
        query = self.get_queryset().filter(pk=routine_id).first()

        if not query:
            msg = { "msg"    : "routine could not be found.",
                    "status" : "NOT_FOUND_404"}
            return Response({"message": msg})

        serializer = RoutineSerializer(query)
        msg = { "msg"    : "Routine lookup was successful.",
                "status" : "ROUTINE_DETAIL_OK_200" }
        # return Response(
        #     {
        #         "data"   : serializer.data,
        #         "message": msg
        #     })
        return Response(serializer.data)

    @renderer_classes([JSONRenderer])
    def update(self, request, routine_id=None):
        instance = self.get_object()                # routine 객체
        serializer = RoutineSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = {
                "msg"    : "The routine has been modified.",
                "status" : "ROUTINE_UPDATE_OK_200"
            }
            # return Response({
            #         "data":serializer.data,
            #         "message": msg
            #         })
            return Response(serializer.data)

    @renderer_classes([JSONRenderer])
    def destroy(self, request, routine_id=None):
        msg = { "msg"    : "The routine has been deleted.",
                "status" : "ROUTINE_DELETE_OK_200"}
        query = self.get_queryset().filter(pk=routine_id)
        if not query:
            msg= { "msg" : "routine could not be found.",
                  "status" : "NOT_FOUND_404"}
        query.delete()
        return Response({"message":msg})
    
    # 유저가 갖고 있는 outine 전부 보여주기 
    def list(self, request):
        queryset = self.get_queryset().all()
        serializer = RoutineSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # detail action(id를 필요로 하는 개별 action)이면 True
    # list action (id가 필요없는 리스트 action)이면 False
    
    # daylist에 mon이 들어가거나 
    @action(detail=False, methods=["GET"])
    def days(self, request):
        queryset = self.get_queryset().all() # 유저로 특정된 routine들이 있음.
        date = request.GET.get('date')
        _date = "mon"    # 날짜 to 요일 변경 로직
        day_list = []
        for query in queryset:
            r_id = query.routine_id
            day_obj = RoutineDay.objects.filter(day=_date, id=r_id).first()
            if not day_obj:
                continue
            day_list.append(day_obj)
        serializer = DaySerializer(day_list, many=True)
        return Response(serializer.data)

 

    # local/routine/daylist/?date GET > 월요일 일정모두 내놔 
    
    # local/routine/daydetail/d_id/?date GET, UPDATE, DELETE/CREATE
    # @action(detail=False, methods=["GET", "PUT"])
    # def daydetail(self, request, day_id=None):
    #     # 쿼리로 넘어온 날짜를 str()요일로 바꾸는 로직
    #     day = "mon"
    #     if request.method == "GET":
    #         query = RoutineDay.objects.filter(day=day, id=day_id).first()
    #         if not query:
    #             msg= { "msg" : "Couldn't find that routine detail",
    #                    "status" : "NOT_FOUND_404"}
    #             return Response({"message":msg})

    #         msg = { "msg" : "Routine detail lookup was successful.",
    #                 "status" : "ROUTINE_DETAIL_OK_200"}
    #         serializer = DaySerializer(query)
    #         return Response(serializer.data)
        
    #     else:
            
            