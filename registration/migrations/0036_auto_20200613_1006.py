# Generated by Django 3.0.3 on 2020-06-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0035_auto_20200613_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=64266908, max_length=20),
        ),
    ]