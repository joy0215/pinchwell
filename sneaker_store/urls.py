"""
URL configuration for sneaker_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 引入Django模組
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
    path('login/', views.login_page, name='login'),
    path('marketing/', views.marketing_page, name='marketing_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)