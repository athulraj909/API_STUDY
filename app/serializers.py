from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person,ChatRoom,Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = User.objects.make_random_password()
        return User.objects.create_user(**validated_data)


class PersonSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = Person
        fields = ['user_id', 'Name', 'Age', 'Phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user_id')
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password']
        )
        return Person.objects.create(user_id=user, **validated_data)


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    

