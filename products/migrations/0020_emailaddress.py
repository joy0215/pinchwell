# Generated by Django 4.2.6 on 2024-03-31 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_inventory_size_alter_orderitem_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.userprofile')),
            ],
        ),
    ]
