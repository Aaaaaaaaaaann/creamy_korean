# Generated by Django 3.0.5 on 2020-04-25 09:13

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20200425_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('kind', models.CharField(blank=True, choices=[('нежелательные', 'Undesirable'), ('активные', 'Active')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('brand', models.TextField()),
                ('volume', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('slug', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('available_regions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
                ('free_courier_delivery', models.TextField(blank=True, null=True)),
                ('link_to_delivery_conditions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SectionTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), blank=True, null=True, size=None)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='section_temp', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='products.Section')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.BooleanField(default=False)),
                ('current_price', models.IntegerField(blank=True, null=True)),
                ('link_to_product_page', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='available_in_shops', to='products.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.Section'),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('function', models.TextField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ingredients', to='products.IngredientsGroup')),
            ],
        ),
        migrations.CreateModel(
            name='CompositionTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composition', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='composition_temp', to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composition', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='composition', to='products.Product')),
            ],
        ),
    ]
