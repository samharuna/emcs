from django.contrib import admin
from newsletter.models import Subscriber, SendMessage, Mails

# Register your models here.

admin.site.register(Subscriber)
admin.site.register(SendMessage)
admin.site.register(Mails)
