from django.db import models
from backend.validators import image_extension
from PIL import Image
from account.models import User
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

# Create your models here.
TITLE = [
    ('', 'Select Title'),
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Alhaji', 'Alhaji'),
    ('Alhaja', 'Alhaja'),
    ('Others', 'Others'),
]

MARITAL = [
    ('', 'Select Status'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Others', 'Others'),
]

GENDER = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

RELIGION = [
    ('', 'Select Religion'),
    ('Christianity', 'Christianity'),
    ('Islam', 'Islam'),
    ('Traditional', 'Traditional'),
    ('Others', 'Others'),
]


class Profile(models.Model):
    user            = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    slug            = AutoSlugField(populate_from='user', unique_with='date_created', unique=True, editable=False)
    title           = models.CharField(max_length=15, choices=TITLE, null=True, blank=True, help_text='Select Title', verbose_name='Title:')
    middle_name     = models.CharField(max_length=100, null=True, blank=True, help_text='Enter Middle Name', verbose_name='Middle Name:')
    date_of_birth   = models.DateField(blank=True, null=True, help_text='Select Date of Birth', verbose_name='Date of Birth:')
    phone           = PhoneNumberField(max_length=17, help_text='Phone Number Format: 09031926026', blank=True, null=True, verbose_name='Phone Number')
    spousephone     = PhoneNumberField(max_length=17, blank=True, null=True, verbose_name='Spouse Phone Number')
    gender          = models.CharField(max_length=15, choices=GENDER, null=True, blank=True, help_text='Select Gender', verbose_name='Gender:')
    marital         = models.CharField(max_length=15, choices=MARITAL, null=True, blank=True, help_text='Select Marital', verbose_name='Marital:')
    religion        = models.CharField(max_length=15, choices=RELIGION, null=True, blank=True, help_text='Select Religion', verbose_name='Religion:')
    busstop         = models.CharField(max_length=255, null=True, blank=True, help_text='Enter Bus Stop', verbose_name='Bus Stop:')
    address         = models.CharField(max_length=255, null=True, blank=True, help_text='Enter Residential Address', verbose_name='Residential Address:')
    occupation      = models.CharField(max_length=255, null=True, blank=True, help_text='Enter Occupation', verbose_name='Occupation:')
    office          = models.CharField(max_length=255, null=True, blank=True, help_text='Enter Office Address', verbose_name='Office Address:')
    country         = CountryField(multiple=False, blank_label="Select Country")
    state           = models.CharField(max_length=255, null=True, blank=True, help_text='Enter State of Origin', verbose_name='State:')
    lga             = models.CharField(max_length=255, null=True, blank=True, help_text='Enter L.G.A. of Origin', verbose_name='Local Government Area:')
    home            = models.CharField(max_length=255, null=True, blank=True, help_text='Enter Home Town', verbose_name='Home Town:')
    bio             = RichTextUploadingField(null=True, blank=True, verbose_name='Biography Content')
    facebook        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Facebook URL', verbose_name='Facebook URL:')
    twitter         = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Twitter URL', verbose_name='Twitter URL:')
    instagram       = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Instagram URL', verbose_name='Instagram URL:')
    linkedin        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Linkedin URL', verbose_name='Linkedin URL:')
    whatsapp        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter WhatsApp URL', verbose_name='WhatsApp URL:')
    youtube         = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Youtube URL', verbose_name='Youtube URL:')
    image           = models.FileField(upload_to='backend/profile/', help_text='Passport format should be; .png, .jpeg, .jpg', validators=([image_extension]), default='images/profile.png', verbose_name='Applicant Passport:')
    date_created    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated    = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
