# Generated by Django 2.2.5 on 2019-12-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0019_auto_20191201_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupclientipreserve',
            name='client_name',
            field=models.CharField(default='', max_length=225),
            preserve_default=False,
        ),
    ]
