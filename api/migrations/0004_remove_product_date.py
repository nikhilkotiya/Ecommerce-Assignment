# Generated by Django 3.2.5 on 2022-01-16 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_product_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='date',
        ),
    ]
