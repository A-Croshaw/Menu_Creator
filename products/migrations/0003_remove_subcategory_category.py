# Generated by Django 5.1 on 2024-08-12 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_rename_product_cost_product_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
    ]
