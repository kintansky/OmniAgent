# Generated by Django 2.2.5 on 2019-10-28 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='commandline',
            table='MR_REC_cmd_line',
        ),
        migrations.AlterModelTable(
            name='device',
            table='MR_REC_watchdog_device',
        ),
        migrations.AlterModelTable(
            name='devicemanufactor',
            table='MR_REC_device_manufactor',
        ),
    ]
