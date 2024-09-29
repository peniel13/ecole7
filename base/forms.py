from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import BlogInfo, Contact,Preinscription,Payment





class BlogInfoForm(forms.ModelForm):
    class Meta:
        model = BlogInfo
        fields = ['title', 'content', 'description', 'image']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'content', 'number']


class PreinscriptionForm(forms.ModelForm):
    class Meta:
        model = Preinscription
        fields = ['first_name', 'last_name', 'email', 'description', 'document']

from django import forms

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'position', 'email', 'phone', 'amount', 'device', 'transaction_id', 'transaction_number', 'description']

