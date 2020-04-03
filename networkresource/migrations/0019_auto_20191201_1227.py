# Generated by Django 2.2.5 on 2019-12-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0018_auto_20191201_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupClientIpReserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subnet_gateway', models.GenericIPAddressField()),
                ('subnet_mask', models.PositiveSmallIntegerField()),
                ('reserved_cnt', models.PositiveIntegerField()),
                ('reserved_person', models.CharField(max_length=20)),
                ('contact', models.EmailField(max_length=254)),
                ('reserved_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'MR_REC_group_client_ip_reserve',
            },
        ),
        migrations.AddIndex(
            model_name='groupclientipreserve',
            index=models.Index(fields=['subnet_gateway'], name='MR_REC_grou_subnet__ff7113_idx'),
        ),
    ]
