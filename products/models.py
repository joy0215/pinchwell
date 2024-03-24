from django.db import models

class Product(models.Model):
    SIZE_CHOICES = (
        ('25cm', 'US 7'),
        ('25.5cm', 'US 7.5'),
        ('26cm', 'US 8'),
        ('26.5cm', 'US 8.5'),
        ('27cm', 'US 9'),
        ('27.5cm', 'US 9.5'),
        ('28cm', 'US 10'),
        ('28.5cm', 'US 10.5'),
        ('29cm', 'US 11'),
        ('29.5cm', 'US 11.5'),
        ('30cm', 'US 12'),
        ('31cm', 'US 13'),
    )

    BRAND_CHOICES = (
        ('Nike', 'Nike'),
        ('Adidas', 'Adidas'),
        ('Jordan', 'Jordan'),
        ('New Balance', 'New Balance'),
    )
    
    def get_price(self):
        return self.price

    get_price.short_description = 'Price'  # 修改顯示在管理界面中的欄位名稱

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='25cm')
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='YesMYdee')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Order(models.Model):
    products = models.ManyToManyField(Product)  # 訂單中的產品
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 訂單總價
    shipping_address = models.TextField()  # 運送地址
    created_at = models.DateTimeField(auto_now_add=True)  # 訂單建立時間
