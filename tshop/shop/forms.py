from django import forms
from .models import Customer, Business, Product, Category, ProductCategory, Address

##Customer 회원가입
class CustomerSignupForm(forms.ModelForm):
    street_address = forms.CharField(max_length=225, required=True, label='거리 주소')
    city = forms.CharField(max_length=45, required=True, label='도시')
    state = forms.CharField(max_length=45, required=True, label='주')
    country = forms.CharField(max_length=45, required=True, label='국가')
    postal_code = forms.CharField(max_length=20, required=True, label='우편번호')
    password = forms.CharField(widget=forms.PasswordInput(), label='비밀번호')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='비밀번호 확인')

    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone_number', 'user_id', 'password', 'password_confirm']
        labels = {
            'name': '이름',
            'age': '나이',
            'phone_number': '전화번호',
            'user_id': '사용자 ID'
        }

    def clean(self):
        # 부모 클래스의 clean() 메소드 호출
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # 비밀번호와 비밀번호 확인이 일치하지 않으면 ValidationError 발생
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data


    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.password = self.cleaned_data['password']
        # 주소 인스턴스 생성
        address = Address(
            street_address=self.cleaned_data['street_address'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            country=self.cleaned_data['country'],
            postal_code=self.cleaned_data['postal_code']
        )
        address.save()  # 주소 저장
        customer.address = address
        if commit:
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

##주소
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'country', 'postal_code']