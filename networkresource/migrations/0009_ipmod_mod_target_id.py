# Generated by Django 2.1.7 on 2019-07-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0008_auto_20190719_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipmod',
            name='mod_target_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
