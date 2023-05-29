from django.db import models
import uuid
from autoslug import AutoSlugField
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from twilio.rest import Client
import environ
from pathlib import Path
import requests

#########
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / '.env')
#########

# Create your models here.


class HeaderLogo(models.Model):
    name                = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Company Name')
    image               = models.ImageField(upload_to='logo', default='images/logo.png', verbose_name='Company Logo')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 40 or img.width > 203:
            output_size = (40, 203)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FooterLogo(models.Model):
    name                = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Company Name')
    image               = models.ImageField(upload_to='logo', default='images/emcs.png', verbose_name='Company Logo')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 40 or img.width > 203:
            output_size = (40, 203)
            img.thumbnail(output_size)
            img.save(self.image.path)


# IDENTIFICATION
IDENTITY = [
    ('', 'Select Means of Identification'),
    ('Voter Card', 'Voter Card'),
    ('NIMC Card', 'NIMC Card'),
    ('Passport', 'Passport'),
    ('Driver Licence', 'Driver Licence'),
]

# IDENTIFICATION


# START OF LOAN
LOANPLAN = [
    ('', 'Select Repayment Plan'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
]


RELATIONSHIP = [
    ('', 'Select Relationship'),
    ('Friend', 'Friend'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Uncle', 'Uncle'),
    ('Aunty', 'Aunty'),
]

MARITAL = [
    ('', 'Select Marital Status'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
]

GENDER = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
]

COUNTRY = [
    ('Nigeria', 'Nigeria'),
]

# START OF OCCUPATION
class Occupation(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Staff Position')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
# END OF OCCUPATION

# START OF INTEREST
class LoanInterest(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Loan Interest')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
# END OF INTEREST

# START OF DURATION
class LoanDuration(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Loan Duration')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
# END OF DURATION


class Status(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVE = 1, 'Approved'
    DISAPPROVE = 2, 'Disapproved'

class Loan(models.Model):
    applicant           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    slug                = AutoSlugField(populate_from='applicant', unique=True)
    
    identity            = models.CharField(max_length=20, null=True, choices=IDENTITY, verbose_name='Means of Identification')
    cardissuer          = models.DateField(null=True)
    cardexpiry          = models.DateField(null=True)
    cardnumber          = models.CharField(max_length=20, null=True, verbose_name='ID Card Number')
    bvn                 = models.CharField(max_length=11, null=True, verbose_name='BVN')
    spousephone         = PhoneNumberField(blank=True, verbose_name="Spouse Phone Number")
    
    purpose             = models.TextField(verbose_name='Purpose of Loan')
    amount              = models.IntegerField(verbose_name='Loan Principal Amount in (Figure)')
    words               = models.CharField(max_length=255, null=True, verbose_name='Loan Principal Amount in (Words)')
    plan                = models.CharField(max_length=20, null=True, choices=LOANPLAN, verbose_name='Loan Plan')
    duration            = models.ForeignKey(LoanDuration, on_delete=models.PROTECT, verbose_name='Loan Duration (Weeks)')
    interest            = models.ForeignKey(LoanInterest, on_delete=models.PROTECT, verbose_name='Loan Interest')
    status              = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    guarantor           = models.CharField(max_length=255, null=True, verbose_name='Guarantor Full Name')
    guarantor_mobile    = PhoneNumberField(blank=True, verbose_name='Guarantor Phone Number')
    guarantor_email     = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Guarantor Email Address')
    guarantor_occupation= models.ForeignKey(Occupation, on_delete=models.CASCADE, verbose_name='Guarantor Occupation')
    guarantor_address   = models.CharField(max_length=255, null=True, verbose_name='Guarantor Residential Address')
    guarantor_office    = models.CharField(max_length=255, null=True, verbose_name='Guarantor Office Address')
    guarantor_gender    = models.CharField(max_length=10, null=True, choices=GENDER, verbose_name='Gender')
    guarantor_marital   = models.CharField(max_length=20, null=True, choices=MARITAL, verbose_name='Marital Status')
    guarantor_country   = models.CharField(max_length=10, null=True, choices=COUNTRY, verbose_name='Country')
    guarantor_state     = models.CharField(max_length=150, null=True, verbose_name='State of Origin')
    guarantor_lga       = models.CharField(max_length=150, null=True, verbose_name='LGA of Origin')
    guarantor_home      = models.CharField(max_length=150, null=True, verbose_name='Home Town')
    guarantor_image     = models.ImageField(upload_to='passport', default='images/profile.png', verbose_name='Guarantor Passport')
    
    relationship        = models.CharField(max_length=20, null=True, choices=RELATIONSHIP, verbose_name='Guarantor Relationship')
    years_known         = models.CharField(max_length=20, null=True, verbose_name='Years of relationship with Applicant')

    payment_period      = models.CharField(max_length=266, null=True, blank=True, verbose_name='Payment Period')
    payment_starts      = models.CharField(max_length=266, null=True, blank=True, verbose_name='Payment Starts')
    payment_ends        = models.CharField(max_length=266, null=True, blank=True, verbose_name='Payment Ends')
    repayment           = models.IntegerField(default=0, blank=True, verbose_name='Loan Repayment')
    total_amount        = models.IntegerField(default=0, blank=True, verbose_name='Total Amount')

    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['applicant']
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    @property
    def get_interest(self):
        results = (int(self.interest.name) / 100) * self.amount
        return results

    @property
    def get_total_amount(self):
        results = self.amount + self.get_interest
        return results

    @property
    def get_repayment(self):
        results = self.get_total_amount / int(self.duration.name)
        return results
    
    
    def save(self, *args, **kwargs):
        self.total_amount = self.get_total_amount
        self.repayment = self.get_repayment
        """
        if self.status == 1:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.applicant.profile.phonenumber}",
                    "from": "EMCS",
                    "sms": f"Dear {self.applicant.profile.title} {self.applicant.first_name}, the fund of #{self.amount} you applied with EMCS has been APPROVED, Please PRINT, SIGN, and SUBMIT your PAYMENT ADVICE before FUND DISBURSEMENT",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": env('API_KEY'),  
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        elif self.status == 2:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.applicant.profile.phonenumber}",
                    "from": "EMCS",
                    "sms": f"We are Sorry {self.applicant.profile.title} {self.applicant.first_name}, the fund you applied with EMCS has been DISAPPROVED",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": env('API_KEY'),
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        """
        super(Loan, self).save(*args, **kwargs)
    

    def __str__(self):
        return f'{self.applicant.get_full_name} applied for Loan of #{self.amount} at {self.interest}% for {self.duration} Weeks'
# END OF LOAN


# START OF INVESTMENT INTEREST
class InvestmentInterest(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Investment Interest')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
# END OF INVESTMENT INTEREST

# START OF INVESTMENT DURATION
class InvestmentDuration(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Investment Duration')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'
# END OF INVESTMENT DURATION


# START OF INVESTMENT
class Investment(models.Model):
    investor            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor')
    slug                = AutoSlugField(populate_from='investor', unique=True)
    
    identity            = models.CharField(max_length=20, null=True, choices=IDENTITY, verbose_name='Means of Identification')
    cardissuer          = models.DateField(null=True)
    cardexpiry          = models.DateField(null=True)
    cardnumber          = models.CharField(max_length=20, null=True, verbose_name='ID Card Number')
    bvn                 = models.CharField(max_length=11, null=True, verbose_name='BVN')
    spousephone         = PhoneNumberField(blank=True, verbose_name="Spouse Phone Number")
    
    amount              = models.IntegerField(default=0, verbose_name='Amount in Figure')
    words               = models.CharField(max_length=255, null=True, verbose_name='Amount in Words')
    duration            = models.ForeignKey(InvestmentDuration, on_delete=models.PROTECT, verbose_name='Investment Duration')
    interest            = models.ForeignKey(InvestmentInterest, on_delete=models.PROTECT, verbose_name='Investment Interest')
    status              = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    next_kin            = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Full Name')
    next_kin_mobile     = PhoneNumberField(blank=True, verbose_name='Next of Kin Phone Number')
    next_kin_email      = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Next of Kin Email Address')
    next_kin_occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, verbose_name='Guarantor Occupation')
    next_kin_address    = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Residential Address')
    next_kin_office     = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Office Address')
    relationship        = models.CharField(max_length=20, null=True, choices=RELATIONSHIP, verbose_name='Next of Kin Relationship')
    next_kin_image      = models.ImageField(upload_to='passport', default='images/profile.png', verbose_name='Next of Kin Passport')

    description         = models.CharField(max_length=150, default='Fixed Deposit', null=True, blank=True, verbose_name='Investment Description')
    repayment           = models.IntegerField(default=0, null=True, blank=True,  verbose_name='Investment Repayment')
    investment_starts   = models.CharField(max_length=266, null=True, blank=True, verbose_name='Investment Starts')
    investment_ends     = models.CharField(max_length=266, null=True, blank=True, verbose_name='Investment Ends')
    director_name       = models.CharField(max_length=266, default='Akintola, Omowumi Ajibola', null=True, blank=True, verbose_name='Director Full Name')

    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['investor']
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'
                
    @property
    def investment_interest(self):
        results = (int(self.interest.name)/100) * self.amount
        return results

    @property
    def total_investment_interest(self):
        results = self.investment_interest / 2
        return results

    @property
    def total_investment(self):
        results = self.amount + self.total_investment_interest
        return results

    def save(self, *args, **kwargs):
        self.repayment = self.total_investment
        """
        if self.status == 1:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.investor.profile.phonenumber}",
                    "from": "EMCS",
                    "sms": f"Dear {self.investor.profile.title} {self.investor.first_name}, the investment of #{self.amount} you applied with EMCS has been APPROVED, we will send your CONFIRMATION Letter to you soon",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": env('API_KEY'),  
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        elif self.status == 2:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.investor.profile.phonenumber}",
                    "from": "EMCS",
                    "sms": f"We are Sorry {self.investor.profile.title} {self.investor.first_name}, the investment you applied with EMCS has been DISAPPROVED",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": env('API_KEY'),
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        """
        super(Investment, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.investor.get_full_name} applied for Investment of #{self.amount} at {self.interest}% for {self.duration} Months'
# END OF INVESTMENT


# START OF BLOG POST
class Tags(models.Model):
    name                = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Tags')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    tags                = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Select Tags')
    slug                = AutoSlugField(populate_from='name', unique=True)
    name                = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Category')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'LGA'
        verbose_name_plural = 'LGAs'
    
    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    slug                = AutoSlugField(populate_from='title', unique=True)
    title               = models.CharField(max_length=50, null=True, verbose_name='Post Title')
    description         = models.CharField(max_length=100, null=True, verbose_name='Post Description')
    category            = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Category')
    tags                = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='tags', verbose_name='Tags')
    author              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', verbose_name='Author')
    body                = models.TextField(null=True, verbose_name='Post Content')
    likes               = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name='Likes')
    dislikes            = models.ManyToManyField(User, related_name='dislikes', blank=True, verbose_name='Dislikes')
    status              = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    view_count          = models.IntegerField(default=0)
    last_view           = models.DateTimeField(blank=True, null=True)
    image               = models.ImageField(default='images/placeholder.png', upload_to='posts', verbose_name='Post Image')
    restricted          = models.BooleanField(default=False, blank=True, null=True, verbose_name='Restrict Comment')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 1000 or img.height > 500:
            output_size =(1000, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    @property
    def total_dislikes(self):
        return self.dislikes.count()

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_post(self):
        return self.author.all()

class Comment(models.Model):
    commenter           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter', verbose_name='User')
    post                = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post', verbose_name='Post')
    body                = models.TextField(null=True, verbose_name='Message')
    comment_likes       = models.ManyToManyField(User, related_name='comment_likes', blank=True, verbose_name='Likes')
    comment_dislikes    = models.ManyToManyField(User, related_name='comment_dislikes', blank=True, verbose_name='Dislikes')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['post']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.commenter}'

    @property
    def total_comment(self):
        return self.post.count()

class Reply(models.Model):
    replier             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replier', verbose_name='User')
    comment             = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment', verbose_name='Comment')
    body                = models.TextField(null=True, verbose_name='Reply Content')
    reply_likes         = models.ManyToManyField(User, related_name='reply_likes', blank=True, verbose_name='Likes')
    reply_dislikes      = models.ManyToManyField(User, related_name='reply_dislikes', blank=True, verbose_name='Dislikes')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['comment']
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'{self.replier} - [{self.comment.post}] - {self.body}'
# END OF BLOG POST


# START OF ABOUT
class About(models.Model):
    slug                = AutoSlugField(populate_from='description', unique=True)
    description         = models.CharField(max_length=150, null=True, verbose_name='About Description')
    body                = models.TextField(verbose_name='About Body')
    image               = models.ImageField(default='images/placeholder.png', upload_to='about', verbose_name='About Image')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 900 or img.height > 400:
            output_size = (900, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF ABOUT


# START OF SERVICES
class Title(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Title')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    title               = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name='Service Title')
    slug                = AutoSlugField(populate_from='title', unique=True)
    description         = models.CharField(max_length=150, null=True, verbose_name='Service Description')
    body                = models.TextField(verbose_name='Service Body')
    image               = models.ImageField(default='images/placeholder.png', upload_to='services', verbose_name='Service Image')
    list1               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 1')
    list2               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 2')
    list3               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 3')
    list4               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 4')
    list5               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 5')
    list6               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 6')
    list7               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 7')
    list8               = models.CharField(max_length=200, null=True, blank=True, verbose_name='Service List 8')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 900 or img.height > 400:
            output_size = (900, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF SERVICES


# START OF STATEMENT
class Purpose(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Purpose')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

class Statement(models.Model):
    purpose             = models.ForeignKey(Purpose, on_delete=models.CASCADE, verbose_name='Statement Purpose')
    slug                = AutoSlugField(populate_from='purpose', unique=True)
    body                = models.TextField(max_length=400, verbose_name='Statement Body')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.purpose}'
# END OF STATEMENT


# START OF TEAM
class Team(models.Model):
    team                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team', verbose_name='Team')
    slug                = AutoSlugField(populate_from='team', unique=True)
    description         = models.CharField(max_length=200, null=True,  verbose_name='Team Description')
    body                = models.TextField(verbose_name='Team Body')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.team.get_full_name}'
# END OF TEAM


# START OF TESTIMONY
class Testimony(models.Model):
    occupation          = models.ForeignKey(Occupation, on_delete=models.CASCADE, verbose_name='Testifier Occupation')
    slug                = AutoSlugField(populate_from='occupation', unique=True)
    name                = models.CharField(max_length=100, null=True, verbose_name='Testifier Name')
    body                = models.TextField(max_length=400, verbose_name='Testifier Body')
    image               = models.ImageField(default='images/placeholder.png', upload_to='testimonies', verbose_name='Testifier Image')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.occupation}'

    class Meta:
        ordering = ['occupation']
        verbose_name = 'Testimony'
        verbose_name_plural = 'Testimonies'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 400 or img.height > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF TESTIMONY


# START OF NEWSLETTERS
class Newsletter(models.Model):
    email               = models.EmailField(max_length=100, null=True, verbose_name='Subscriber', unique=True, error_messages={'unique': 'Email Address Exist'})
    slug                = AutoSlugField(populate_from='email', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email}'
# END OF NEWSLETTERS


# START OF MAIL
class Mail(models.Model):
    subject             = models.CharField(max_length=266, null=True, verbose_name='Description')
    slug                = AutoSlugField(populate_from='subject', unique=True)
    body                = models.TextField(verbose_name='Body')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}'
# END OF MAIL


# START OF CAREER
class Career(models.Model):
    position            = models.CharField(max_length=100, null=True, verbose_name='Position')
    slug                = AutoSlugField(populate_from='position', unique=True)
    description         = models.CharField(max_length=200, null=True, blank=True, verbose_name='Description')
    body                = models.TextField(verbose_name='Body')
    image               = models.ImageField(default='images/placeholder.png', upload_to='career', verbose_name='Image')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.position}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 600 or img.height > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF CAREER

# START OF ADVERTS
class Advert(models.Model):
    title               = models.CharField(max_length=100, null=True, verbose_name='Title')
    slug                = AutoSlugField(populate_from='title', unique=True)
    image               = models.ImageField(default='images/placeholder.png', upload_to='advert', verbose_name='Image')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 400 or img.height > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF ADVERTS

# START OF CONTACT
class Contact(models.Model):
    name                = models.CharField(max_length=100, null=True, verbose_name='Full Name')
    email               = models.EmailField(max_length=100, null=True, verbose_name='Email Address')
    slug                = AutoSlugField(populate_from='email', unique=True)
    subject             = models.CharField(max_length=200, null=True, verbose_name='Subject')
    body                = models.TextField(verbose_name='Body')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.email}'
# END OF CONTACT

# START OF CONTACT DETAIL
class ContactDetail(models.Model):
    title               = models.CharField(max_length=100, null=True, verbose_name='Contact Page Title')
    email               = models.EmailField(max_length=100, null=True, verbose_name='Email Address')
    phone               = PhoneNumberField(blank=True, verbose_name='Phone Number')
    mobile              = PhoneNumberField(blank=True, verbose_name='Mobile Number')
    slug                = AutoSlugField(populate_from='email', unique=True)
    address             = models.CharField(max_length=200, null=True, verbose_name='Headquarter Address')
    branch              = models.CharField(max_length=200, null=True, blank=True, verbose_name='Branch Address')
    facebook            = models.URLField(max_length=255, null=True, blank=True, verbose_name='Facebook Link')
    twitter             = models.URLField(max_length=255, null=True, blank=True, verbose_name='Twitter Link')
    instagram           = models.URLField(max_length=255, null=True, blank=True, verbose_name='Instagram Link')
    youtube             = models.URLField(max_length=255, null=True, blank=True, verbose_name='Youtube Link')
    map_url             = models.URLField(max_length=255, null=True, blank=True, verbose_name='Map URL Link')
    work_starts         = models.CharField(max_length=10, null=True, blank=True, verbose_name='Work Starts')
    work_ends           = models.CharField(max_length=10, null=True, blank=True, verbose_name='Work Ends')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email}'
# END OF CONTACT DETAIL

# START OF FAQ
class Faq(models.Model):
    title               = models.CharField(max_length=100, null=True, verbose_name='Title')
    slug                = AutoSlugField(populate_from='title', unique=True)
    body                = models.TextField(blank=True, verbose_name='Body')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
# END OF FAQ


# START OF Gallery
class Event(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Event Title')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

class Gallery(models.Model):
    title               = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Event')
    slug                = AutoSlugField(populate_from='title', unique=True)
    image               = models.ImageField(default='images/placeholder.png', upload_to='advert', verbose_name='Image')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 800 or img.height > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)
# END OF Gallery


