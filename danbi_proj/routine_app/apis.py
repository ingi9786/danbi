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
        # serializer = RoutineCreateSerializer(data=request.data)
        serializer = RoutineSerializer(data = request.data)
        if serializer.is_valid():
            # user_id = request.user.id
            # serializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get test >  http://127.0.0.1:8000/rou 
    def get(self, request, format=None):
        r = Routine.objects.filter(routine_id=1)
        print("+++++++++++++++++++++++++++")
        serializer = RoutineSerializer(r, many=True)
        return Response(serializer.data)