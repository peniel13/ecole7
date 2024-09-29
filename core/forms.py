# core/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Payment, Behavior, Note, Attendance,CustomUser,AutresFrais,Convocation




class RegisterForm(forms.ModelForm): 
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label='Password',
        help_text='Password must be at least 8 characters long.'
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        label='Confirm Password',
        help_text='Please confirm your password.'
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label='Role',
        help_text='Select your role: Student or Teacher.'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }
        labels = {
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        help_texts = {
            'email': 'Enter a valid email address.',
            'first_name': 'Enter your first name.',
            'last_name': 'Enter your last name.',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        if request and not request.user.is_staff:
            self.fields['role'].choices = [
                choice for choice in CustomUser.ROLE_CHOICES if choice[0] != 'admin'
            ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_pic', 'address', 'phone', 'bio']

# forms.py
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reason', 'amount', 'month', 'class_assigned']  # Ajouter le champ class_assigned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month'].widget = forms.Select(choices=Payment.MONTH_CHOICES)
        
        # Si vous voulez cacher le champ class_assigned
        self.fields['class_assigned'].widget = forms.HiddenInput()


class BehaviorForm(forms.ModelForm):
    class Meta:
        model = Behavior
        fields = ['commentaire', 'level', 'periode']  # Ajout des nouveaux champs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].widget = forms.Select(choices=Behavior.LEVEL_CHOICES)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['epreuve', 'date_epreuve', 'note']  # Ajout des nouveaux champs


class AutresFraisForm(forms.ModelForm):
    class Meta:
        model = AutresFrais
        fields = [ 'motif', 'date_frais', 'montant']  # Ajout du champ user si nécessaire


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['absences', 'presences']


class ConvocationForm(forms.ModelForm):
    class Meta:
        model = Convocation
        fields = ['titre', 'raison', 'statut']




