from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Business, Product, Category
from django.contrib.auth.hashers import make_password

##Customer 회원가입
class CustomerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone_number', 'user_id', 'password']

##Business 회원가입
class BusinessSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = Business
        fields = ['business_name', 'registration_number', 'email', 'password']

##Customer 로그인
class CustomerLoginForm(forms.Form):
    user_id = forms.CharField(max_length=45, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

##Business 로그인
class BusinessLoginForm(forms.Form):
    business_name = forms.CharField(max_length=45, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

#
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Product
        fields = ['product_name', 'stock', 'price', 'categories']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']