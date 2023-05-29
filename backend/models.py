from django.db import models
from autoslug import AutoSlugField
import uuid
from frontend.models import Occupation
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# Create your models here.
TITLE = [
    ('', 'Select Title'),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Alhaji', 'Alhaji'),
    ('Alhaja', 'Alhaja'),
]

RELIGION = [
    ('', 'Select Religion'),
    ('Christianity', 'Christianity'),
    ('Islam', 'Islam'),
    ('Traditional', 'Traditional'),
    ('Others', 'Others'),
]

GENDER = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
]

COUNTRY = [
    ('Nigeria', 'Nigeria'),
]

IDENTITY = [
    ('', 'Select Means of Identification'),
    ('Voter Card', 'Voter Card'),
    ('NIMC Card', 'NIMC Card'),
    ('Passport', 'Passport'),
    ('Driver Licence', 'Driver Licence'),
]

MARITAL = [
    ('', 'Select Marital Status'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
]


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    slug            = AutoSlugField(populate_from='user', unique=True)
    title           = models.CharField(max_length=10, null=True, choices=TITLE, verbose_name='Title')
    middlename      = models.CharField(max_length=50, null=True, blank=True, verbose_name='Middle Name')
    dob             = models.DateField(null=True)
    religion        = models.CharField(max_length=20, null=True, choices=RELIGION, verbose_name='Religion')
    gender          = models.CharField(max_length=10, null=True, choices=GENDER, verbose_name='Gender')
    marital         = models.CharField(max_length=20, null=True, choices=MARITAL, verbose_name='Marital Status')
    phonenumber     = PhoneNumberField(blank=True, verbose_name="Phone Number")
    occupation      = models.ForeignKey(Occupation, null=True, on_delete=models.CASCADE, verbose_name='Occupation')
    address         = models.CharField(max_length=255, null=True, verbose_name="Residential Address")
    busstop         = models.CharField(max_length=255, null=True, verbose_name='Nearest Bus Stop')
    office          = models.CharField(max_length=255, null=True, verbose_name="Office Address")
    bio             = models.TextField(max_length=300, null=True, blank=True, verbose_name="Biography")
    country         = models.CharField(max_length=10, null=True, choices=COUNTRY, verbose_name='Country')
    state           = models.CharField(max_length=150, null=True, verbose_name='State of Origin')
    lga             = models.CharField(max_length=150, null=True, verbose_name='LGA of Origin')
    home            = models.CharField(max_length=150, null=True, verbose_name='Home Town')
    facebook        = models.URLField(max_length=255, null=True, blank=True, verbose_name='Facebook Link')
    twitter         = models.URLField(max_length=255, null=True, blank=True, verbose_name='Twitter Link')
    instagram       = models.URLField(max_length=255, null=True, blank=True, verbose_name='Instagram Link')
    youtube         = models.URLField(max_length=255, null=True, blank=True, verbose_name='Youtube Link')
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    image           = models.ImageField(upload_to='profile', default='images/profile.png', verbose_name='Applicant Image')

    class Meta:
        ordering = ['user']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 400 or img.height > 400:
            output_size =(400, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Follow(models.Model):
    followed        = models.CharField(max_length=255, null=True, verbose_name='Followed')
    followed_by     = models.CharField(max_length=255, null=True, verbose_name='Followed By')
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.followed_by} started following {self.followed}'