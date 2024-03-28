from django.db import models
from django.contrib.auth.models import User

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

    get_price.short_description = 'Price'

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='25cm')
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='YesMYdee')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return self.user.username
    
class UpcomingProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='upcoming_products/')
    start_date = models.DateField()

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    full_name = models.CharField(max_length=200)


    def __str__(self):
        return self.full_name
    
class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)  # 新增 ordered 字段

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=Product.SIZE_CHOICES)



