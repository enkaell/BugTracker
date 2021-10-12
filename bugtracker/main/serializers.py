from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'role']


class AllTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['tittle', 'type', 'priority', 'text', 'status', 'executor']