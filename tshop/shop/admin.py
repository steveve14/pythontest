from django.contrib import admin
from .models import Cart, Address, Customer, Business, Product, Category, ProductCategory, Order

admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Business)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductCategory)