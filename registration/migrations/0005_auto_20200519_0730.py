# Generated by Django 3.0.3 on 2020-05-19 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20200519_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=85894022, max_length=20),
        ),
    ]
