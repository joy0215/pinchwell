# Generated by Django 4.2.6 on 2024-03-28 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('25cm', 'US 7'), ('25.5cm', 'US 7.5'), ('26cm', 'US 8'), ('26.5cm', 'US 8.5'), ('27cm', 'US 9'), ('27.5cm', 'US 9.5'), ('28cm', 'US 10'), ('28.5cm', 'US 10.5'), ('29cm', 'US 11'), ('29.5cm', 'US 11.5'), ('30cm', 'US 12'), ('31cm', 'US 13')], max_length=10),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('25cm', 'US 7'), ('25.5cm', 'US 7.5'), ('26cm', 'US 8'), ('26.5cm', 'US 8.5'), ('27cm', 'US 9'), ('27.5cm', 'US 9.5'), ('28cm', 'US 10'), ('28.5cm', 'US 10.5'), ('29cm', 'US 11'), ('29.5cm', 'US 11.5'), ('30cm', 'US 12'), ('31cm', 'US 13')], max_length=10)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'unique_together': {('product', 'size')},
            },
        ),
    ]