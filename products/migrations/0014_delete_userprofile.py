# Generated by Django 3.1.2 on 2020-12-01 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_remove_ingredientsgroup_kind'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]