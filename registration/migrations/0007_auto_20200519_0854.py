# Generated by Django 3.0.3 on 2020-05-19 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20200519_0733'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='register',
            name='alternate_mobile',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AddField(
            model_name='register',
            name='business_description',
            field=models.TextField(blank=True, max_length=15000, null=True),
        ),
        migrations.AddField(
            model_name='register',
            name='business_name',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='account_id',
            field=models.CharField(default=80514744, max_length=20),
        ),
        migrations.AddField(
            model_name='register',
            name='business_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='registration.BusinessType'),
        ),
    ]
