from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'size', 'display_price')  # 在列表中顯示價格
    list_filter = ('size',)  # 在側邊欄中添加過濾器
    search_fields = ('name', 'description', 'size')  # 在搜尋欄中添加尺寸搜索
    readonly_fields = ('display_price',)  # 將價格設定為只讀字段，以防止在後台修改
    
    list_display = ('name', 'description', 'get_price')  # 將 get_price 方法添加到 list_display 中
    # your other admin options here
    
    
    def display_price(self, obj):
        return obj.get_price()
    display_price.short_description = 'Price'

admin.site.register(Product, ProductAdmin)

from .models import UserProfile
admin.site.register(UserProfile)

from .models import UpcomingProduct
admin.site.register(UpcomingProduct)

from .models import Employee
admin.site.register(Employee)

