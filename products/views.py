from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Member ,UpcomingProduct ,Employee ,EmployeeProfile ,Inventory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView ,View 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate , logout
from sneaker_store.forms import UserProfileForm,EmployeePasswordForm, EmployeeEditForm,FeedbackForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from .cart import Cart
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Member


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['username', 'email', 'phone_number', 'birthdate', 'gender', 'bio']
    template_name = 'member_edit.html'
    success_url = reverse_lazy('index')  # 編輯成功後重定向到主頁

    def get_object(self, queryset=None):
        return self.request.user  # 返回當前登入的用戶

def logout_view(request):
    logout(request)
    return redirect('login')  # 登出後重定向到主頁或其他頁面


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用戶名或電子郵件'  # 修改用戶名字段標籤為“用戶名或電子郵件”


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Member  # 假設你的使用者模型是 Member

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('index')  # 重定向到主頁
        else:
            messages.error(request, '無效的用戶名或密碼。')

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from sneaker_store.forms import SignupForm

from django.contrib.auth.hashers import make_password

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            member = form.save(commit=False)
            password = form.cleaned_data.get('password')  # 獲取密碼
            member.password = make_password(password)  # 加密密碼
            member.save()

            # 使用 messages 來傳遞客戶編號
            messages.success(request, f'註冊成功！您的客戶編號是 {member.member_id}')
            return redirect('signup')  # 導向到註冊頁面，這樣可以顯示彈窗
        else:
            print(form.errors)  # 印出錯誤訊息
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# 商品列表視圖
class ProductListView(TemplateView):
    template_name = 'shop/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context

