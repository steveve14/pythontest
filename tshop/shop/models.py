from django.db import models
from django.contrib.auth.hashers import make_password

class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    cart_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

class Order(models.Model):
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

class Address(models.Model):
    street_address = models.CharField(max_length=225)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=20)
    customer = models.OneToOneField('Customer', related_name='address', on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=45)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    user_id = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, primary_key=True)

class Business(models.Model):
    business_name = models.CharField(max_length=45)
    registration_number = models.IntegerField(unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=45, unique=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    category_name = models.CharField(max_length=45)

class ProductCategory(models.Model):  # 'models'로 변경
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)