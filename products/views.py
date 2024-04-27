from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Pinchwell,Order ,OrderItem ,UpcomingProduct ,Employee ,UserProfile,EmployeeProfile ,Inventory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from sneaker_store.forms import UserProfileForm,EmployeePasswordForm, EmployeeEditForm,PasswordForm, EditForm ,InventoryUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '用戶名或電子郵件'  # 修改用戶名字段標籤為“用戶名或電子郵件”


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
def login_page(request):
    form = AuthenticationForm()  # 先定義 form 變數
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 先檢查是否為 Pinchwell 使用者
        try:
            pinchwell_user = Pinchwell.objects.get(username=username)
            if pinchwell_user.check_password(password):  # 假設 PinchwellUser 有 check_password 方法
                # 如果密碼正確，則導向 dashboard
                return redirect('employee_dashboard')
        except Pinchwell.DoesNotExist:
            pass  # 如果不是 Pinchwell 使用者，則繼續檢查是否為一般使用者

        # 再檢查是否為一般使用者
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, '無效的用戶名或密碼。')

    return render(request, 'login.html', {'form': form})

import logging

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from sneaker_store.forms import SignupUserForm, SignupProfileForm
def signup(request):
    if request.method == 'POST':
        user_form = SignupUserForm(request.POST)
        profile_form = SignupProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # 加密密碼
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')  # 或者你想要導向的頁面
        else:
            print(user_form.errors, profile_form.errors)  # 印出錯誤訊息
    else:
        user_form = SignupUserForm()
        profile_form = SignupProfileForm()

    return render(request, 'signup.html', {'user_form': user_form, 'profile_form': profile_form})
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