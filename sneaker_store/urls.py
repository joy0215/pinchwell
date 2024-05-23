'''

'''

from django.urls import path
from django.contrib import admin
from products import views
from django.conf import settings
from django.conf.urls.static import static
from products.views import ProductListView

urlpatterns = [
    path('', views.index, name='index'), 
    path('admin/', admin.site.urls),
    path('product_list.html', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('login/', views.login_page, name='login'),  # 登入頁面的URL
    path('signup/', views.signup, name='signup'),  # 註冊頁面的URL
    path('marketing/', views.marketing_page, name='marketing_page'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('upcoming_products/', views.upcoming_products, name='upcoming_products'),
    path('employee/login/', views.employee_login, name='employee_login'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/employee_profile/', views.employee_profile_view, name='employee_profile'),  # 將視圖函數和URL路徑匹配
    path('edit_employee_profile/', views.edit_employee_profile, name='edit_employee_profile'),
    path('edit_employee_profile/<int:employee_id>/', views.edit_employee_profile, name='edit_employee_profile'),
    path('inventory/query/', views.inventory_query, name='inventory_query'),
    path('inventory/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/update/<int:product_id>/', views.update_inventory, name='update_inventory'),
    path('testform/<int:product_id>/', views.testform_view, name='testform'),
    path('order_confirmation/', views.confirmation_view, name='order_confirmation'),
    path('low_stock_warning/', views.low_stock_warning, name='low_stock_warning'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('feedback/', views.feedback, name='feedback'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

