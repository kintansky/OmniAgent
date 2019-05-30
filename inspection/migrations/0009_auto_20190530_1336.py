# Generated by Django 2.1.7 on 2019-05-30 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0008_auto_20190530_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porterrordiff',
            name='record_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddIndex(
            model_name='porterrordiff',
            index=models.Index(fields=['port'], name='inspection__port_885f82_idx'),
        ),
    ]
