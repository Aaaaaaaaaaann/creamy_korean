# Generated by Django 3.1.4 on 2020-12-27 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20201205_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='ingredientsgroup',
            options={'ordering': ['name']},
        ),
    ]
