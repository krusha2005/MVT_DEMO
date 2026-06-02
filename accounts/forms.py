from django import forms
from .models import User, SellerProfile
from products.models import Category
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class LoginForm(AuthenticationForm):
    pass

class BuyerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'city', 'state']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SellerRegisterForm(forms.ModelForm):
    username = forms.CharField( widget=forms.TextInput( attrs={'class' :'form-control'}))
    email = forms.EmailField( 
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@gmail\.com$', message='email must be ends with @gmail.com'
            )
        ],
        widget=forms.EmailInput( attrs={'class':'form-control'})
        )
    password = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#*^&=!%]).{8,16}$',message='password must be contain one symbol ,capital ,small latter nd number nd atleast 8 digit password! '
            )
        ],
        widget=forms.PasswordInput( attrs={'class':'form-control'})
        )
    store_name = forms.CharField(widget=forms.TextInput( attrs={'class':'form-control'}))
    phone= forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[^0]\d{9}$',message='phone number must be excatly 10 digits nd does not start with 0 !'
            )
        ],
        widget=forms.TextInput(attrs={'class':'form-control','maxlength':'10'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple() 
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'city', 'state','categories']
        widgets={
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'})
        }
