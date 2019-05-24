# Generated by Django 2.1.7 on 2019-05-24 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0004_onewaydevice'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='onewaydevice',
            index=models.Index(fields=['device_name'], name='inspection__device__8dba78_idx'),
        ),
        migrations.AddIndex(
            model_name='onewaydevice',
            index=models.Index(fields=['port'], name='inspection__port_f434c1_idx'),
        ),
    ]
