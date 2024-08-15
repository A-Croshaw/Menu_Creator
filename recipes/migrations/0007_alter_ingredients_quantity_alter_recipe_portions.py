# Generated by Django 5.1 on 2024-08-15 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_method_steps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='quantity',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='portions',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
