# Generated by Django 3.0.5 on 2020-04-19 14:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsgroup',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='originalsection',
            name='section',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='volume',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
