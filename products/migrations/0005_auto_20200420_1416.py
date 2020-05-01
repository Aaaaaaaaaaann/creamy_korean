# Generated by Django 3.0.5 on 2020-04-20 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200420_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='composition', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='originalsection',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='original_section', to='products.Product'),
        ),
    ]
