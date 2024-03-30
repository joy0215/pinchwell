from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_pinchwell_alter_employee_employee_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
