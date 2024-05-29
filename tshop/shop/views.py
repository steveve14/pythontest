from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from .forms import ProductCategoryForm, CustomerLoginForm, BusinessLoginForm, CustomerSignupForm, BusinessSignupForm, ProductForm, CategoryForm, ProductCategoryForm, AddressForm
from .models import Product, Cart, Order, Customer, Business, Category, ProductCategory

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

#데쉬보드(비즈니스)
def business_dashboard(request):
    business_id = request.session.get('business_id')
    if not business_id:
        return redirect('shop:business_login')
    
    business = Business.objects.get(id=business_id)
    orders = Order.objects.filter(product__business_id=business)
    products = Product.objects.filter(business_id=business)
    product_categories = ProductCategory.objects.filter(product__in=products)
    categories = Category.objects.all()
    customer = Customer.objects.all()

    product_categories_dict = {}
    for pc in product_categories:
        if pc.product.id not in product_categories_dict:
            product_categories_dict[pc.product.id] = []
        product_categories_dict[pc.product.id].append(pc.category.category_name)
    

    if request.method == 'POST':
        ##재품 추가
        if 'create_product' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.business = business
                product.save()
                messages.success(request, '제품이 성공적으로 생성되었습니다.')
                return redirect('shop:business_dashboard')
        ## 카테고리 생성
        elif 'create_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, '카테고리가 성공적으로 생성되었습니다.')
                return redirect('shop:business_dashboard')
        ##카테고리 설정
        elif 'product_category' in request.POST:
            if 'product_category' in request.POST:
                product_category_form = ProductCategoryForm(request.POST, business_id=business_id)
                if product_category_form.is_valid():
                    product_category_form.save()
                    messages.success(request, '상품에 카테고리가 추가되었습니다.')
                    return redirect('shop:business_dashboard')
            
    else:
        product_form = ProductForm()
        category_form = CategoryForm()
        product_category_form = ProductCategoryForm(business_id=business_id)

    context = {
        'orders': orders,
        'products': products,
        'categories': categories,
        'customer' : customer,
        'product_form': product_form,
        'category_form': category_form,
        'product_category_form': product_category_form,
        'product_categories_dict': product_categories_dict,
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

# 카트 겟수 조절,삭제 뷰
def update_cart_quantity(request, cart_id, action):
    if not request.session.get('customer_id', None):
        return redirect('shop:customer_login')
    
    cart_item = get_object_or_404(Cart, id=cart_id)
    
    ## 갯수 + (max 물건.갯수 추가 예정)
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    ##갯수 감소 (1 이하는 무시)
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            return redirect('shop:view_cart')
        cart_item.save()
    ##물건 삭제
    elif action == 'delete':
        cart_item.delete()
    
    ## 카트로 돌아 갈때 사용
    return redirect('shop:view_cart') 

# 카트 보기 뷰
def view_cart(request):  
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:customer_login')
    
    customer = get_object_or_404(Customer, id=customer_id)
    address = customer.address
    cart_items = Cart.objects.filter(customer=customer)
    orders = Order.objects.filter(customer=customer)

    address_form = AddressForm(instance=address)

    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('shop:view_cart')

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'orders': orders,
        'customer': customer,
        'address': address,
        'address_form': address_form,
    })

#구입
def purchase(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('shop:customer_login')
    
    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = Cart.objects.filter(customer=customer)
    
    if not cart_items:
        messages.error(request, '카트가 비어있습니다.')
        return redirect('shop:view_cart')

    for item in cart_items:
        Order.objects.create(
            quantity=item.quantity,
            order_date=timezone.now(),
            product=item.product,
            customer=customer
        )
        item.delete()

    messages.success(request, '주문 완료')
    return redirect('shop:view_cart')