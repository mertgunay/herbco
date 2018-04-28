from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras import SelectDateWidget

from profiles.models import User, Distributor
from shop.models import ShoppingCart
from django_countries.widgets import CountrySelectWidget

class RegisterForm(forms.ModelForm):
    username    = forms.CharField(help_text="")
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password Again', widget=forms.PasswordInput)
    email       = forms.EmailField(label='Email Adress', required=True)

    class Meta:
        model = User
        fields = [

            'last_name',
            'first_name',
            'email',
            'username',
            'adress',
            'postcode',
            'country',

        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email already exists!")
        return email

    def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Password does not match!")
            return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            shopcart = ShoppingCart.objects.create(owner=user)
            shopcart.save()
        return user

class DistributorCreateForm(forms.ModelForm):
    company_created_At = forms.DateField(widget=SelectDateWidget(years=range(1970, 2018)))

    class Meta:
        model = Distributor
        fields = [
            'brand',
            'ceo_name',
            'average_earnings',
            'company_created_At',
        ]
