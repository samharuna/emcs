from django import forms
from account.models import User
from applications.models import Loan, LoanDuration, Investment, InvestmentDuration, Requirement
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


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
    ('Son', 'Son'),
    ('Daughter', 'Daughter'),
]

GENDER = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

COUNTRY = [
    ('', 'Select Country'),
    ('Nigeria', 'Nigeria'),
    ('Ghana', 'Ghana'),
    ('Others', 'Others'),
]

MARITAL = [
    ('', 'Select Marital Status'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Others', 'Others'),
]

IDENTITY = [
    ('', 'Select Means of Identification'),
    ('Voter Card', 'Voter Card'),
    ('NIMC Card', 'NIMC Card'),
    ('Passport', 'Passport'),
    ('Driver License', 'Driver License'),
]


class LoanDurationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Loan Duration:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Loan Duration', 'type':'text'}))
            
    class Meta:
        model = LoanDuration
        fields = ['name']
        error_class = 'error'


class LoanForm(forms.ModelForm):
    purpose                 = forms.CharField(label='Purpose for seeking Loan', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the purpose for seeking Loan', 'type':'text'}))
    amount                  = forms.CharField(label='Amount Applying for in Figure:', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter amount applying for (In figure)', 'type':'number'}))
    words                   = forms.CharField(max_length=255, label='Amount Applying for in Words:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter amount applying for (In words)', 'type':'text'}))
    plan                    = forms.ChoiceField(label='Loan Plan:', choices=LOANPLAN, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    guarantor               = forms.CharField(max_length=255, label='Guarantor Full Name:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Full Name', 'type':'text'}))
    guarantor_email         = forms.EmailField(max_length=255, label='Guarantor Email Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address', 'type':'email'}))
    guarantor_occupation    = forms.CharField(max_length=255, label='Guarantor Occupation:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Guarantor Occupation', 'type':'text'}))
    guarantor_mobile        = PhoneNumberField(max_length=17, region='NG', label='Guarantor Phone Number', widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class':'form-select col-6 p-1', 'type':'tel', 'placeholder':'Phone Number'}))
    guarantor_address       = forms.CharField(max_length=255, label='Guarantor Residential Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Guarantor Residential Address', 'type':'text'}))
    guarantor_office        = forms.CharField(max_length=255, label='Guarantor Office Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Guarantor Office Address', 'type':'text'}))
    guarantor_gender        = forms.ChoiceField(label='Gender:', choices=GENDER, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    guarantor_marital       = forms.ChoiceField(label='Marital Status:', choices=MARITAL, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    relationship            = forms.ChoiceField(label='Relationship with Applicant:', choices=RELATIONSHIP, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    duration                = forms.ModelChoiceField(queryset=LoanDuration.objects.all(), empty_label='Select Loan Duration:', label='Loan Duration (Weeks)', widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    guarantor_state         = forms.CharField(max_length=150, label='State of Origin:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter State of Origin', 'type':'text'}))
    guarantor_lga           = forms.CharField(max_length=150, label='Local Government Area of Origin:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter LGA of Origin', 'type':'text'}))
    guarantor_home          = forms.CharField(max_length=150, label='Home Town:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Home Town', 'type':'text'}))
    years_known             = forms.CharField(max_length=20, label='Years of relationship with Applicant:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Years of relationship with Applicant', 'type':'text'}))
   
    class Meta:
        model = Loan
        fields = ['purpose', 'amount',  'words', 'plan', 'duration', 'guarantor_lga', 'guarantor', 'guarantor_gender', 'guarantor_marital', 'years_known', 'guarantor_mobile', 
                  'guarantor_email', 'guarantor_home', 'picture', 'guarantor_occupation', 'guarantor_address', 'guarantor_office', 'relationship', 'guarantor_country', 'guarantor_state']
        error_class = 'error'
                

class UpdateLoanForm(forms.ModelForm):
    applicant               = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'bootstrap-select', 'readonly':'readonly'}))
    guarantor               = forms.CharField(max_length=255, label='Guarantor Full Name:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Full Name', 'type':'text', 'readonly':'readonly'}))
    total_amount            = forms.IntegerField(label='Total Amount:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Total Loan Amount', 'type':'number', 'readonly':'readonly'}))
    
    class Meta:
        model = Loan
        fields = ['status', 'applicant', 'total_amount', 'guarantor']
        error_class = 'error'


