# Generated by Django 3.0.3 on 2020-05-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0024_auto_20200529_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=47100999, max_length=20),
        ),
    ]