# Generated by Django 2.1.7 on 2019-07-14 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0003_auto_20190708_2146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipallocation',
            old_name='client_id',
            new_name='product_id',
        ),
    ]
