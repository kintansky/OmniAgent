# Generated by Django 2.1.7 on 2019-06-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0004_auto_20190602_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='NatPoolUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device1', models.CharField(max_length=255)),
                ('device1_nat_usage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('device2', models.CharField(max_length=255)),
                ('device2_nat_usage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('record_time', models.DateTimeField()),
            ],
            options={
                'ordering': ['-record_time'],
            },
        ),
    ]
