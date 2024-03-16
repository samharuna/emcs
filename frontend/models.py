from collections.abc import Iterable
from typing import Any
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from autoslug import AutoSlugField
from account.models import User
from backend.models import Profile
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Status(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVE = 1, 'Approved'
    DISAPPROVE = 2, 'Disapproved'

class Tags(models.Model):
    name            = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tag Title:')
    slug            = AutoSlugField(populate_from='name', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return f"{self.name}"
    
class Category(models.Model):
    tags            = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='tags', null=True, verbose_name='Category Tag:')
    name            = models.CharField(max_length=100, null=True, blank=True, verbose_name='Category Title:')
    slug            = AutoSlugField(populate_from='name', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return f"{self.name}"

class About(models.Model):
    description     = models.CharField(max_length=200, blank=True, null=True, verbose_name='About Description:')
    slug            = AutoSlugField(populate_from='description', unique_with='date_created', unique=True, editable=False)
    body            = RichTextUploadingField(verbose_name='About Content')
    image           = models.ImageField(upload_to='frontend/about/', default='images/placeholder.png', blank=True, null=True, verbose_name='About Image:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.description}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
        
    
class Services(models.Model):
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories', null=True, verbose_name='Service Category:')
    slug            = AutoSlugField(populate_from='category', unique_with='date_created', unique=True, editable=False)
    description     = models.CharField(max_length=255, blank=True, null=True, verbose_name='Service Description:')
    body            = RichTextUploadingField(verbose_name='Service Content')
    image           = models.ImageField(upload_to='frontend/services/', default='images/placeholder.png', blank=True, null=True, verbose_name='Service Image:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
        
    class Meta:
        verbose_name_plural = "Services"
    
    def __str__(self):
        return f"{self.category}"
    
    def delete(self):
        self.image.delete()
        return super().delete()

    def save(self, *args, **kwargs):
        return super(Services, self).save(*args, **kwargs)
    
class Blog(models.Model):
    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', null=True, verbose_name='Blog Author:')
    image           = models.ImageField(upload_to='frontend/blog/', default='images/placeholder.png', blank=True, null=True, verbose_name='Blog Image:')
    title           = models.CharField(max_length=100, blank=True, null=True, verbose_name='Blog Title:')
    slug            = AutoSlugField(populate_from='author', unique_with='date_created', unique=True, editable=False)
    description     = models.CharField(max_length=200, blank=True, null=True, verbose_name='Blog Description:')
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, verbose_name='Blog Category:')
    body            = RichTextUploadingField(verbose_name='Blog Content')
    status          = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)
        

class Testimonial(models.Model):
    image           = models.ImageField(upload_to='frontend/testimonial/', default='images/placeholder.png', blank=True, null=True, verbose_name='Image:')
    name            = models.CharField(max_length=100, null=True, verbose_name='Full Name:')
    slug            = AutoSlugField(populate_from='name', unique_with='date_created', unique=True, editable=False)
    occupation      = models.CharField(max_length=200, blank=True, null=True, verbose_name='Occupation:')
    body            = RichTextUploadingField(verbose_name='Testimonial Content')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Testimonial, self).save(*args, **kwargs)
    
class Contact(models.Model):
    name            = models.CharField(max_length=100, null=True, verbose_name='Full Name:')
    email           = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Email Address')
    slug            = AutoSlugField(populate_from='name', unique_with='date_created', unique=True, editable=False)
    subject         = models.CharField(max_length=200, blank=True, null=True, verbose_name='Contact Subject:')
    body            = models.TextField(blank=True, null=True, verbose_name='Contact Body')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"
    
class Details(models.Model):
    address         = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detail Address:')
    slug            = AutoSlugField(populate_from='address', unique_with='date_created', unique=True, editable=False)
    description     = models.CharField(max_length=200, null=True, verbose_name='Detail Description:')
    branch          = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detail Branch:')
    starts          = models.CharField(max_length=20, blank=True, null=True, verbose_name='Resumption Time:')
    closes          = models.CharField(max_length=20, blank=True, null=True, verbose_name='Closing Time:')
    phone           = PhoneNumberField(max_length=17, null=True, blank=True, verbose_name='Phone Number')
    mobile          = PhoneNumberField(max_length=17, null=True, blank=True, verbose_name='Mobile Number')
    email           = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Office Email Address')
    
    direction       = models.URLField(max_length=500, blank=True, null=True, verbose_name='Direction Map URL:')
    facebook        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Facebook URL', verbose_name='Facebook URL:')
    twitter         = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Twitter URL', verbose_name='Twitter URL:')
    
    instagram       = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Instagram URL', verbose_name='Instagram URL:')
    linkedin        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Linkedin URL', verbose_name='Linkedin URL:')
    whatsapp        = models.URLField(max_length=500, blank=True, null=True, help_text='Enter WhatsApp URL', verbose_name='WhatsApp URL:')
    youtube         = models.URLField(max_length=500, blank=True, null=True, help_text='Enter Youtube URL', verbose_name='Youtube URL:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Details"
    
    def __str__(self):
        return f"{self.address}"
    
class Advert(models.Model):
    title           = models.CharField(max_length=100, blank=True, null=True, verbose_name='Advert Title:')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    image           = models.ImageField(upload_to='frontend/adverts/', default='images/placeholder.png', blank=True, null=True, verbose_name='Advert Image:')
    advert_url      = models.URLField(max_length=255, blank=True, null=True, verbose_name='Advert URL:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Advert, self).save(*args, **kwargs)
    
class Statement(models.Model):
    title           = models.CharField(max_length=100, blank=True, null=True, verbose_name='Statement Title:')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    body            = RichTextUploadingField(verbose_name='Statement Content')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
class Career(models.Model):
    position        = models.CharField(max_length=100, blank=True, null=True, verbose_name='Career Position:')
    slug            = AutoSlugField(populate_from='position', unique_with='date_created', unique=True, editable=False)
    description     = models.CharField(max_length=200, blank=True, null=True, verbose_name='Career Description:')
    body            = RichTextUploadingField(verbose_name='Career Content')
    image           = models.ImageField(upload_to='frontend/careers/', default='images/placeholder.png', blank=True, null=True, verbose_name='Career Image:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.position}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Career, self).save(*args, **kwargs)

class News(models.Model):
    title           = models.CharField(max_length=255, null=True, blank=True, verbose_name='News Title:')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "News"
    
    def __str__(self):
        return f"{self.title}"
    

class Faq(models.Model):
    title           = models.CharField(max_length=140, null=True, blank=True, verbose_name='FAQ Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    body            = RichTextUploadingField(verbose_name='FAQ Content:')
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Privacy(models.Model):
    title           = models.CharField(max_length=110, null=True, blank=True, verbose_name='Privacy Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    body            = RichTextUploadingField(verbose_name='Privacy Content:')
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    
class Header(models.Model):
    title           = models.CharField(max_length=100, blank=True, null=True, verbose_name='Header Title:')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    image           = models.ImageField(upload_to='frontend/header/', default='images/placeholder.png', blank=True, null=True, verbose_name='Header Image:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Header, self).save(*args, **kwargs)
        

class Footer(models.Model):
    title           = models.CharField(max_length=100, blank=True, null=True, verbose_name='Footer Title:')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    image           = models.ImageField(upload_to='frontend/footer/', default='images/placeholder.png', blank=True, null=True, verbose_name='Footer Image:')
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated    = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
    def delete(self):
        self.image.delete()
        return super().delete()
    
    def save(self, *args, **kwargs):
        super(Footer, self).save(*args, **kwargs)
        
        
class ServiceHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
class FAQHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='FAQ Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
class TestimonialHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='Testimonial Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
class AboutHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='About Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    
class ContactHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='Contact Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class CareerHeader(models.Model):
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='Career Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
class Steps(models.Model):
    serial_number   = models.CharField(max_length=10,  null=True, blank=True, verbose_name='Serial Number')
    title           = models.CharField(max_length=200, null=True, blank=True, verbose_name='Loan Steps Title')
    slug            = AutoSlugField(populate_from='title', unique_with='date_created', unique=True, editable=False)
    description     = models.CharField(max_length=200, null=True, blank=True, verbose_name='Loan Steps Description')
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Step"
        verbose_name_plural = "Steps"

    def __str__(self):
        return f'{self.title}'
        


