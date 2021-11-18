from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer, RegisterUserSerializer
from todo.models import Todo
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework.authtoken.models import Token


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({"error": "That username has already been taken. Please choose an other one"}, status=400)

class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({"error": "That username has already been taken. Please choose an other one"}, status=400)

        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": str(token)}, status=201)

class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoListRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoListComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()


