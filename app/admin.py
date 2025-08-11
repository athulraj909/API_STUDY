from django.contrib import admin

# Register your models here.
from .models import Person,ChatRoom,Message


admin.site.register(Person)
admin.site.register(ChatRoom)
admin.site.register(Message)