# Generated by Django 3.0.3 on 2020-05-25 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_auto_20200524_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=73828079, max_length=20),
        ),
    ]
