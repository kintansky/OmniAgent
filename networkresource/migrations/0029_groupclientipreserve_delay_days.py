# Generated by Django 3.0.5 on 2020-04-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0028_ipmod_icp'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupclientipreserve',
            name='delay_days',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]