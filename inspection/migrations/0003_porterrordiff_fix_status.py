# Generated by Django 2.1.7 on 2019-06-02 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0002_auto_20190602_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='porterrordiff',
            name='fix_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
