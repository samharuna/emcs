from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField

# Create your models here.

class User(AbstractUser):
    username    = models.CharField(max_length=100, unique=True, verbose_name='Username')
    slug        = AutoSlugField(populate_from='username', unique=True, editable=False)
    email       = models.EmailField(max_length=100, unique=True, verbose_name='Email Address')
    first_name  = models.CharField(max_length=100, verbose_name='First Name')
    last_name   = models.CharField(max_length=100, verbose_name='Last Name')
    
    def __str__(self):
        return f'{self.username}'
    
    def clean(self):
        self.username = self.username.lower()
        self.email = self.email.lower()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        return super().clean()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']