# Generated by Django 4.2.8 on 2024-01-06 05:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0001_initial'),
        ('products', '0008_product_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=100)),
                ('payment_type', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'processing'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('refunded', 'refunded'), ('on_hold', 'on_hold')], default='pending', max_length=100)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products')),
                ('date', models.DateField(default=datetime.date.today)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_address', to='user_app.address')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem_product', to='products.product')),
            ],
        ),
    ]