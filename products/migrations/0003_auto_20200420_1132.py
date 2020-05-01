# Generated by Django 3.0.5 on 2020-04-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200419_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'en'), ('ru', 'ru')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='kind',
            field=models.CharField(blank=True, choices=[('undesirable', 'нежелательный'), ('active', 'активный')], max_length=20, null=True),
        ),
    ]
