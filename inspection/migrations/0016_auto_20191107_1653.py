# Generated by Django 2.2.5 on 2019-11-07 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0015_linkpingcoststepaggregate'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='linkpingtest',
            index=models.Index(fields=['source_device'], name='OM_REP_ping_source__702db1_idx'),
        ),
        migrations.AddIndex(
            model_name='linkpingtest',
            index=models.Index(fields=['target_device'], name='OM_REP_ping_target__ccd352_idx'),
        ),
    ]