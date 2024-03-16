from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from backend.models import Profile
from account.models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



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

COUNTRY = [
    ('', 'Select Country'),
    ('Nigeria', 'Nigeria'),
    ('Ghana', 'Ghana'),
    ('Others', 'Others'),
]

class ProfileForm(forms.ModelForm):
    title           = forms.ChoiceField(label='Title', required=True, choices=TITLE, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    middle_name     = forms.CharField(max_length=100, label='Middle Name', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Middle Name', 'type':'text'}))
    gender          = forms.ChoiceField(label='Gender', required=True, choices=GENDER, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    marital         = forms.ChoiceField(label='Marital Status', required=True, choices=MARITAL, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    religion        = forms.ChoiceField(label='Religion', required=True, choices=RELIGION, widget=forms.Select(attrs={'class':'bootstrap-select', 'type':'select'}))
    date_of_birth   = forms.DateField(label='Date of Birth', required=True, widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    phone           = PhoneNumberField(max_length=17, label='Phone Number', region='NG', widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class':'form-select col-6 p-1', 'placeholder':'Phone Number', 'type':'tel'}))
    spousephone     = PhoneNumberField(max_length=17, label='Spouse Phone Number', region='NG', widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class':'form-select col-6 p-1', 'placeholder':'Phone Number', 'type':'tel'}))
    occupation      = forms.CharField(max_length=255, label='Occupation', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Occupation', 'type':'text'}))
    busstop         = forms.CharField(max_length=255, label='Nearest Bus Stop', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Bus Stop', 'type':'text'}))
    address         = forms.CharField(max_length=255, label='Residential Address', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Residential Address', 'type':'text'}))
    office          = forms.CharField(max_length=255, label='Office Address', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Office Address', 'type':'text'}))
    country         = CountryField(blank_label='Select Country').formfield(required=False, widget=CountrySelectWidget(attrs={'class': 'bootstrap-select d-block w-100', 'type':'select'}))
    state           = forms.CharField(max_length=255, label='State of Origin', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your State of Origin', 'type':'text'}))
    lga             = forms.CharField(max_length=255, label='L.G.A. of Origin', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your L.G.A. of Origin', 'type':'text'}))
    home            = forms.CharField(max_length=255, label='Home Town', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Home Town', 'type':'text'}))
    facebook        = forms.URLField(max_length=500, label='Facebook Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your Facebook URL', 'type':'url'}))
    twitter         = forms.URLField(max_length=500, label='Twitter Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your Twitter URL', 'type':'url'}))
    instagram       = forms.URLField(max_length=500, label='Instagram Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your Instagram URL', 'type':'url'}))
    linkedin        = forms.URLField(max_length=500, label='Linkedin Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your Linkedin URL', 'type':'url'}))
    whatsapp        = forms.URLField(max_length=500, label='WhatsApp Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your WhatsApp URL', 'type':'url'}))
    youtube         = forms.URLField(max_length=500, label='Youtube Url', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter your Youtube URL', 'type':'url'}))
    
    class Meta:
        model = Profile
        fields = ['title', 'middle_name', 'gender', 'bio', 'marital', 'religion', 'date_of_birth', 'phone', 'spousephone', 'occupation', 'busstop',  'address', 'office', 'country', 'state', 'lga', 'home', 'facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp', 'youtube']
        exclude = ['user']
        
        
class ProfilePictureForm(forms.ModelForm):
    image           = forms.ImageField(required=True, help_text='Passport format should be; .png, .jpeg, .jpg', widget=forms.FileInput(attrs={'class':'custom-upload', 'accept':'.jpeg, .jpg, .png', 'type':'file', 'name':'image', 'id':'image'}))

    class Meta:
        model = Profile
        fields = ['image', ]

class UpdateUserForm(forms.ModelForm):
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text', 'readonly':'readonly'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text', 'readonly':'readonly'}))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
      
        
class ChangePasswordForm(PasswordChangeForm):
    old_password    = forms.CharField(max_length=100, label='Old Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Old Password', 'type':'password'}))
    new_password1   = forms.CharField(max_length=100, label='New Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter New Password', 'type':'password'}))
    new_password2   = forms.CharField(max_length=100, label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter New Password Again', 'type':'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        

class SuperUserForm(UserCreationForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text'}))
    password1       = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password', 'type':'password'}))
    password2       = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Again', 'type':'password'}))
    is_superuser    = forms.BooleanField(label='Is Super User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_staff        = forms.BooleanField(label='Is Staff User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_active       = forms.BooleanField(label='Is Active', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active']
        
        
class EditSuperUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text', 'readonly':'readonly'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text', 'readonly':'readonly'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text', 'readonly':'readonly'}))
    is_superuser    = forms.BooleanField(label='Is Super User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_staff        = forms.BooleanField(label='Is Staff User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_active       = forms.BooleanField(label='Is Active', initial=True, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active']
        
        
class StaffUserForm(UserCreationForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text'}))
    password1       = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password', 'type':'password'}))
    password2       = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Again', 'type':'password'}))
    is_staff        = forms.BooleanField(label='Is Staff User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_active       = forms.BooleanField(label='Is Active', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active']
        
        
class EditStaffUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text', 'readonly':'readonly'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text', 'readonly':'readonly'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text', 'readonly':'readonly'}))
    is_staff        = forms.BooleanField(label='Is Staff User', initial=True, required=True, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    is_active       = forms.BooleanField(label='Is Active', initial=True, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        
            
class EditUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text', 'readonly':'readonly'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        
class ActionUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Username', 'type':'text', 'readonly':'readonly'}))
    email           = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address', 'type':'email', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your First Name', 'type':'text', 'readonly':'readonly'}))
    last_name       = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Last Name', 'type':'text', 'readonly':'readonly'}))
    is_active       = forms.BooleanField(label='Is Active', initial=True, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']   
