from django.contrib import admin
from core.models import User, Room, Topic, Message

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
