# Generated by Django 3.0.3 on 2020-05-19 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0004_auto_20200519_0729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(blank=True, max_length=250, null=True)),
                ('search_count', models.IntegerField(default=0)),
                ('search_result_status', models.BooleanField(default=False)),
                ('search_result_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='registration.Register')),
            ],
        ),
        migrations.CreateModel(
            name='EnquiryForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250)),
                ('product_company', models.CharField(max_length=250)),
                ('product_series_num', models.CharField(blank=True, max_length=200, null=True)),
                ('prod_description', models.TextField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='registration.Register')),
            ],
        ),
    ]
