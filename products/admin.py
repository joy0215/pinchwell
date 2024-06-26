from django.contrib import admin
from .models import Product, UpcomingProduct, Inventory,Member,Pincher,Feedback

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'size', 'price')  # 將 'price' 添加到列表顯示中
    inlines = [InventoryInline]  # 將 InventoryInline 添加到 ProductAdmin 中


admin.site.register(Product, ProductAdmin)
admin.site.register(UpcomingProduct)
admin.site.register(Member)
admin.site.register(Pincher)
admin.site.register(Feedback)
