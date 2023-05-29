from django import forms
from phonenumber_field.formfields import PhoneNumberField
from accounts.models import User
from frontend.models import HeaderLogo, FooterLogo, Loan, LoanDuration, LoanInterest, Investment, InvestmentDuration, InvestmentInterest, Post, Tags, Category, Comment, Reply, About, Title, Occupation, Service, Purpose, Statement, Team, Testimony, Newsletter, Mail, Career, Advert, Contact, ContactDetail, Faq, Event, Gallery


class HeaderLogoForm(forms.ModelForm):
    image                   = forms.ImageField(label='Header Logo Image', widget=forms.FileInput(attrs={'class':'form-control', 'type':"file"}))
    name                    = forms.CharField(max_length=100, label='Company Name', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Company Name', 'type':'text'}))
    
    class Meta:
        model = HeaderLogo
        fields = ['image', 'name']
        error_class = 'error'


class FooterLogoForm(forms.ModelForm):
    name                    = forms.CharField(max_length=100, label='Company Name', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Company Name', 'type':'text'}))
    image                   = forms.ImageField(label='Footer Logo Image', widget=forms.FileInput(attrs={'class':'form-control', 'type':"file"}))

    class Meta:
        model = FooterLogo
        fields = ['image', 'name']
        error_class = 'error'


LOANPLAN = [
    ('', 'Select Repayment Plan'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
]

OCCUPATION = [
    ('', 'Select Occupation'),
    ('Trader', 'Trader'),
    ('Civil Servant', 'Civil Servant'),
    ('Public Servant', 'Public Servant'),
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

GENDER = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

COUNTRY = [
    ('Nigeria', 'Nigeria'),
]

MARITAL = [
    ('', 'Select Marital Status'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
]

IDENTITY = [
    ('', 'Select Means of Identification'),
    ('Voter Card', 'Voter Card'),
    ('NIMC Card', 'NIMC Card'),
    ('Passport', 'Passport'),
    ('Driver Licence', 'Driver Licence'),
]


class LoanForm(forms.ModelForm):
    purpose                 = forms.CharField(label='Purpose for seeking Loan', widget=forms.TextInput(attrs={'placeholder':'Purpose for seeking Loan here...', 'type':'text'}))
    
    identity                = forms.ChoiceField(label='Means of Identification:', choices=IDENTITY, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    cardnumber              = forms.CharField(max_length=20, label='ID Card Number:', widget=forms.TextInput(attrs={'placeholder':'Enter ID Card Number here...', 'type':'text'}))
    cardissuer              = forms.DateTimeField(label='ID Card Issuer Date:', widget=forms.DateInput(attrs={'type':'date', 'class':'form-select pt-1'}))
    cardexpiry              = forms.DateTimeField(label='ID Card Expiry Date:', widget=forms.DateInput(attrs={'type':'date', 'class':'form-select pt-1'}))
    bvn                     = forms.CharField(max_length=11, label='BVN:', widget=forms.TextInput(attrs={'placeholder':'Enter BVN here...', 'type':'text'}))
    spousephone             = PhoneNumberField(region='NG', label='Spouse Mobile Number:', help_text='Enter Mobile Number Format: +2347037678697')
    
    amount                  = forms.CharField(label='Amount Applying for in Figure', widget=forms.NumberInput(attrs={'placeholder':'Amount Applying for in Figure here...', 'type':'number'}))
    words                   = forms.CharField(max_length=255, label='Amount Applying for in Words', widget=forms.TextInput(attrs={'placeholder':'Amount Applying for in Words here...', 'type':'text'}))
    duration                = forms.ModelChoiceField(queryset=LoanDuration.objects.all(), empty_label='Select Loan Duration', label='Loan Duration (Weeks)')
    plan                    = forms.ChoiceField(label='Loan Plan', choices=LOANPLAN, widget=forms.Select(attrs={'class':'form-select p-0', 'type':'select'}))
    interest                = forms.ModelChoiceField(queryset=LoanInterest.objects.all(), empty_label='Select Loan Interest', label='Loan Interest')
    guarantor               = forms.CharField(max_length=255, label='Full Name', widget=forms.TextInput(attrs={'placeholder':'Full Name here...', 'type':'text'}))
    guarantor_mobile        = PhoneNumberField(region='NG', label='Mobile Number', help_text='Mobile Number Format: +2347037678697')
    guarantor_email         = forms.EmailField(max_length=255, label='Email Address', widget=forms.TextInput(attrs={'placeholder':'Email Address here...', 'type':'text'}))
    guarantor_occupation    = forms.ModelChoiceField(queryset=Occupation.objects.all(), empty_label='Select Occupation', label='Guarantor Occupation')
    guarantor_address       = forms.CharField(max_length=255, label='Residential Address', widget=forms.TextInput(attrs={'placeholder':'Guarantor Residential Address here...', 'type':'text'}))
    guarantor_office        = forms.CharField(max_length=255, label='Guarantor Office Address', widget=forms.TextInput(attrs={'placeholder':'Guarantor Office Address here...', 'type':'text'}))
    guarantor_gender        = forms.ChoiceField(label='Gender:', choices=GENDER, widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    guarantor_marital       = forms.ChoiceField(label='Marital Status:', choices=MARITAL, widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    relationship            = forms.ChoiceField(label='Relationship with Applicant', choices=RELATIONSHIP, widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    guarantor_country       = forms.ChoiceField(label='Country:', choices=COUNTRY, widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    guarantor_state         = forms.CharField(max_length=150, label='State of Origin:', widget=forms.TextInput(attrs={'placeholder':'State of Origin here...', 'type':'text'}))
    guarantor_lga           = forms.CharField(max_length=150, label='Local Government Area of Origin:', widget=forms.TextInput(attrs={'placeholder':'Enter LGA of Origin here...', 'type':'text'}))
    guarantor_home          = forms.CharField(max_length=150, label='Home Town:', widget=forms.TextInput(attrs={'placeholder':'Enter Home Town here...', 'type':'text'}))
    years_known             = forms.CharField(max_length=20, label='Years of relationship with Applicant:', widget=forms.TextInput(attrs={'placeholder':'Enter Years of relationship with Applicant here...', 'type':'text'}))
    guarantor_image         = forms.ImageField(label='Upload Guarantor Passport', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Loan
        fields = ['purpose', 'amount', 'identity', 'cardnumber', 'cardissuer', 'cardexpiry', 'bvn', 'spousephone', 'words', 'duration', 'plan', 'interest', 'guarantor', 'guarantor_gender', 'guarantor_marital', 'years_known', 'guarantor_mobile', 'guarantor_email', 'guarantor_occupation', 'guarantor_address', 'guarantor_office', 'relationship', 'guarantor_country', 'guarantor_state', 'guarantor_lga', 'guarantor_home', 'guarantor_image']
        error_class = 'error'


class UpdateLoanForm(forms.ModelForm):
    applicant                = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}))
    
    class Meta:
        model = Loan
        fields = ['status', 'applicant', 'guarantor']
        error_class = 'error'


class LoanPaymentForm(forms.ModelForm):
    applicant               = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}))
    amount                  = forms.IntegerField(label='Loan Principal', required=False, widget=forms.NumberInput(attrs={'placeholder':'Enter Loan Principal', 'type':'number', 'readonly':'readonly'}))
    interest                = forms.ModelChoiceField(queryset=LoanInterest.objects.all(), empty_label='Select Loan Interest', label='Loan Interest', required=False, widget=forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}))
    plan                    = forms.ChoiceField(label='Loan Plan',  required=False, choices=LOANPLAN, widget=forms.Select(attrs={'class':'form-select p-0', 'type':'select', 'readonly':'readonly'}))
    payment_period          = forms.CharField(label='Payment Period', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Loan Payment Period', 'type':'text'}))
    payment_starts          = forms.CharField(label='Payment Starts', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Loan Payment Starts Date', 'type':'text'}))
    payment_ends            = forms.CharField(label='Payment Ends', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Loan Payment Maturity Date', 'type':'text'}))
    repayment               = forms.IntegerField(label='Repayment',  required=False, widget=forms.NumberInput(attrs={'placeholder':'Enter Loan Repayment', 'type':'number'}))
    total_amount            = forms.IntegerField(label='Total Amount',  required=False, widget=forms.NumberInput(attrs={'placeholder':'Enter Total Loan Amount', 'type':'number'}))
    
    class Meta:
        model = Loan
        fields = ['applicant', 'amount', 'interest', 'plan', 'status', 'payment_period', 'payment_starts', 'payment_ends', 'repayment', 'total_amount']
        error_class = 'error'


class InvestmentForm(forms.ModelForm):
    amount                  = forms.CharField(label='Amount in Figure', widget=forms.NumberInput(attrs={'placeholder':'Amount you intend to invest in figure here', 'type':'number'}))
    
    identity                = forms.ChoiceField(label='Means of Identification:', choices=IDENTITY, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    cardnumber              = forms.CharField(max_length=20, label='ID Card Number:', widget=forms.TextInput(attrs={'placeholder':'Enter ID Card Number here...', 'type':'text'}))
    cardissuer              = forms.DateTimeField(label='ID Card Issuer Date:', widget=forms.DateInput(attrs={'type':'date', 'class':'form-select pt-1'}))
    cardexpiry              = forms.DateTimeField(label='ID Card Expiry Date:', widget=forms.DateInput(attrs={'type':'date', 'class':'form-select pt-1'}))
    bvn                     = forms.CharField(max_length=11, label='BVN:', widget=forms.TextInput(attrs={'placeholder':'Enter BVN here...', 'type':'text'}))
    spousephone             = PhoneNumberField(region='NG', label='Spouse Mobile Number:', help_text='Enter Mobile Number Format: +2347037678697')
    
    words                   = forms.CharField(max_length=255, label='Amount in Words', widget=forms.TextInput(attrs={'placeholder':'Amount you intend to invest in words here', 'type':'text'}))
    interest                = forms.ModelChoiceField(queryset=InvestmentInterest.objects.all(), empty_label='Select Investment Interest', label='Investment Interest [15%]')
    duration                = forms.ModelChoiceField(queryset=InvestmentDuration.objects.all(), empty_label='Select Investment Duration', label='Investment Duration [6 Months]')
    next_kin                = forms.CharField(max_length=255, label='Next of Kin Full Name', widget=forms.TextInput(attrs={'placeholder':'Next of Kin Full Name here', 'type':'text'}))
    next_kin_mobile         = PhoneNumberField(region='NG', label='Next of Kin Mobile Number', help_text='Enter Mobile Number Format: +2347037678697')
    next_kin_email          = forms.EmailField(max_length=255, label='Next of Kin Email Address', widget=forms.TextInput(attrs={'placeholder':'Next of Kin Email Address here', 'type':'text'}))
    next_kin_occupation     = forms.ModelChoiceField(queryset=Occupation.objects.all(), empty_label='Select Occupation', label='Next of Kin Occupation')
    next_kin_address        = forms.CharField(max_length=255, label='Next of Kin Residential Address', widget=forms.TextInput(attrs={'placeholder':'Next of Kin Residential Address here', 'type':'text'}))
    next_kin_office         = forms.CharField(max_length=255, label='Next of Kin Office Address', widget=forms.TextInput(attrs={'placeholder':'Next of Kin Office Address here', 'type':'text'}))
    relationship            = forms.ChoiceField(label='Next of Kin Relationship', choices=RELATIONSHIP, widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    next_kin_image          = forms.ImageField(label='Upload Next of Kin Passport', widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Investment
        fields = ['amount', 'identity', 'cardnumber', 'cardissuer', 'cardexpiry', 'bvn', 'spousephone', 'words', 'duration', 'interest', 'repayment', 'next_kin', 'next_kin_mobile', 'next_kin_email', 'next_kin_occupation', 'next_kin_address', 'next_kin_office', 'next_kin_image', 'relationship']
        error_class = 'error'


class UpdateInvestmentForm(forms.ModelForm):
    investor                = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}))
    
    class Meta:
        model = Investment
        fields = ['status', 'investor', 'amount']
        error_class = 'error'


class InvestmentPaymentForm(forms.ModelForm):
    investor                = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'form-control', 'readonly':'readonly'}))
    description             = forms.CharField(max_length=150, label='Investment Description', initial='Fixed Deposit', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Investment Description', 'type':'text'}))
    director_name           = forms.CharField(label='Director Full Name', initial='Akintola, Omowumi Ajibola', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Director Full Name', 'type':'text'}))
    interest                = forms.ModelChoiceField(queryset=InvestmentInterest.objects.all(), empty_label='Select Investment Interest', label='Investment Interest')
    duration                = forms.ModelChoiceField(queryset=InvestmentDuration.objects.all(), empty_label='Select Investment Duration', label='Investment Duration')
    repayment               = forms.IntegerField(label='Repayment',  required=False, widget=forms.NumberInput(attrs={'placeholder':'Enter Investment Repayment', 'type':'number'}))
    investment_starts       = forms.CharField(label='Investment Starts', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Investment Starts Date', 'type':'text'}))
    investment_ends         = forms.CharField(label='Investment Ends', required=False, max_length=266, widget=forms.TextInput(attrs={'placeholder':'Enter Investment Ends Date', 'type':'text'}))
    
    class Meta:
        model = Investment
        fields = ['investor', 'description', 'director_name', 'interest', 'duration', 'repayment', 'investment_starts', 'investment_ends']


class TagsForm(forms.ModelForm):
    name                    = forms.CharField(max_length=100, label='Tags', widget=forms.TextInput(attrs={'placeholder':'Enter Post Tags', 'type':'text'}))
    
    class Meta:
        model = Tags
        fields = ['name']
        error_class = 'error'

class CategoryForm(forms.ModelForm):
    tags                    = forms.ModelChoiceField(queryset=Tags.objects.all(), empty_label='Select Tags')
    name                    = forms.CharField(max_length=100, label='Category', widget=forms.TextInput(attrs={'placeholder':'Enter Post Category', 'type':'text'}))
    
    class Meta:
        model = Category
        fields = ['tags', 'name']
        error_class = 'error'

class PostForm(forms.ModelForm):
    title                   = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder':'Enter Post Title', 'type':'text'}))
    description             = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'Enter Post Description', 'type':'text'}))
    body                    = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Enter Post Content', 'rows':'4', 'type':'textarea'}))
    tags                    = forms.ModelChoiceField(queryset=Tags.objects.all(), empty_label='Select Tags', label='')
    category                = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Category', label='')
    image                   = forms.ImageField(label='Post Image', widget=forms.FileInput())

    class Meta:
        model = Post
        fields = ['image', 'title', 'description', 'tags', 'category', 'body', 'restricted']
        exclude = ['author', 'slug']
        error_class = 'error'

class CommentForm(forms.ModelForm):
    body                    = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Enter Post Comment', 'rows':'4', 'type':'textarea'}))

    class Meta:
        model = Comment
        fields = ['body']
        error_class = 'error'

class ReplyForm(forms.ModelForm):
    body                    = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Reply Comment Here', 'rows':'3', 'type':'textarea'}))

    class Meta:
        model = Reply
        fields = ['body']
        error_class = 'error'

class AboutForm(forms.ModelForm):
    description         = forms.CharField(max_length=150, label='Description', widget=forms.TextInput(attrs={'placeholder':'Enter Description', 'type':'text'}))
    body                = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = About
        fields = ['image', 'description', 'body']
        error_class = 'error'

class TitleForm(forms.ModelForm):
    name                = forms.CharField(max_length=100, label='Title', widget=forms.TextInput(attrs={'placeholder':'Enter Title', 'type':'text'}))
   
    class Meta:
        model = Title
        fields = ['name']
        error_class = 'error'

class ServiceForm(forms.ModelForm):
    title               = forms.ModelChoiceField(queryset=Title.objects.all(), empty_label='Select Title', label='Service Title')
    description         = forms.CharField(max_length=150, label='Description', widget=forms.TextInput(attrs={'placeholder':'Enter Description', 'type':'text'}))
    body                = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    list1               = forms.CharField(max_length=200, label='Requirement List 1', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 1', 'type':'text'}))
    list2               = forms.CharField(max_length=200, label='Requirement List 2', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 2', 'type':'text'}))
    list3               = forms.CharField(max_length=200, label='Requirement List 3', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 3', 'type':'text'}))
    list4               = forms.CharField(max_length=200, label='Requirement List 4', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 4', 'type':'text'}))
    list5               = forms.CharField(max_length=200, label='Requirement List 5', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 5', 'type':'text'}))
    list6               = forms.CharField(max_length=200, label='Requirement List 6', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 6', 'type':'text'}))
    list7               = forms.CharField(max_length=200, label='Requirement List 7', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 7', 'type':'text'}))
    list8               = forms.CharField(max_length=200, label='Requirement List 8', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Service List 8', 'type':'text'}))
   
    class Meta:
        model = Service
        fields = ['image', 'title', 'description', 'body', 'list1', 'list2', 'list3', 'list4', 'list5', 'list6', 'list7', 'list8']
        error_class = 'error'

class PurposeForm(forms.ModelForm):
    name                = forms.CharField(max_length=100, label='Statement Purpose', widget=forms.TextInput(attrs={'placeholder':'Enter Statement Purpose', 'type':'text'}))
    
    class Meta:
        model = Purpose
        fields = ['name']
        error_class = 'error'

class StatementForm(forms.ModelForm):
    purpose             = forms.ModelChoiceField(queryset=Purpose.objects.all(), empty_label='Select Statement Purpose', label='Statement Purpose')
    body                = forms.CharField(max_length=400, label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
   
    class Meta:
        model = Statement
        fields = ['purpose', 'body']
        error_class = 'error'

class TeamForm(forms.ModelForm):
    description         = forms.CharField(max_length=200, label='Description', widget=forms.TextInput(attrs={'placeholder':'Enter Description', 'type':'text'}))
    body                = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))

    class Meta:
        model = Team
        fields = ['description', 'body']
        error_class = 'error'

class TestimonyForm(forms.ModelForm):
    occupation          = forms.ModelChoiceField(queryset=Occupation.objects.all(), empty_label='Select Occupation', label='Occupation')
    name                = forms.CharField(max_length=100, label='Testifier Name', widget=forms.TextInput(attrs={'placeholder':'Enter Testifier Name', 'type':'text'}))
    body                = forms.CharField(max_length=400, label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Testimony
        fields = ['image', 'name', 'occupation', 'body' ]
        error_class = 'error'

class NewsletterForm(forms.ModelForm):
    email               = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'placeholder':'Enter Email Address', 'type':'email'}))
   
    class Meta:
        model = Newsletter
        fields = ['email']
        error_class = 'error'

class OccupationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Profession:', widget=forms.TextInput(attrs={'placeholder': 'Enter Profession', 'type':'text'}))
            
    class Meta:
        model = Occupation
        fields = ['name']
        error_class = 'error'


class MailForm(forms.ModelForm):
    subject             = forms.CharField(max_length=266, label='Subject', widget=forms.TextInput(attrs={'placeholder':'Enter Description', 'type':'text'}))
    body                = forms.CharField(label='Message Content', widget=forms.Textarea(attrs={'placeholder':'Enter Message Content', 'rows':'6', 'type':'textarea'}))
   
    class Meta:
        model = Mail
        fields = ['subject', 'body']
        error_class = 'error'

class CareerForm(forms.ModelForm):
    position            = forms.CharField(max_length=100, label='Position', widget=forms.TextInput(attrs={'placeholder':'Enter Position', 'type':'text'}))
    description         = forms.CharField(max_length=200, required=False, label='Description', widget=forms.TextInput(attrs={'placeholder':'Enter Description', 'type':'text'}))
    body                = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Career
        fields = ['image', 'position', 'description', 'body']
        error_class = 'error'

class AdvertForm(forms.ModelForm):
    title               = forms.CharField(max_length=100, label='Title', widget=forms.TextInput(attrs={'placeholder':'Enter Title', 'type':'text'}))
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Advert
        fields = ['image', 'title']
        error_class = 'error'

class ContactForm(forms.ModelForm):
    name                = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'Enter Full Name', 'class':'form-control form-control-sm', 'type':'text'}))
    email               = forms.EmailField(max_length=100, label='', widget=forms.EmailInput(attrs={'placeholder':'Enter Email Address', 'class':'form-control form-control-sm', 'type':'email'}))
    subject             = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'placeholder':'Enter Subject', 'class':'form-control form-control-sm', 'type':'text'}))
    body                = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Type Message Here', 'rows':'3', 'class':'form-control form-control-sm', 'type':'textarea'}))
   
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'body']
        error_class = 'error'


class ContactDetailForm(forms.ModelForm):
    title               = forms.CharField(max_length=100, label='Contact Page Title:', widget=forms.TextInput(attrs={'placeholder':'Enter Title', 'type':'text'}))
    email               = forms.EmailField(max_length=100, label='Email Address:', widget=forms.EmailInput(attrs={'placeholder':'Enter Email Address', 'type':'email'}))
    phone               = PhoneNumberField(region='NG', label='Mobile Number:', help_text='Enter Mobile Number Format: +2347037678697')
    mobile              = PhoneNumberField(region='NG', label='Phone Number:', help_text='Enter Phone Number Format: +2347037678697')
    address             = forms.CharField(max_length=200, label='Headquarter Address:', widget=forms.TextInput(attrs={'placeholder':'Enter Headquarter Address', 'type':'text'}))
    branch              = forms.CharField(max_length=200, required=False, label='Branch Address:', widget=forms.TextInput(attrs={'placeholder':'Enter Branch Address', 'type':'text'}))
    facebook            = forms.URLField(max_length=255, label='Facebook Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Facebook Link', 'type':'url'}))
    twitter             = forms.URLField(max_length=255, label='Twitter Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Twitter Link', 'type':'url'}))
    instagram           = forms.URLField(max_length=255, label='Instagram Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Instagram Link', 'type':'url'}))
    youtube             = forms.URLField(max_length=255, label='Youtube Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Youtube Link', 'type':'url'}))
    map_url             = forms.URLField(max_length=255, label='Map Url Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Map Link', 'type':'url'}))
    work_starts         = forms.CharField(max_length=10, required=False, label='Work Starts:', widget=forms.TextInput(attrs={'placeholder':'Enter Work Starts', 'type':'text'}))
    work_ends           = forms.CharField(max_length=10, required=False, label='Work End:', widget=forms.TextInput(attrs={'placeholder':'Enter Work Ends', 'type':'text'}))
    
    class Meta:
        model = ContactDetail
        fields = ['title', 'email', 'phone', 'mobile', 'address', 'branch', 'facebook', 'twitter', 'instagram', 'youtube', 'map_url', 'work_starts', 'work_ends']
        error_class = 'error'


