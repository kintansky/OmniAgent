# Generated by Django 2.1.7 on 2019-04-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0005_porterrordiff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porterrordiff',
            name='stateCRC',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='stateIpv4HeadError',
            field=models.FloatField(),
        ),
    ]
