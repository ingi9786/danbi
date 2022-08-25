from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Routine, RoutineDay
from .serializers import RoutineSerializer, DaySerializer
from .utils import *



class RoutineViewSet(viewsets.GenericViewSet):
    serializer_class = RoutineSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field     = 'routine_id'

    def get_queryset(self):
        uid = self.request.user.id
        return Routine.objects.filter(account=uid)

    def create(self, request, routine_id=None):
        serializer = RoutineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response_201(serializer.data, "_CREATE")

    def retrieve(self, request, routine_id=None):
        query = self.get_queryset().filter(pk=routine_id).first()
        if not query:
            return Response_404()
        serializer = RoutineSerializer(query)
        return Response_200(serializer.data, "_LOOKUP")

    def update(self, request, routine_id=None):
        instance = self.get_object()                # routine 객체
        serializer = RoutineSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response_200(serializer.data, "_UPDATE")
        else:
            return Response_400()
                
    def destroy(self, request, routine_id=None):
        query = self.get_queryset().filter(pk=routine_id)
        if not query:
            return Response_404()
        query.delete()
        return Response_200(action="_DELETE")

    def list(self, request):
        queryset = self.get_queryset().all()
        if not queryset:
            return Response_404()
        serializer = RoutineSerializer(queryset, many=True)
        return Response_200(serializer.data, "_LOOKUP", "ROUTINES")

    @action(detail=False, methods=["GET"])
    def days(self, request):
        queryset = self.get_queryset().all()
        if not queryset:
           return Response_404('DAY')
        date = request.GET.get('date', 'None') 
        _date = convert_day(date) if is_valid_date(date) else convert_day(get_today()) 

        day_list = []
        for query in queryset:
            r_id = query.routine_id
            day_obj = RoutineDay.objects.filter(day=_date, id=r_id).first()
            if not day_obj:
                continue
            day_list.append(day_obj)

        serializer = DaySerializer(day_list, many=True)
        return Response_200(serializer.data, "_LOOKUP", "DAYS")