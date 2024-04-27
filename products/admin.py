from django.contrib import admin
from .models import Product, UserProfile, UpcomingProduct, Employee, Pinchwell, Inventory,SignupProfile

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'size', 'price')  # 將 'price' 添加到列表顯示中
    inlines = [InventoryInline]  # 將 InventoryInline 添加到 ProductAdmin 中


admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)
admin.site.register(UpcomingProduct)
admin.site.register(Employee)
admin.site.register(Pinchwell)
admin.site.register(SignupProfile)

