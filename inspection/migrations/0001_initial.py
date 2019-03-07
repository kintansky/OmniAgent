# Generated by Django 2.1.7 on 2019-03-07 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpticalMoudleDiff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=40)),
                ('now_moudle', models.CharField(max_length=60)),
                ('ever_moudle', models.CharField(max_length=60)),
                ('status', models.CharField(choices=[('NEW', 'plugin'), ('MISS', 'missing'), ('CH', 'changed')], max_length=20)),
                ('record_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-record_time'],
            },
        ),
    ]
