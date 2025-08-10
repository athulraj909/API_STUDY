from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Person,ChatRoom,Message
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .serializers import PersonSerializer,ChatRoomSerializer,MessageSerializer
from rest_framework import status




class Register(APIView):
    def post(self,request,format=None):
        try:
            serializer = PersonSerializer(data=request.data.get('data'))
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": 1}, status=status.HTTP_201_CREATED)
            return JsonResponse({"status": 0, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse({"status": 0, "error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class Profile_user(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            person = Person.objects.get(user_id=request.user)
            serializer = PersonSerializer(person)
            return JsonResponse({"status": 1, "data": serializer.data})
        except Person.DoesNotExist:
            return JsonResponse({"status": 0, "error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return JsonResponse({"status": 0, "error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

