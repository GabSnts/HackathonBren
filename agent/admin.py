from django.contrib import admin
from agent.models import Conversation

class Admin(admin.ModelAdmin):
    list_display =[
                ]

admin.site.register(Conversation, Admin)