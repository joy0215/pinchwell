# Generated by Django 4.2.6 on 2024-03-30 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_remove_userprofile_email_remove_userprofile_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default='2000-01-01'),  # 使用您選擇的特定日期作為默認值
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),  # 確保這裡沒有默認值問題
        ),
    ]

