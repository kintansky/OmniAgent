# Generated by Django 2.1.7 on 2019-03-28 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0008_auto_20190323_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicIpGateway',
            fields=[
                ('gateway', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('mask', models.SmallIntegerField()),
            ],
        ),
    ]
