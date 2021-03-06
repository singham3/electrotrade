# Generated by Django 3.0.3 on 2020-05-25 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200525_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderaddress',
            name='order',
        ),
        migrations.AddField(
            model_name='orderaddress',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='delivery_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='products.OrderAddress'),
        ),
        migrations.AlterField(
            model_name='orderid',
            name='order_id',
            field=models.IntegerField(default=30932327),
        ),
    ]
