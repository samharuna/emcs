from django.db import models
from backend.validators import image_extension
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from autoslug import AutoSlugField
from account.models import User
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.conf import settings
import requests

# Create your models here.



# IDENTIFICATION
IDENTITY = [
    ('', 'Select Means of Identification'),
    ('Voter Card', 'Voter Card'),
    ('NIMC Card', 'NIMC Card'),
    ('Passport', 'Passport'),
    ('Driver License', 'Driver License'),
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
    ('Son', 'Son'),
    ('Daughter', 'Daughter'),
]

MARITAL = [
    ('', 'Select Marital Status'),
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


# START OF DURATION
class LoanDuration(models.Model):
    name                = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='Loan Duration:')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Loan Duration'
        verbose_name_plural = 'Loan Duration'
    
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
    purpose             = models.TextField(verbose_name='Purpose of Loan')
    amount              = models.IntegerField(verbose_name='Loan Principal Amount in (Figure)')
    words               = models.CharField(max_length=255, null=True, verbose_name='Loan Principal Amount in (Words)')
    plan                = models.CharField(max_length=20, null=True, choices=LOANPLAN, verbose_name='Loan Plan')
    duration            = models.ForeignKey(LoanDuration, on_delete=models.PROTECT, verbose_name='Loan Duration (Weeks)')
    interest            = models.IntegerField(default=0, blank=True, null=True, verbose_name='Loan Interest')
    percent             = models.IntegerField(default=10, blank=True, null=True, verbose_name='Loan Percentage')
    status              = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    guarantor           = models.CharField(max_length=255, null=True, verbose_name='Guarantor Full Name')
    guarantor_mobile    = PhoneNumberField(max_length=17, blank=True, null=True, verbose_name='Guarantor Phone Number')
    guarantor_email     = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Guarantor Email Address')
    guarantor_occupation= models.CharField(max_length=255, null=True, verbose_name='Guarantor Occupation')
    guarantor_address   = models.CharField(max_length=255, null=True, verbose_name='Guarantor Residential Address')
    guarantor_office    = models.CharField(max_length=255, null=True, verbose_name='Guarantor Office Address')
    guarantor_gender    = models.CharField(max_length=10, null=True, choices=GENDER, verbose_name='Gender')
    guarantor_marital   = models.CharField(max_length=20, null=True, choices=MARITAL, verbose_name='Marital Status')
    guarantor_country   = CountryField(multiple=False, blank_label="Select Country")
    guarantor_state     = models.CharField(max_length=150, null=True, verbose_name='State of Origin')
    guarantor_lga       = models.CharField(max_length=150, null=True, verbose_name='LGA of Origin')
    guarantor_home      = models.CharField(max_length=150, null=True, verbose_name='Home Town')
    picture             = models.ImageField(upload_to='applications/passport/', help_text='Passport format should be; .png, .jpeg, .jpg', validators=([image_extension]), default='images/profile.png', verbose_name='Guarantor Passport:')
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
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'
        
    @property
    def get_interest(self):
        interest = self.percent/100 * self.amount
        return interest
    
    @property
    def get_total_amount(self):
        total_amount = self.percent/100 * self.amount + self.amount
        return total_amount

    @property
    def get_repayment(self):
        repayment = self.get_total_amount / int(self.duration.name)
        return repayment
    
    
    def save(self, *args, **kwargs):
        self.interest = self.get_interest
        self.total_amount = self.get_total_amount
        self.repayment = self.get_repayment
  
        if self.status == 1:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.applicant.profile.phone}",
                    "from": "Empower MCS",
                    "sms": f"Dear {self.applicant.first_name}, the fund of #{self.amount} you applied with EMCS has been APPROVED.\nPlease Submit the signed Form & Payment Advice before CASH DISBURSEMENT.",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": settings.API_KEY,
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        elif self.status == 2:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.applicant.profile.phone}",
                    "from": "Empower MCS",
                    "sms": f"We are Sorry {self.applicant.first_name}, the fund you applied with EMCS has been DISAPPROVED.",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": settings.API_KEY, 
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
    
        super(Loan, self).save(*args, **kwargs)
        
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
    

    def __str__(self):
        return f'{self.applicant.username} applied for Loan of #{self.amount} at {self.percent}% for {self.duration} Weeks'
