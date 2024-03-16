from django import forms
from newsletter.models import Subscriber, SendMessage, Mails


class SubscriberForm(forms.ModelForm):
    email       = forms.EmailField(max_length=100, label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address for our Newsletter subscription', 'type':'email', 'id':'email', 'name':'email'}))
    class Meta:
        model = Subscriber
        fields = ['email',]
        
        
class SendMessageForm(forms.ModelForm):
    subject     = forms.CharField(max_length=100, label='Message Subject', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Subject for our Newsletter subscription lists', 'type':'text'}))
    class Meta:
        model = SendMessage
        fields = ['subject', 'body']
        
        
class MailsForm(forms.ModelForm):
    subject     = forms.CharField(max_length=70, label='Mail Subject', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Mail Subject', 'type':'text'}))
    
    class Meta:
        model = Mails
        fields = ['subject', 'body']
    
        