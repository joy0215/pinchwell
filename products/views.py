# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order ,OrderItem
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages

class CustomAuthenticationForm(AuthenticationForm):
    custom_username = forms.CharField(max_length=150)  # 自訂用戶名欄位

def login_page(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('custom_username')  # 自訂用戶名欄位
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # 登錄成功後重新導向到首頁
            else:
                # 登錄失敗
                return render(request, 'login.html', {'form': form, 'error_message': '無效的用戶名或密碼。'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

class ProductListView(TemplateView):
    template_name = 'shop/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})



def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        # 獲取選擇的尺寸
        selected_size = request.POST.get('size')
        # 創建訂單或者從現有訂單中獲取
        order, created = Order.objects.get_or_create(user=request.user, ordered=False)
        # 添加產品到訂單
        order.products.add(product)
        # 創建訂單項目
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product, size=selected_size)
        # 顯示成功訊息
        messages.success(request, '商品已成功添加到購物車！')
        return redirect('product_detail', pk=pk)
    else:
        return redirect('product_detail', pk=pk)


@login_required
def cart(request):
    # 获取购物车中的商品
    cart_items = []  # 假设这是购物车中的商品列表，这里应根据您的实际逻辑来获取购物车中的商品
    total_price = sum(item.price for item in cart_items) if cart_items else 0
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    # 處理結帳邏輯
    return render(request, 'shop/checkout.html', {})

@login_required
def complete_order(request):
    # 建立訂單
    # 重定向到訂單確認頁面
    return redirect('order_confirmation')

@login_required
def order_confirmation(request):
    # 獲取最新訂單
    # 渲染訂單確認頁面
    return render(request, 'shop/order_confirmation.html', {})

def index(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'index.html', {'user': user})

def register_page(request):
    # 註冊頁面邏輯
    return render(request, 'register.html', {})

def marketing_page(request):
    return render(request, 'marketing/marketing.html')

