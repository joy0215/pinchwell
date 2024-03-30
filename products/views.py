from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order ,OrderItem ,UpcomingProduct ,Employee ,UserProfile,EmployeeProfile ,Inventory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from sneaker_store.forms import UserProfileForm,EmployeePasswordForm, EmployeeEditForm,PasswordForm, EditForm
from django.contrib.auth.decorators import login_required

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用戶名或電子郵件'  # 修改用戶名字段標籤為“用戶名或電子郵件”


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import authenticate, login

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('employee_dashboard')
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

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # 儲存用戶
            profile = profile_form.save(commit=False)
            profile.user = user  # 關聯用戶資料到用戶
            profile.save()  # 儲存用戶資料
            messages.success(request, 'Registration successful!')
            return redirect('index')
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



@login_required
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')

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

def inventory_query(request):
    if request.method == 'POST':
        # 接收來自前端的查詢條件
        product_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        size = request.POST.get('size')

        # 根據查詢條件查詢庫存信息
        inventories = Inventory.objects.all()

        if product_name:
            inventories = inventories.filter(product__name__icontains=product_name)
        if brand:
            inventories = inventories.filter(product__brand__icontains=brand)
        if size:
            inventories = inventories.filter(size__icontains=size)

        # 將庫存信息傳遞給模板
        context = {'inventories': inventories}
        return render(request, 'inventory_query.html', context)
    else:
        # 如果是 GET 請求，返回空的庫存列表
        inventories = Inventory.objects.none()
        context = {'inventories': inventories}
        return render(request, 'inventory_query.html', context)
