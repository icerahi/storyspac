from django import forms

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import UserProfile

from allauth.account.views import LoginForm


class UserRegisterForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError('This username name already taken')
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError('This email already register')
        return email




## User edit form
class UserEditForm(forms.ModelForm):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={
        "class":"form-control col-sm-9",
    }))


    email=forms.EmailField(disabled=True,widget=forms.EmailInput(attrs={
        'class':'form-control col-sm-9',

    }))
    class Meta:
        model=User
        fields=('username','email')




## only profile update form
class ProfileEditForm(forms.ModelForm):
    fullname=forms.CharField(required=False,widget=forms.TextInput(attrs={
        "class":"form-control col-sm-9",
    }))

    profile_pic = forms.ImageField(
        label='', help_text="JPEG,PNG,JPG will accepted", required=False,widget=forms.FileInput(
            attrs={

            }
        )

    )

    date_of_birth=forms.DateField(required=False,widget=forms.DateInput(attrs={

        'type':'date'

    }))
    bio=forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class':'form-control col-sm-9'
    }))
    class Meta:
        model=UserProfile
        exclude=('user',)

class PasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'class':'form-control col-sm-9'
    }))
    new_password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'class':'form-control col-sm-9'
    }))
    new_password2=forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'class':'form-control col-sm-9'
    }))
    class Meta:
        model=User
        fields=('old_password','new_password1','new_password2')