class LoanPaymentForm(forms.ModelForm):
    applicant               = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'bootstrap-select', 'readonly':'readonly'}))
    amount                  = forms.IntegerField(label='Loan Principal:', required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Principal', 'type':'number', 'readonly':'readonly'}))
    repayment               = forms.IntegerField(label='Loan Repayment:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Repayment', 'type':'number', 'readonly':'readonly'}))
    interest                = forms.IntegerField(label='Loan Interest:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Interest', 'type':'number', 'readonly':'readonly'}))
    total_amount            = forms.IntegerField(label='Total Amount:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Total Loan Amount', 'type':'number', 'readonly':'readonly'}))
    plan                    = forms.ChoiceField(label='Loan Plan:',  required=False, choices=LOANPLAN, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select', 'readonly':'readonly'}))
    duration                = forms.ModelChoiceField(queryset=LoanDuration.objects.all(), empty_label='Select Loan Duration:', label='Loan Duration (Weeks)', widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    percent                 = forms.IntegerField(label='Loan Percent:', initial=10,  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Percent', 'type':'number'}))
    payment_period          = forms.CharField(label='Payment Period:', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Payment Period', 'type':'text'}))
    payment_starts          = forms.CharField(label='Payment Starts:', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Payment Starts Date', 'type':'text'}))
    payment_ends            = forms.CharField(label='Payment Ends:', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Payment Maturity Date', 'type':'text'}))
    
    class Meta:
        model = Loan
        fields = ['applicant', 'amount', 'percent', 'duration', 'interest', 'plan', 'payment_period', 'payment_starts', 'payment_ends', 'repayment', 'total_amount']
        error_class = 'error'



class InvestmentDurationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Investment Duration:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Investment Duration', 'type':'text'}))
            
    class Meta:
        model = InvestmentDuration
        fields = ['name']



class InvestmentForm(forms.ModelForm):
    amount                  = forms.CharField(label='Amount in Figure:', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter amount you intend to Invest (In figure)', 'type':'number'}))
    words                   = forms.CharField(max_length=255, label='Amount in Words', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter amount you intend to Invest (In words)', 'type':'text'}))
    duration                = forms.ModelChoiceField(queryset=InvestmentDuration.objects.all(), empty_label='Select Investment Duration:', label='Investment Duration [6 Months]', widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    next_kin_mobile         = PhoneNumberField(max_length=17, region='NG', label='Next of Kin Phone Number', widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class':'form-select col-6 p-1', 'type':'tel', 'placeholder':'Phone Number'}))
    next_kin                = forms.CharField(max_length=255, label='Next of Kin Full Name:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Next of Kin Full Name', 'type':'text'}))
    next_kin_email          = forms.EmailField(max_length=255, label='Next of Kin Email Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Next of Kin Email Address', 'type':'email'}))
    next_kin_occupation     = forms.CharField(max_length=255, label='Next of Kin Occupation:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Next of Kin Occupation', 'type':'text'}))
    next_kin_address        = forms.CharField(max_length=255, label='Next of Kin Residential Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Next of Kin Residential Address', 'type':'text'}))
    next_kin_office         = forms.CharField(max_length=255, label='Next of Kin Office Address:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Next of Kin Office Address', 'type':'text'}))
    relationship            = forms.ChoiceField(label='Next of Kin Relationship:', choices=RELATIONSHIP, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    
    class Meta:
        model = Investment
        fields = ['amount', 'words', 'duration', 'next_kin', 'next_kin_mobile', 'next_kin_email', 'next_kin_occupation', 'next_kin_address', 'next_kin_office', 'relationship', 'picture']
        error_class = 'error'

class UpdateInvestmentForm(forms.ModelForm):
    investor                = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'bootstrap-select', 'readonly':'readonly'}))
    total_amount            = forms.IntegerField(label='Total Amount:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Total Investment Amount', 'type':'number', 'readonly':'readonly'}))
    next_kin                = forms.CharField(max_length=255, label='Next of Kin Full Name:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Next of Kin Full Name', 'type':'text', 'readonly':'readonly'}))
    
    class Meta:
        model = Investment
        fields = ['status', 'investor', 'next_kin', 'total_amount']
        error_class = 'error'


class InvestmentPaymentForm(forms.ModelForm):
    investor                = forms.ModelChoiceField(queryset=User.objects.all(), label='', required=False, widget=forms.Select(attrs={'class': 'bootstrap-select', 'readonly':'readonly'}))
    description             = forms.CharField(max_length=150, label='Investment Description:', initial='Fixed Deposit', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Description', 'type':'text'}))
    director_name           = forms.CharField(label='Director Full Name:', initial='Akintola, Omowumi Ajibola', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Director Full Name', 'type':'text'}))
    interest                = forms.IntegerField(label='Investment Interest:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Interest', 'type':'number', 'readonly':'readonly'}))
    percent                 = forms.IntegerField(label='Investment Percent:', initial=10,  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Percent', 'type':'number'}))
    amount                  = forms.IntegerField(label='Investment Principal:', required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Principal', 'type':'number', 'readonly':'readonly'}))
    total_amount            = forms.IntegerField(label='Total Amount:',  required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Total Investment Amount', 'type':'number', 'readonly':'readonly'}))
    investment_starts       = forms.CharField(label='Investment Starts:', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Starts Date', 'type':'text'}))
    investment_ends         = forms.CharField(label='Investment Ends:', required=False, max_length=266, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Investment Ends Date', 'type':'text'}))
    
    class Meta:
        model = Investment
        fields = ['investor', 'description', 'director_name', 'interest', 'amount', 'percent', 'total_amount', 'investment_starts', 'investment_ends']
    

class RequirementForm(forms.ModelForm):
    title           = forms.CharField(max_length=120, label='Service Title:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Service Title', 'type':'text'}))
    link            = forms.CharField(max_length=120, label='Service Link:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Service Link', 'type':'text'}))
    link_caption    = forms.CharField(max_length=120, label='Service Link Caption:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Service Link Caption', 'type':'text'}))
    
    class Meta:
        model = Requirement
        fields = ['title', 'body', 'link', 'link_caption']
