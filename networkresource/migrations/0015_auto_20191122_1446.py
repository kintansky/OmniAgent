# Generated by Django 2.2.5 on 2019-11-22 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0014_auto_20191028_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupClientIPSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('ip_state', models.BooleanField(default=False)),
                ('segment', models.GenericIPAddressField()),
                ('mask', models.PositiveSmallIntegerField()),
                ('segment_state', models.BooleanField(default=False)),
                ('subnet_gateway', models.GenericIPAddressField(null=True)),
                ('subnet_mask', models.PositiveSmallIntegerField(null=True)),
                ('ip_func', models.CharField(max_length=2, null=True)),
            ],
            options={
                'db_table': 'MR_REC_group_client_ip_segment',
            },
        ),
        migrations.CreateModel(
            name='GroupClientPublicGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.GenericIPAddressField()),
                ('olt_cnt', models.PositiveIntegerField(default=0)),
                ('olts', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'MR_STS_group_client_public_gateway',
            },
        ),
        migrations.CreateModel(
            name='SwVlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=30)),
                ('vlan', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'MR_REC_sw_vlan',
            },
        ),
        migrations.DeleteModel(
            name='PublicIpGateway',
        ),
        migrations.AddIndex(
            model_name='groupclientipsegment',
            index=models.Index(fields=['segment'], name='MR_REC_grou_segment_fb2adb_idx'),
        ),
        migrations.AddIndex(
            model_name='groupclientipsegment',
            index=models.Index(fields=['subnet_gateway'], name='MR_REC_grou_subnet__9a8f9c_idx'),
        ),
    ]
