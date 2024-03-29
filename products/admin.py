from django.contrib import admin
from .models import Product, UserProfile, UpcomingProduct, Employee , Pinchwell


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'size', 'price')  # 將 'price' 添加到列表顯示中

admin.site.register(Product, ProductAdmin)

# 註冊其他模型
admin.site.register(UserProfile)
admin.site.register(UpcomingProduct)
admin.site.register(Employee)
admin.site.register(Pinchwell)
