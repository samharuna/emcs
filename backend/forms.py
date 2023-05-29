from django import forms
from accounts.models import User
from backend.models import Profile
from frontend.models import Occupation
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm



class AddSuperUserForm(UserCreationForm):
    username        = forms.CharField(max_length=100, label='Enter Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'type':'text'}))
    first_name      = forms.CharField(max_length=100, label='Enter First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Enter Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Enter Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email'}))
    password1       = forms.CharField(max_length=100, label='Enter Password:', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'type':'password'}))
    password2       = forms.CharField(max_length=100, label='Enter Confirm Password:', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confrim Password', 'type':'password'}))
    is_superuser    = forms.BooleanField(initial=True, required=True)
    is_staff        = forms.BooleanField(initial=True, required=True)
    is_active       = forms.BooleanField(initial=True, required=True)

    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active']
        error_class = 'error'


class UpdateSuperUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Enter Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'type':'text'}))
    first_name      = forms.CharField(max_length=100, label='Enter First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Enter Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Enter Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email'}))
    is_superuser    = forms.BooleanField(initial=True, required=True)
    is_staff        = forms.BooleanField(initial=True, required=True)
    is_active       = forms.BooleanField(initial=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
        error_class = 'error'



class AddUserForm(UserCreationForm):
    username        = forms.CharField(max_length=100, label='Enter Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'type':'text'}))
    first_name      = forms.CharField(max_length=100, label='Enter First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Enter Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Enter Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email'}))
    password1       = forms.CharField(max_length=100, label='Enter Password:', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'type':'password'}))
    password2       = forms.CharField(max_length=100, label='Enter Confirm Password:', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confrim Password', 'type':'password'}))
    is_staff        = forms.BooleanField(initial=True, required=True)
    is_active       = forms.BooleanField(initial=True, required=True)

    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active']
        error_class = 'error'


class UpdateUserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Enter Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'type':'text', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='Enter First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Enter Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Enter Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email', 'readonly':'readonly'}))
    is_staff        = forms.BooleanField(initial=True, required=True)
    is_active       = forms.BooleanField(initial=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        error_class = 'error'


class EditUserForm(forms.ModelForm):
    first_name      = forms.CharField(max_length=100, label='First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text', 'readonly':'readonly'}))
    last_name       = forms.CharField(max_length=100, label='Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text', 'readonly':'readonly'}))
    email           = forms.EmailField(max_length=100, label='Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email', 'readonly':'readonly'}))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        error_class = 'error'
        

class UserForm(forms.ModelForm):
    username        = forms.CharField(max_length=100, label='Username:', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'type':'text', 'readonly':'readonly'}))
    first_name      = forms.CharField(max_length=100, label='First Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'type':'text'}))
    last_name       = forms.CharField(max_length=100, label='Last Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label='Email Address:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address', 'type':'email', 'readonly':'readonly'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        error_class = 'error'


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


class ProfileForm(forms.ModelForm):
    title           = forms.ChoiceField(label='Title:', choices=TITLE, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    middlename      = forms.CharField(max_length=50, required=False, label='Middle Name:', widget=forms.TextInput(attrs={'placeholder':'Middle Name here...', 'type':'text'}))
    religion        = forms.ChoiceField(label='Religion:', choices=RELIGION, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    dob             = forms.DateTimeField(label='Date of Birth:', widget=forms.DateInput(attrs={'type':'date', 'class':'form-select pt-1'}))
    gender          = forms.ChoiceField(label='Gender:', choices=GENDER, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    marital         = forms.ChoiceField(label='Marital Status:', choices=MARITAL, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    phonenumber     = PhoneNumberField(region='NG', label='Mobile Number:', help_text='Mobile Number Format: +2347037678697')
    occupation      = forms.ModelChoiceField(queryset=Occupation.objects.all(), empty_label='Select Occupation', label='Occupation')
    bio             = forms.CharField(max_length=300, label='Biography:', required=False, widget=forms.Textarea(attrs={'placeholder':'Enter Biography here...', 'rows':'4', 'type':'textarea'}))
    address         = forms.CharField(max_length=255, label='Residential Address:', widget=forms.TextInput(attrs={'placeholder':'Enter Residential Address here...', 'type':'text'}))
    busstop         = forms.CharField(max_length=255, label='Nearest Bus Stop:', widget=forms.TextInput(attrs={'placeholder':'Enter Nearest Bus Stop here...', 'type':'text'}))
    office          = forms.CharField(max_length=255, label='Office Address:', widget=forms.TextInput(attrs={'placeholder':'Enter Office Address here...', 'type':'text'}))
    country         = forms.ChoiceField(label='Country:', choices=COUNTRY, widget=forms.Select(attrs={'class':'form-select pt-1', 'type':'select'}))
    state           = forms.CharField(max_length=150, label='State of Origin:', widget=forms.TextInput(attrs={'placeholder':'Enter State of Origin here...', 'type':'text'}))
    lga             = forms.CharField(max_length=150, label='Local Government Area of Origin:', widget=forms.TextInput(attrs={'placeholder':'Enter LGA of Origin here...', 'type':'text'}))
    home            = forms.CharField(max_length=150, label='Home Town:', widget=forms.TextInput(attrs={'placeholder':'Enter Home Town here...', 'type':'text'}))
    facebook        = forms.URLField(max_length=255, label='Facebook Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Facebook Link here...', 'type':'url'}))
    twitter         = forms.URLField(max_length=255, label='Twitter Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Twitter Link here...', 'type':'url'}))
    instagram       = forms.URLField(max_length=255, label='Instagram Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Instagram Link here...', 'type':'url'}))
    youtube         = forms.URLField(max_length=255, label='Youtube Link:', required=False, widget=forms.URLInput(attrs={'placeholder':'Enter your Youtube Link here...', 'type':'url'}))
    image           = forms.ImageField(label='Passport', widget=forms.FileInput())
    
    class Meta:
        model = Profile
        fields = ['title', 'middlename', 'religion', 'dob', 'gender', 'phonenumber',  'marital', 'occupation', 'address', 'busstop', 'office', 'bio', 'country', 'state', 'lga', 'home', 'facebook', 'twitter', 'instagram', 'youtube', 'image']
        error_class = 'error'


class OccupationForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label='Occupation:', widget=forms.TextInput(attrs={'placeholder': 'Enter Occupation', 'type':'text'}))
            
    class Meta:
        model = Occupation
        fields = ['name']
        error_class = 'error'