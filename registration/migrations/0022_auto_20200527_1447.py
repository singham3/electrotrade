# Generated by Django 3.0.3 on 2020-05-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_auto_20200527_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=12626636, max_length=20),
        ),
    ]
