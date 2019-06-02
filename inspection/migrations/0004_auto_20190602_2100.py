# Generated by Django 2.1.7 on 2019-06-02 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0003_porterrordiff_fix_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porterrordiff',
            name='everCRC',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='everIpv4HeaderError',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='nowCRC',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='nowIpv4HeaderError',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='stateCRC',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='porterrordiff',
            name='stateIpv4HeadError',
            field=models.FloatField(null=True),
        ),
    ]