#即將發售商品日曆視圖
def upcoming_products(request):
    upcoming_products = UpcomingProduct.objects.all()
    return render(request, 'shop/upcoming_products.html', {'upcoming_products': upcoming_products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(username=username)
            if employee.password == password:
                # 登入成功，重定向到員工儀表板
                login(request, employee)
                messages.success(request, '員工登入成功!')
                return redirect('employee_dashboard')  # 重定向到員工儀表板視圖
            else:
                messages.error(request, '密碼錯誤，請再試一次')
        except Employee.DoesNotExist:
            messages.error(request, '員工帳號並不存在，請聯繫主管')
    
    return render(request, 'employee_login.html')

@login_required
def employee_profile(request):
    try:
        employee_profile = EmployeeProfile.objects.get(user=request.user)  # 根據用戶查詢 EmployeeProfile
        employee = employee_profile.employee  # 獲取相關聯的 Employee 物件
    except EmployeeProfile.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('index')  # 如果找不到相應的 EmployeeProfile，重定向到首頁或其他頁面

    if request.method == 'POST':
        password_form = EmployeePasswordForm(request.POST)
        if password_form.is_valid():
            edit_form = EmployeeEditForm(request.POST, request.FILES, instance=employee)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Employee data updated successfully.')
                return redirect('employee_profile')
        else:
            messages.error(request, 'Unable to verify password')
    else:
        password_form = EmployeePasswordForm(initial={'username': request.user.username})
        edit_form = EmployeeEditForm(instance=employee)

    return render(request, 'employee_profile.html', {'password_form': password_form, 'edit_form': edit_form})

def low_stock_warning(request):
    low_stock_products = Inventory.objects.filter(stock__lt=5)
    all_products = Product.objects.all()  # 獲取所有球鞋

    context = {
        'low_stock_products': low_stock_products,
        'all_products': all_products,  # 將所有球鞋傳遞到模板中
    }

    return render(request, 'low_stock_warning.html', context)

@login_required
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    size = request.POST.get('size')
    if not size:
        messages.error(request, "Please select a size.")
        return redirect('product_detail', product_id=product_id)
    cart = Cart(request)
    cart.add(product=product, size=size)
    messages.success(request, "Product added to cart successfully.")
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        
        if size and quantity:
            try:
                quantity = int(quantity)
                cart = Cart(request)
                cart.add(product=product, size=size, quantity=quantity, update_quantity=True)
                messages.success(request, "Cart updated successfully.")
            except ValueError:
                messages.error(request, "Invalid quantity. Please enter a valid number.")
        else:
            messages.error(request, "Size or quantity is missing.")
    return redirect('cart')

import logging

logger = logging.getLogger(__name__)

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size')
        if size:
            cart = Cart(request)
            cart.remove(product_id, size)
            messages.success(request, "Product removed from cart successfully.")
            if cart.is_empty():
                messages.info(request, "Your cart is now empty.")
            return redirect('cart')
        else:
            return JsonResponse({'error': 'Invalid request. Please provide size.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request. Please use POST method.'}, status=400)
    
@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

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

@login_required
def edit(request):
    return render(request, 'edit.html')

class OrdersView(View):
    def get(self, request):
            # 处理获取订单的逻辑
            return render(request, 'shop/cart.html')  # 渲染订单页面模板

from django.contrib.auth.forms import UserCreationForm

# 行銷頁面視圖
def marketing_page(request):
    return render(request, 'marketing/marketing.html')


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_thanks')
    else:
        form = FeedbackForm()

    return render(request, 'marketing/feedback.html', {'form': form})

def feedback_thanks(request):
    return render(request, 'shop/feedback_thanks.html')


def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(username=username)
            if employee.password == password:
                # 登入成功，可以执行其他操作，如设置登入状态等
                messages.success(request, '員工登入成功!')
                return redirect('index')  # 重定向到首页或其他页面
            else:
                messages.error(request, '密碼錯誤，請再試一次')
        except Employee.DoesNotExist:
            messages.error(request, '員工帳號並不存在，請聯繫主管')
    
    return render(request, 'employee_login.html')

def employee_profile_view(request):
    employees = Employee.objects.all() 
    return render(request, 'employee_profile.html', {'employees': employees})


def edit_employee_profile(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_profile')  # 重定向到員工資料頁面
    else:
        form = EmployeeEditForm(instance=employee)
    return render(request, 'edit_employee_profile.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Inventory, Product

def inventory_query(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        size = request.POST.get('size')

        inventories = Inventory.objects.all()

        if product_name:
            inventories = inventories.filter(product__name__icontains=product_name)
        if brand:
            inventories = inventories.filter(product__brand__icontains=brand)
        if size:
            inventories = inventories.filter(size__icontains=size)

        context = {'inventories': inventories}
        return render(request, 'inventory_query.html', context)
    else:
        inventories = Inventory.objects.none()
        context = {'inventories': inventories}
        return render(request, 'inventory_query.html', context)

from .models import Product, Inventory


def inventory_edit(request):
    products = Product.objects.all()  # 獲取所有產品
    total_stocks = {product.id: product.inventory_set.aggregate(total_stock=Sum('stock'))['total_stock'] for product in products}
    context = {
        'products': products,
        'total_stocks': total_stocks,
    }
    return render(request, 'inventory_edit.html', context)

def testform_view(request, product_id):
    # 獲取所有尺碼的庫存數據，以字典形式傳遞到模板
    inventory_data = {}
    inventory_records = Inventory.objects.filter(product_id=product_id)
    for record in inventory_records:
        inventory_data[record.size] = record.stock  # 更新此處獲取的屬性名稱

    return render(request, 'testform.html', {'inventory_data': inventory_data, 'product_id': product_id})

def update_inventory(request, product_id):
    if request.method == 'POST':
        # 更新庫存數據
        for key, value in request.POST.items():
            if key.startswith('size_'):
                size = key.split('_')[1]
                quantity = int(value)
                inventory, created = Inventory.objects.get_or_create(product_id=product_id, size=size)
                if created:
                    inventory.stock = quantity
                else:
                    inventory.stock += quantity
                inventory.save()
        # 提取返回鏈接
        return_link = request.POST.get('return_link', 'inventory/edit/')  # 使用返回鏈接或默認為首頁
        return redirect(return_link)  # 重定向到返回鏈接
    
    # 如果沒有成功更新，返回空數據
    return JsonResponse({}, status=400)


def confirmation_view(request):
    # 在這裡可以處理接收到的表單數據，並根據需要進行相應的處理
    # 例如，保存訂單到數據庫等操作
    if request.method == 'POST':
        # 處理POST請求，例如保存表單數據
        pass
    else:
        # 如果是GET請求，則渲染checkout.html模板
        return render(request, 'order_confirmation.html')
def orders(request):

    return render(request, 'pinchwell/orders.html')

def record(request):
    return render(request, 'shop/choose.html')