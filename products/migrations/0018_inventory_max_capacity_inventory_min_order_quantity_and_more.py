# Generated by Django 4.2.6 on 2024-03-30 08:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_userprofile_birthdate_alter_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='max_capacity',
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='inventory',
            name='min_order_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
        ),
    ]
