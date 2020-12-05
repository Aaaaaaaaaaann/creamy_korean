# Generated by Django 3.1.2 on 2020-12-05 13:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20201203_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='exclude_ingrs_groups',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='include_ingrs_groups',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]
