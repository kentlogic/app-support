# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm
from django.forms import DateInput , SelectDateWidget , EmailField
from django_crispy_bulma.widgets import EmailInput

from .models import User , Profile



class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']
        widgets = {
            'email': EmailInput(attrs={'class': 'input'}),
        }


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name' , 'last_name')

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileUpdateForm(forms.ModelForm):
    #birth_date = forms.DateField()

    class Meta:
        model = Profile
        fields = ['middle_name' , 'extension_name' , 'nickname' , 'marital_status' , 'phone_number' , 'mobile_number' ,
                  'birth_date' , 'present_address' , 'permanent_address' , 'gender' , 'image']
        widgets = {
            'birth_date': DateInput()
        }

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['middle_name' , 'extension_name' , 'nickname' , 'marital_status' , 'phone_number' , 'mobile_number' ,
                  'birth_date' , 'present_address' , 'permanent_address' , 'gender' , 'image']
        widgets = {
            'birth_date': DateInput()
        }

#yyyy-MM-dd
# widgets = {
#  'birth_date': DateInput(attrs={'type': 'date', 'input_format': '%y-%N-%d'})
#   }