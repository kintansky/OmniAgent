# Generated by Django 2.1.7 on 2019-04-04 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0006_auto_20190403_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='porterrordiff',
            options={'ordering': ['-record_time', '-stateIpv4HeadError', '-stateCRC']},
        ),
    ]