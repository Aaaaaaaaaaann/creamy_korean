# Generated by Django 3.0.7 on 2020-10-22 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20201005_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientsgroup',
            name='kind',
        ),
    ]