from django.db import models
import uuid
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password, **kwargs):
        if not username:
            raise ValueError(_('Your must provide a username'))

        if not email:
            raise ValueError(_('User must provide a valid Email Address'))

        if not first_name:
            raise ValueError(_('Your must provide First Name'))
        
        if not last_name:
            raise ValueError(_('Your must provide Last Name'))
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **kwargs,
        )
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.is_active=True
        user.save(using=self._db)
        return user
        
    def create_staff(self, username, email, first_name, last_name, password, **kwargs):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            first_name = first_name, 
            last_name = last_name,
            password = password,
            **kwargs,
            )
        user.is_superuser =False
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password, **kwargs):
        user = self.create_user(
            username=username, 
            email = self.normalize_email(email),
            first_name=first_name, 
            last_name=last_name,
            password = password,
            **kwargs
            )
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length=100, null=True, verbose_name=_('Username'), unique=True)
    email           = models.EmailField(max_length=100, null=True, verbose_name=_('Email Address'), unique=True)
    first_name      = models.CharField(max_length=100, null=True, verbose_name=_('First Name'))
    last_name       = models.CharField(max_length=100, null=True, verbose_name=_('Last Name'))
    is_superuser    = models.BooleanField(default=False, verbose_name=_('Superuser'))
    is_staff        = models.BooleanField(default=False, verbose_name=_('Staff'))
    is_active       = models.BooleanField(default=True, blank=True, verbose_name=_('Active'))
    date_joined     = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
    date_updated    = models.DateTimeField(auto_now=True, verbose_name=_('Date Created'))
    last_login      = models.DateTimeField(auto_now=True, verbose_name=_('Last Login'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()

    
    class Meta:
        ordering = ["username"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}'

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_short_name(self):
        return f'{self.username}'


    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
