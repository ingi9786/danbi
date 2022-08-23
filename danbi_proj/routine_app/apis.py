from .models import Routine, RoutineDay, RoutineResult
from .serializers import RoutineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RoutinetList(APIView):
    """
    List all routines, or create a new routine.
    """
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        # user_id = request.user.id
        user_id = 10
        serializer = RoutineSerializer(data=request.data) #, context={"user_id":user_id}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get test >  http://127.0.0.1:8000/rou 
    def get(self, request, format=None):
        r = Routine.objects.filter(routine_id=1)
        serializer = RoutineSerializer(r, many=True)
        return Response(serializer.data)
    

# 다 account_id는 있어야함. 
# routine 생성 > routine + days 보내서  routine_id를 응답
# routine 조회 > routine_id 보내서 > routine + days 응답
# routines 조회 > routine_id + 날짜(오늘) routine+rreslt+day?
# routine 수정 > 변경 원하는 필드를 입력 받고 > routine_id를 응답
# routine 삭제  > routine_id > routine, routine_result(is_del True) and days는 삭제. 

# 나의 전체 일정보기: account_id >> 모든 routine들 + days
# 나의 오늘 일정보기: ac_id + 날짜 >> 날짜에 해당되는 routine들 + result
