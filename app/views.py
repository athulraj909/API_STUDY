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
        






import google.auth.transport.requests
import google.oauth2.id_token
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class GoogleLogin(APIView):
    def post(self, request):
        try:
            id_token = request.data.get("id_token")
            if not id_token:
                return JsonResponse({"error": "ID token is required"}, status=400)

            # Verify token with Google
            request_adapter = google.auth.transport.requests.Request()
            idinfo = google.oauth2.id_token.verify_oauth2_token(
                id_token, request_adapter, settings.GOOGLE_CLIENT_ID
            )

            # Extract user info
            email = idinfo.get("email")
            name = idinfo.get("name")
            google_id = idinfo.get("sub")

            if not email:
                return JsonResponse({"error": "Invalid token"}, status=400)

            # Generate a random password if creating new user
            random_password = get_random_string(20)

            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "password": random_password
                }
            )

            if created:
                # set usable password (hash it properly)
                user.set_password(random_password)
                user.save()

            # Check if Person exists
            person, _ = Person.objects.get_or_create(user_id=user, defaults={
                "Name": name if name else email,
                "Age": 0,
                "Phone": 0
            })

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "status": 1,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": person.Name
                }
            })

        except ValueError as e:
            return JsonResponse({"error": "Invalid token", "details": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Something went wrong", "details": str(e)}, status=500)
