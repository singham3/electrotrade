# Generated by Django 3.0.3 on 2020-05-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20200519_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=24147880, max_length=20),
        ),
    ]
