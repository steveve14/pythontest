from django.urls import path
from . import views

app_name = 'shop'  # 네임스페이스 설정

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/customer/', views.customer_signup, name='customer_signup'),
    path('signup/business/', views.business_signup, name='business_signup'),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('login/business/', views.business_login, name='business_login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.view_cart, name='view_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('business_dashboard/', views.business_dashboard, name='business_dashboard'),
]
