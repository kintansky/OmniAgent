# Generated by Django 3.0.5 on 2020-04-20 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0029_groupclientipreserve_delay_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupclientipreserve',
            name='expire_time',
            field=models.DateTimeField(null=True),
        ),
    ]
