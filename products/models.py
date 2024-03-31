from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    SIZE_CHOICES = (
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
    )

    BRAND_CHOICES = (
        ('Nike', 'Nike'),
        ('Adidas', 'Adidas'),
        ('Jordan', 'Jordan'),
        ('New Balance', 'New Balance'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='YesMYdee')
    image = models.ImageField(upload_to='product_images/')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=Product.SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    min_order_quantity = models.PositiveIntegerField(default=1)  # 最小訂購量
    max_capacity = models.PositiveIntegerField(default=1000)  # 最大容量

    class Meta:
        unique_together = ('product', 'size')

@receiver(post_save, sender=Product)
def create_or_update_inventory(sender, instance, created, **kwargs):
    sizes = instance.SIZE_CHOICES
    for size in sizes:
        if created:
            Inventory.objects.create(product=instance, size=size[0], stock=0)  # 如果是新建 Product 記錄，則創建相應的 Inventory 記錄，並初始化庫存量為0
        else:
            try:
                inventory = Inventory.objects.get(product=instance, size=size[0])
                inventory.save()  # 如果是更新 Product 記錄，則同步更新相應的 Inventory 記錄
            except Inventory.DoesNotExist:
                pass  # 如果相應的庫存記錄不存在，則忽略這個尺寸的庫存


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(default=0)
    phone = models.CharField(max_length=20 , default = timezone.now)
    
    def __str__(self):
        return self.user.username
    
class EmailAddress(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email
    
class UpcomingProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='upcoming_products/')
    start_date = models.DateField()

    def __str__(self):
        return self.name

from django.db import models

class Employee(models.Model):
    profile_picture = models.ImageField(upload_to='employee_profile_pictures/', null=True, blank=True)
    employee_id = models.CharField(max_length=100, default='')  # 添加了預設值
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.employee.full_name


class Pinchwell(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)  # 新增 ordered 字段

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=Product.SIZE_CHOICES)