class FaqForm(forms.ModelForm):
    title               = forms.CharField(max_length=100, label='Title', widget=forms.TextInput(attrs={'placeholder':'Enter Position', 'type':'text'}))
    body                = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder':'Enter Content', 'rows':'4', 'type':'textarea'}))
    
    class Meta:
        model = Faq
        fields = ['title', 'body']
        error_class = 'error'


class EventForm(forms.ModelForm):
    name                = forms.CharField(max_length=100, label='Event Title', widget=forms.TextInput(attrs={'placeholder':'Enter Event Title', 'type':'text'}))
    
    class Meta:
        model = Event
        fields = ['name']
        error_class = 'error'


class GalleryForm(forms.ModelForm):
    title               = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label='Select Event Title', label='Event Title')
    image               = forms.ImageField(label='Image', widget=forms.FileInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Gallery
        fields = ['title', 'image']
        error_class = 'error'


class LoanDurationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Loan Duration:', widget=forms.TextInput(attrs={'placeholder': 'Enter Loan Duration', 'type':'text'}))
            
    class Meta:
        model = LoanDuration
        fields = ['name']
        error_class = 'error'


class LoanInterestForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Loan Interest:', widget=forms.TextInput(attrs={'placeholder': 'Enter Loan Interest', 'type':'text'}))
            
    class Meta:
        model = LoanInterest
        fields = ['name']
        error_class = 'error'


class InvestmentDurationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Investment Duration:', widget=forms.TextInput(attrs={'placeholder': 'Enter Investment Duration', 'type':'text'}))
            
    class Meta:
        model = InvestmentDuration
        fields = ['name']
        error_class = 'error'


class InvestmentInterestForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Investment Interest:', widget=forms.TextInput(attrs={'placeholder': 'Enter Investment Interest', 'type':'text'}))
            
    class Meta:
        model = InvestmentInterest
        fields = ['name']
        error_class = 'error'