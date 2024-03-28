from django.contrib import admin
from .models import Product, UserProfile, UpcomingProduct, Employee

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('size',)  # 確保這裡引用的 'size' 與模型中的字段名稱完全一致
    # 在列表中顯示名稱、描述和價格
    list_display = ('name', 'description', 'display_price')  
    # 在側邊欄中添加尺寸過濾器
    list_filter = ('size',)  # 確保這裡引用了 'size' 字段  
    # 在搜尋欄中添加名稱、描述和尺寸搜索
    search_fields = ('name', 'description', 'size')  
    # 將價格設定為只讀字段，以防止在後台修改
    readonly_fields = ('display_price',)  

    def display_price(self, obj):
        return obj.get_price()
    display_price.short_description = '價格'


admin.site.register(Product, ProductAdmin)

# 註冊其他模型
admin.site.register(UserProfile)
admin.site.register(UpcomingProduct)
admin.site.register(Employee)
