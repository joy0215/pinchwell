from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order ,OrderItem
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from sneaker_store.forms import UserProfileForm



class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用戶名或電子郵件'  # 修改用戶名字段標籤為“用戶名或電子郵件”


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, '無效的用戶名或密碼。')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

import logging

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from sneaker_store.forms import UserCreationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Registration successful!')
            return redirect('index')  # 注册成功后重定向到首页或其他页面
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})



# 商品列表視圖
class ProductListView(TemplateView):
    template_name = 'shop/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context

# 商品詳情視圖
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# 添加商品到購物車視圖
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        selected_size = request.POST.get('size')
        order, created = Order.objects.get_or_create(user=request.user, ordered=False)
        order.products.add(product)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product, size=selected_size)
        messages.success(request, '商品已成功添加到購物車！')
        return redirect('product_detail', pk=pk)
    else:
        return redirect('product_detail', pk=pk)

# 購物車視圖
@login_required
def cart(request):
    cart_items = []  # 您的購物車邏輯應該在這裡獲取購物車中的商品列表
    total_price = sum(item.price for item in cart_items) if cart_items else 0
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# 結賬視圖
@login_required
def checkout(request):
    # 處理結賬邏輯
    return render(request, 'shop/checkout.html', {})

# 完成訂單視圖
@login_required
def complete_order(request):
    # 建立訂單並重定向到訂單確認頁面
    return redirect('order_confirmation')

# 訂單確認視圖
@login_required
def order_confirmation(request):
    # 渲染訂單確認頁面
    return render(request, 'shop/order_confirmation.html', {})

# 首頁視圖
def index(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'index.html', {'user': user})

from django.contrib.auth.forms import UserCreationForm

# 行銷頁面視圖
def marketing_page(request):
    return render(request, 'marketing/marketing.html')
