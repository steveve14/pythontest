from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.contrib import messages
from .forms import CustomerLoginForm, BusinessLoginForm, CustomerSignupForm, BusinessSignupForm, ProductForm, CategoryForm
from .models import Product, Cart, Order, Customer, Business, Category

# 메인 페이지
def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

# 회원가입 뷰
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.password =form.cleaned_data['password']
            customer.save()
            return redirect('shop:customer_login')
    else:
        form = CustomerSignupForm()
    return render(request, 'shop/signup.html', {'form': form})

def business_signup(request):
    if request.method == 'POST':
        form = BusinessSignupForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.password = form.cleaned_data['password']
            business.save()
            return redirect('shop:business_login')
    else:
        form = BusinessSignupForm()
    return render(request, 'shop/signup.html', {'form': form})

# 로그인 뷰
def customer_login(request):
    form = CustomerLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_id = form.cleaned_data['user_id']
        password = form.cleaned_data['password']
        try:
            customer = Customer.objects.get(user_id=user_id)
            if password == customer.password:
                request.session['customer_id'] = customer.id
                request.session['is_customer_authenticated'] = True
                request.session['business_id'] = None
                request.session['is_business_authenticated'] = False
                messages.success(request, 'Successfully logged in')
                return redirect('shop:index')
            else:
                messages.error(request, '비밀번호를 확인하세요.')
        except Customer.DoesNotExist:
            messages.error(request, '비밀번호를 확인하세요.')
    return render(request, 'shop/customer_login.html', {'form': form})

def business_login(request):
    form = BusinessLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        business_name = form.cleaned_data['business_name']
        password = form.cleaned_data['password']
        try:
            business = Business.objects.get(business_name=business_name)
            if password == business.password:
                request.session['business_id'] = business.id
                request.session['is_business_authenticated'] = True
                request.session['customer_id'] = None
                request.session['is_customer_authenticated'] = False
                messages.success(request, 'Successfully logged in')
                return redirect('shop:business_dashboard')
            else:
                messages.error(request, '비밀번호를 확인하세요.')
        except Business.DoesNotExist:
            messages.error(request, '비밀번호를 확인하세요.')
    return render(request, 'shop/business_login.html', {'form': form})

# 로그아웃 뷰
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('shop:index')

# 상품 검색 뷰
def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(product_name__icontains=query)
    return render(request, 'shop/search_results.html', {'products': products})



# 체크아웃 뷰
def checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(customer=request.user.customer, order_completed=False)
        order = Order.objects.create(customer=request.user.customer)
        for item in cart_items:
            item.order_completed = True
            item.order_time = timezone.now()
            item.save()
            order.products.add(item.product)
        return render(request, 'shop/checkout_success.html', {'order': order})
    return render(request, 'shop/checkout.html')

#데쉬보드(비즈니스)
def business_dashboard(request):
    business_id = request.session.get('business_id')
    if not business_id:
        return redirect('shop:business_login')
    
    business = Business.objects.get(id=business_id)
    orders = Order.objects.filter(product__business_id=business)
    products = Product.objects.filter(business_id=business)
    categories = Category.objects.all()

    if request.method == 'POST':
        if 'create_product' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.business = business
                product.save()
                # 선택된 카테고리들 저장
                product.categories.set(product_form.cleaned_data['categories'])
                messages.success(request, 'Product created successfully')
                return redirect('shop:business_dashboard')
        elif 'create_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Category created successfully')
                return redirect('shop:business_dashboard')
    else:
        product_form = ProductForm()
        category_form = CategoryForm()

    context = {
        'orders': orders,
        'products': products,
        'categories': categories,
        'product_form': product_form,
        'category_form': category_form
    }
    return render(request, 'shop/business_dashboard.html', context)

#로그인 상태 확인을 위한 뷰
def some_view(request):
    context = {
        'is_customer_authenticated': request.session.get('is_customer_authenticated', False),
        'is_business_authenticated': request.session.get('is_business_selected', False),
    }
    return render(request, 'shop/some_template.html', context)

# 카트에 상품 추가 뷰
def add_to_cart(request, product_id):
    if not request.session.get('customer_id', None):
        return redirect('shop:customer_login')
    
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:customer_login')
    customer = get_object_or_404(Customer, id=customer_id)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, 'Product added to cart')
    return redirect('shop:view_cart')

# 카트 삭제 뷰
def remove_from_cart(request, product_id,  action):
    if not request.session.get('customer_id', None):
        return redirect('shop:customer_login')
    
    customer = get_object_or_404(Customer, user_id=request.user.id)
    cart_item = get_object_or_404(Cart, product_id=product_id, customer=customer)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('shop:cart_detail')
# 카트 겟수 조절 뷰
def update_cart_quantity(request, cart_id, action):
    if not request.session.get('customer_id', None):
        return redirect('shop:customer_login')
    
    cart_item = get_object_or_404(Cart, id=cart_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            return redirect('shop:view_cart')
    cart_item.save()
    return redirect('shop:view_cart')

# 카트 보기 뷰
def view_cart(request):  
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:customer_login')
    
    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = Cart.objects.filter(customer=customer)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'orders': orders})

#구입
def purchase(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:customer_login')
    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = Cart.objects.filter(customer=customer)
    if not cart_items:
        messages.error(request, 'Your cart is empty')
        return redirect('shop:view_cart')

    for item in cart_items:
        Order.objects.create(
            quantity=item.quantity,
            order_date=timezone.now(),
            product=item.product,
            customer=customer
        )
        item.delete()

    messages.success(request, 'Purchase completed successfully')
    return redirect('shop:index')