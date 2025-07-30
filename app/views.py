from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Person
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class Register(APIView):
    def post(self,request,format=None):
        try:
            data = request.data.get('data')
            user = User(username=data['username'],password=make_password(data['password']))
            user.save()
            datas = Person.objects.create(
                user_id = user,
                Name = data['name'],
                Age = data['age'],
                Phone = data['phone']
            )
            datas.save()
            data1={"status":1}
            return JsonResponse(data1,safe=False)
        
        except Exception as e:
            print(e)
            data1={"status":0}
            return JsonResponse(data1,safe=False)
            


class Profile_user(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            data = Person.objects.get(user_id = user.id)

            datas = {
                "name":data.Name,
                "age":data.Age,
                "phone":data.Phone,
                "username":data.user_id.username
            }
            return JsonResponse({"status":1,"data":datas},safe=False)

        except Person.DoesNotExist:
            return JsonResponse({"status":0,"error":"User not found"},safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({"status":0,"error":"error"},safe=False)

    