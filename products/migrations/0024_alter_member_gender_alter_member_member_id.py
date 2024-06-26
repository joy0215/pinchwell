# Generated by Django 4.2.6 on 2024-06-01 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_member_pincher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('M', '男性'), ('F', '女性'), ('O', '其他性別')], max_length=1),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.CharField(max_length=17, primary_key=True, serialize=False, unique=True),
        ),
    ]