# END OF LOAN

# START OF INVESTMENT DURATION
class InvestmentDuration(models.Model):
    name                = models.CharField(max_length=100, null=True, unique=True, verbose_name='Investment Duration')
    slug                = AutoSlugField(populate_from='name', unique=True)
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Investment Duration'
        verbose_name_plural = 'Investment Duration'
    
    def __str__(self):
        return f'{self.name}'
# END OF INVESTMENT DURATION

# START OF INVESTMENT
class Investment(models.Model):
    investor            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor')
    slug                = AutoSlugField(populate_from='investor', unique=True)
    percent             = models.IntegerField(default=18, blank=True, null=True, verbose_name='Investment Percentage')
    interest            = models.IntegerField(default=0, blank=True, null=True, verbose_name='Investment Interest')
    amount              = models.IntegerField(default=0, verbose_name='Amount in Figure')
    words               = models.CharField(max_length=255, null=True, verbose_name='Amount in Words')
    duration            = models.ForeignKey(InvestmentDuration, on_delete=models.PROTECT, verbose_name='Investment Duration')
    total_amount        = models.IntegerField(default=0, blank=True, verbose_name='Total Amount')
    status              = models.IntegerField(default=Status.PENDING, choices=Status.choices, verbose_name='Status')
    next_kin            = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Full Name')
    next_kin_mobile     = PhoneNumberField(max_length=17, blank=True, null=True, verbose_name='Next of Kin Phone Number')
    next_kin_email      = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Next of Kin Email Address')
    next_kin_occupation = models.CharField(max_length=255, blank=True, null=True,  verbose_name='Guarantor Occupation')
    next_kin_address    = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Residential Address')
    next_kin_office     = models.CharField(max_length=255, null=True, verbose_name='Next of Kin Office Address')
    relationship        = models.CharField(max_length=20, null=True, choices=RELATIONSHIP, verbose_name='Next of Kin Relationship')
    picture             = models.ImageField(upload_to='passport', help_text='Passport format should be; .png, .jpeg, .jpg', default='images/profile.png', validators=([image_extension]), verbose_name='Next of Kin Passport')
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
    def get_investment_interest(self):
        interest = self.percent / 100 * self.amount / 2
        return interest
    
    @property
    def get_total_investment(self):
        total_amount = self.percent / 100 * self.amount / 2 + self.amount
        return total_amount
    
    @property
    def get_investment_repayment(self):
        repayment = self.get_total_investment / int(self.duration.name)
        return repayment
    

    def save(self, *args, **kwargs):
        self.interest       = self.get_investment_interest
        self.total_amount   = self.get_total_investment
        self.repayment      = self.get_investment_repayment
    
        if self.status == 1:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.investor.profile.phone}",
                    "from": "Empower MCS",
                    "sms": f"Dear {self.investor.first_name}, the investment of #{self.amount} you applied with EMCS has been APPROVED.\nWe will send your CONFIRMATION Advice to you as soon as possible",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": settings.API_KEY, 
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
        elif self.status == 2:
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                    "to": f"{self.investor.profile.phone}",
                    "from": "Empower MCS",
                    "sms": f"We are Sorry {self.investor.first_name}, the investment you applied with EMCS has been DISAPPROVED",
                    "type": "plain",
                    "channel": "generic",
                    "api_key": settings.API_KEY,
                }
            headers = {'Content-Type': 'application/json',}
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)
            
        super(Investment, self).save(*args, **kwargs)
        
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)

    
    def __str__(self):
        return f'{self.investor.username} applied for Investment of #{self.amount} at {self.percent}% for {self.duration} Months'
# END OF INVESTMENT

# START OF REQUIREMENTS
class Requirement(models.Model):
    title               = models.CharField(max_length=120, blank=True, null=True, verbose_name='Service Title')
    slug                = AutoSlugField(populate_from='title', unique=True)
    body                = RichTextUploadingField(verbose_name='Service Content', null=True, blank=True)
    link                = models.CharField(max_length=120, blank=True, null=True, verbose_name='Service Link')
    link_caption        = models.CharField(max_length=120, blank=True, null=True, verbose_name='Link Caption')
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
# START OF REQUIREMENTS