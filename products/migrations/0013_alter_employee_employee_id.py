# Generated by Django 4.2.6 on 2024-03-29 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_employee_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(default='', max_length=100, unique=False),
        ),
    ]
