# 引入Django模組
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

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

def index(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')

def marketing_page(request):
    return render(request, 'marketing/marketing.html')
