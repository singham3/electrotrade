# Generated by Django 3.0.3 on 2020-05-29 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_auto_20200527_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=43714056, max_length=20),
        ),
    ]
