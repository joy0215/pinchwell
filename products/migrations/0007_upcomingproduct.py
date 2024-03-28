# Generated by Django 5.0.3 on 2024-03-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='upcoming_products/')),
                ('start_date', models.DateField()),
            ],
        ),
    ]
