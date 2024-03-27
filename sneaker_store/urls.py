# urls.py

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
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('login/', views.login_page, name='login'),  # 登入頁面的URL
    path('register/', views.register, name='register'),  # 註冊頁面的URL
    path('marketing/', views.marketing_page, name='marketing_page'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)