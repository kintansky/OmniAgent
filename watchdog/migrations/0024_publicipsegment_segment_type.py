# Generated by Django 2.1.7 on 2019-04-19 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0023_auto_20190410_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicipsegment',
            name='segment_type',
            field=models.IntegerField(default=1),
        ),
    ]