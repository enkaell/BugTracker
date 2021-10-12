from django.shortcuts import render
import os.path
from rest_framework.views import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny

class AuthPageView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        #Auth
        serializer = UsersSerializer(data = request.data)
        if Users.objects.filter(username = request.data['username']).exists():
            if Users.objects.filter(password = request.data['password']).exists():
                user = request.user
                serializer.is_valid()
                token, created = Token.objects.get_or_create(user= Users.objects.filter(username = request.data['username']).values_list('id', flat=True).first())
                return Response(token.key)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid(raise_exception=True):
                acc = serializer.save()
                token = Token.objects.get(user=acc)
            return Response({'username': serializer.data['username'],'password': serializer.data['password'],'token': token.key})

class ManagePageView(APIView):
    def get(self, request):
        if request.user.role == 'Менеджер':
            return Response (UsersSerializer(Users.objects.all(), many= True).data)
        else:
            return Response({'response': "You don't have permissions"})
    def put(self, request):
        if request.user.role == 'Менеджер':
            if Users.objects.filter(username = request.data['username']).exists():
                user_to_update = Users.objects.get(username = request.data['username'])
                user_to_update.password = request.data['password']
                user_to_update.role = request.data['role']
                user_to_update.save()
                return Response(request.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'response': "You don't have permissions"})


class AllTasksPageView(APIView):

    def get(self, request):
        return Response(TaskSerializer(Tasks.objects.all(), many= True).data,)

    def post(self, request):
        k = {}
        serializer = TaskSerializer(data = request.data)
        serializer.is_valid()
        serializer.validated_data['creator'] = request.user
        serializer.save()
        return Response({
    "tittle": serializer.data['tittle'],
    "type": serializer.data['type'],
    "priority": serializer.data['priority'],
    "text": serializer.data['text'],
    "status": serializer.data['status'],
    "executor": serializer.data['executor'],
    "creator": str(request.user),
})

    def put(self, request):
            if Tasks.objects.filter(tittle = request.data['tittle']).exists():
                task_to_update = Tasks.objects.get(tittle = request.data['tittle'])
                task_to_update.type = request.data['type']
                task_to_update.priority = request.data['priority']
                task_to_update.executor = request.data['executor']
                task_to_update.text = request.data['text']
                task_to_update.status = request.data['status']
                task_to_update.save()

                return Response({
    "tittle": request.data['tittle'],
    "type": request.data['type'],
    "priority": request.data['priority'],
    "text": request.data['text'],
    "status": request.data['status'],
    "executor": request.data['executor'],
    "creator": str(request.user),
})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.role == 'Менеджер':
            task = Tasks.objects.get(tittle = request.data['tittle'])
            task.delete()
            return Response(request.data)
        else:
            return Response({'response': "You don't have permissions"})

class TaskPageView(APIView):
        def get(self, request, pk):
            return Response(AllTasksSerializer(Tasks.objects.get(id = pk)).data)

