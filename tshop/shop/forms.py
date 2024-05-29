from django import forms
from .models import Customer, Business, Product, Category, ProductCategory, Address

##Customer 회원가입
class CustomerSignupForm(forms.ModelForm):
    street_address = forms.CharField(max_length=225, required=True)
    city = forms.CharField(max_length=45, required=True)
    state = forms.CharField(max_length=45, required=True)
    country = forms.CharField(max_length=45, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone_number', 'user_id', 'password']

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.password = self.cleaned_data['password']
        if commit:
            customer.save()
            address = Address(
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                country=self.cleaned_data['country'],
                postal_code=self.cleaned_data['postal_code'],
                Customer_id=customer
            )
            address.save()
            customer.address = address
            customer.save()
        return customer
    
    
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

#Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

#ProductForm
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'stock', 'price']

#Category
class ProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        business_id = kwargs.pop('business_id', None)
        super().__init__(*args, **kwargs)
        if business_id:
            self.fields['product'].queryset = Product.objects.filter(business_id=business_id)
        
        self.fields['category'].queryset = Category.objects.all()
        self.fields['product'].label_from_instance = lambda instance: instance.product_name
        self.fields['category'].label_from_instance = lambda instance: instance.category_name
    
    class Meta:
        model = ProductCategory
        fields = ['product', 'category']