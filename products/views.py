# 引入Django模組
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm  # 引入 Django 提供的用戶註冊表單
from django.contrib.auth import authenticate, login
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    custom_username = forms.CharField(max_length=150)  # 自定义的用户名字段

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_page(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('custom_username')  # 自定义的用户名字段
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # 登录成功后重定向到首页
            else:
                # 登录失败
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


class ProductListView(TemplateView):
    template_name = 'shop/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        print("Products:", products)  # 添加打印语句
        context['products'] = products
        return context

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# 產品列表視圖
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# 加入購物車視圖
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # 處理加入購物車邏輯
    return redirect('cart')

# 購物車視圖
@login_required
def cart(request):
    # 獲取購物車中的產品
    # 渲染購物車頁面
    return render(request, 'shop/cart.html', {})

# 結帳視圖
@login_required
def checkout(request):
    # 處理結帳邏輯
    return render(request, 'shop/checkout.html', {})

# 完成結帳視圖
@login_required
def complete_order(request):
    # 建立訂單
    # 重定向到訂單確認頁面
    return redirect('order_confirmation')

# 訂單確認視圖
@login_required
def order_confirmation(request):
    # 獲取最新訂單
    # 渲染訂單確認頁面
    return render(request, 'shop/order_confirmation.html', {})

# 首頁視圖
def index(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'index.html', {'user': user})


# 註冊頁面視圖
def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # 註冊成功後重定向到首頁
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 行銷頁面視圖
def marketing_page(request):
    return render(request, 'marketing/marketing.html')
