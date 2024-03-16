from django.db import models
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User

# Create your models here.

class Subscriber(models.Model):
    email           = models.EmailField(max_length=100, null=True, unique=True, verbose_name='Email Address')
    slug            = AutoSlugField(populate_from='email', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.email}'
    
class SendMessage(models.Model):
    subject         = models.CharField(max_length=100, null=True, verbose_name='Subject')
    slug            = AutoSlugField(populate_from='subject', unique_with='date_created', unique=True, editable=False)
    body            = RichTextUploadingField(verbose_name='Message Content')
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.subject}'


class Mails(models.Model):
    sender          = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='sender', verbose_name='Sender')
    recipient       = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='recipient', verbose_name='Receiver')
    slug            = AutoSlugField(populate_from='subject', unique_with='date_created', unique=True, editable=False)
    subject         = models.CharField(max_length=70, null=True, verbose_name='Subject')
    body            = RichTextUploadingField(verbose_name='Message Content')
    is_read         = models.BooleanField(blank=True, null=True, default=False, verbose_name='Is Read')
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, null=True)
    
    
    class Meta:
        ordering = ['is_read']
        verbose_name = 'Mail'
        verbose_name_plural = 'Mails'
    
    
    def __str__(self):
        return f'{self.subject}'