# Generated by Django 4.2.6 on 2024-03-23 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('Nike', 'Nike'), ('Adidas', 'Adidas'), ('Jordan', 'Jordan'), ('New Balance', 'New Balance')], default='YesMYdee', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('25cm', 'US 7'), ('25.5cm', 'US 7.5'), ('26cm', 'US 8'), ('26.5cm', 'US 8.5'), ('27cm', 'US 9'), ('27.5cm', 'US 9.5'), ('28cm', 'US 10'), ('28.5cm', 'US 10.5'), ('29cm', 'US 11'), ('29.5cm', 'US 11.5'), ('30cm', 'US 12'), ('31cm', 'US 13')], default='25cm', max_length=10),
        ),
    ]
