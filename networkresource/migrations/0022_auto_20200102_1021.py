# Generated by Django 3.0.1 on 2020-01-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0021_auto_20191205_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipallocation',
            name='group_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ipallocation',
            name='product_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ipmod',
            name='group_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ipmod',
            name='product_id',
            field=models.BigIntegerField(default=0),
        ),
    ]