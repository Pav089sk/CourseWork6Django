from django.contrib import admin
from .models import Recipient, Message, Messenger, Attempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'user')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'user')

@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ('message', 'status', 'user', 'start_time')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'attempt_time')

