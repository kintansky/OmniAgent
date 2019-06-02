# Generated by Django 2.1.7 on 2019-06-01 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpmanResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('slot', models.SmallIntegerField()),
                ('slot_type', models.CharField(max_length=40)),
                ('mda', models.SmallIntegerField()),
                ('mda_type', models.CharField(max_length=40)),
                ('port', models.CharField(max_length=30)),
                ('brand_width', models.CharField(max_length=20)),
                ('port_status', models.CharField(max_length=10)),
                ('port_phy_status', models.CharField(max_length=10)),
                ('logic_port', models.CharField(max_length=20)),
                ('logic_port_description', models.TextField()),
                ('port_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IpRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_ip', models.GenericIPAddressField()),
                ('ip_mask', models.IntegerField(null=True)),
                ('gateway', models.GenericIPAddressField(null=True)),
                ('device_name', models.CharField(max_length=255)),
                ('logic_port', models.CharField(max_length=40)),
                ('logic_port_num', models.CharField(max_length=40, null=True)),
                ('svlan', models.CharField(max_length=30)),
                ('cvlan', models.CharField(max_length=30)),
                ('ip_description', models.TextField(blank=True)),
                ('ip_type', models.CharField(choices=[('private', 'Private'), ('public_outer', 'PublicOuter'), ('public_inner', 'PublicInner')], max_length=20)),
                ('record_time', models.DateTimeField()),
                ('ip_func', models.CharField(max_length=40, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PrivateIpAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(blank=True, max_length=50, null=True)),
                ('community', models.CharField(blank=True, max_length=50, null=True)),
                ('service_id', models.CharField(blank=True, max_length=50, null=True)),
                ('rd', models.CharField(blank=True, max_length=50, null=True)),
                ('rt', models.CharField(blank=True, max_length=50, null=True)),
                ('order_num', models.CharField(blank=True, max_length=255, null=True)),
                ('client_name', models.CharField(max_length=255)),
                ('client_num', models.CharField(max_length=100)),
                ('product_num', models.CharField(max_length=100)),
                ('device_name', models.CharField(max_length=255)),
                ('logic_port', models.CharField(max_length=40)),
                ('svlan', models.CharField(max_length=30)),
                ('cvlan', models.CharField(max_length=30)),
                ('olt_name', models.CharField(blank=True, max_length=255, null=True)),
                ('access_type', models.CharField(blank=True, max_length=10, null=True)),
                ('ip', models.GenericIPAddressField()),
                ('gateway', models.GenericIPAddressField(null=True)),
                ('ipsegment', models.CharField(max_length=100, null=True)),
                ('ip_description', models.TextField(blank=True, null=True)),
                ('alc_user', models.CharField(max_length=100, null=True)),
                ('alc_time', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-alc_time'],
            },
        ),
        migrations.CreateModel(
            name='PrivateIpModRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_order', models.CharField(max_length=255)),
                ('mod_msg', models.TextField()),
                ('mod_user', models.CharField(max_length=100, null=True)),
                ('record_time', models.DateTimeField(auto_now_add=True)),
                ('ever_service', models.CharField(blank=True, max_length=50, null=True)),
                ('ever_community', models.CharField(blank=True, max_length=50, null=True)),
                ('ever_service_id', models.CharField(blank=True, max_length=50, null=True)),
                ('ever_rd', models.CharField(blank=True, max_length=50, null=True)),
                ('ever_rt', models.CharField(blank=True, max_length=50, null=True)),
                ('ever_client_name', models.CharField(max_length=255, null=True)),
                ('ever_client_num', models.CharField(max_length=100, null=True)),
                ('ever_product_num', models.CharField(max_length=100, null=True)),
                ('ever_device_name', models.CharField(max_length=255, null=True)),
                ('ever_logic_port', models.CharField(max_length=40, null=True)),
                ('ever_svlan', models.CharField(max_length=30, null=True)),
                ('ever_cvlan', models.CharField(max_length=30, null=True)),
                ('ever_olt_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ever_access_type', models.CharField(blank=True, max_length=10, null=True)),
                ('ever_ip', models.GenericIPAddressField(null=True)),
                ('ever_gateway', models.GenericIPAddressField(null=True)),
                ('ever_ipsegment', models.CharField(max_length=100, null=True)),
                ('ever_ip_description', models.TextField(blank=True, null=True)),
                ('ever_state', models.CharField(max_length=10, null=True)),
            ],
            options={
                'ordering': ['-record_time'],
            },
        ),
        migrations.CreateModel(
            name='PublicIpAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ies', models.CharField(blank=True, max_length=20, null=True)),
                ('order_num', models.CharField(blank=True, max_length=255, null=True)),
                ('client_num', models.CharField(max_length=100)),
                ('product_num', models.CharField(max_length=100)),
                ('ip', models.GenericIPAddressField()),
                ('mask', models.SmallIntegerField()),
                ('gateway', models.CharField(max_length=100)),
                ('link_tag', models.SmallIntegerField(blank=True, null=True)),
                ('device_name', models.CharField(max_length=255)),
                ('logic_port', models.CharField(max_length=40)),
                ('svlan', models.CharField(max_length=30)),
                ('cvlan', models.CharField(blank=True, max_length=30, null=True)),
                ('access_type', models.CharField(blank=True, max_length=10, null=True)),
                ('olt_name', models.CharField(blank=True, max_length=255, null=True)),
                ('client_name', models.CharField(max_length=255)),
                ('ip_description', models.TextField(blank=True, null=True)),
                ('up_brandwidth', models.SmallIntegerField(blank=True, null=True)),
                ('down_brandwidth', models.SmallIntegerField()),
                ('alc_user', models.CharField(max_length=100, null=True)),
                ('alc_time', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-alc_time'],
            },
        ),
        migrations.CreateModel(
            name='PublicIpGateway',
            fields=[
                ('gateway', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('mask', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicIpModRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mod_order', models.CharField(max_length=255)),
                ('mod_msg', models.TextField()),
                ('mod_user', models.CharField(max_length=100, null=True)),
                ('record_time', models.DateTimeField(auto_now_add=True)),
                ('ever_ies', models.CharField(blank=True, max_length=20, null=True)),
                ('ever_client_num', models.CharField(max_length=100, null=True)),
                ('ever_product_num', models.CharField(max_length=100, null=True)),
                ('ever_ip', models.GenericIPAddressField(null=True)),
                ('ever_mask', models.SmallIntegerField(null=True)),
                ('ever_gateway', models.CharField(max_length=100, null=True)),
                ('ever_link_tag', models.SmallIntegerField(blank=True, null=True)),
                ('ever_device_name', models.CharField(max_length=255, null=True)),
                ('ever_logic_port', models.CharField(max_length=40, null=True)),
                ('ever_svlan', models.CharField(max_length=30, null=True)),
                ('ever_cvlan', models.CharField(blank=True, max_length=30, null=True)),
                ('ever_access_type', models.CharField(blank=True, max_length=10, null=True)),
                ('ever_olt_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ever_client_name', models.CharField(max_length=255, null=True)),
                ('ever_ip_description', models.TextField(blank=True, null=True)),
                ('ever_up_brandwidth', models.SmallIntegerField(blank=True, null=True)),
                ('ever_down_brandwidth', models.SmallIntegerField(null=True)),
                ('ever_state', models.CharField(max_length=10, null=True)),
            ],
            options={
                'ordering': ['-record_time'],
            },
        ),
        migrations.CreateModel(
            name='PublicIpSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_segment', models.GenericIPAddressField()),
                ('mask', models.IntegerField()),
                ('segment_type', models.IntegerField(choices=[(-1, '私网'), (1, '公网外部使用'), (2, '公网内部使用')], default=1)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ZxClientInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.BigIntegerField(null=True)),
                ('client_name', models.CharField(max_length=255, null=True)),
                ('product_id', models.BigIntegerField(null=True)),
                ('device1', models.CharField(max_length=255, null=True)),
                ('device1_port', models.CharField(max_length=40, null=True)),
                ('device2', models.CharField(max_length=255, null=True)),
                ('device2_port', models.CharField(max_length=40, null=True)),
                ('gateway', models.CharField(max_length=255, null=True)),
                ('address', models.TextField(null=True)),
                ('ip', models.CharField(max_length=255, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddIndex(
            model_name='zxclientinfo',
            index=models.Index(fields=['ip'], name='networkreso_ip_ac310d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='publicipsegment',
            unique_together={('ip_segment', 'mask')},
        ),
        migrations.AddField(
            model_name='publicipmodrecord',
            name='mod_target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='networkresource.PublicIpAllocation'),
        ),
        migrations.AddField(
            model_name='privateipmodrecord',
            name='mod_target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='networkresource.PrivateIpAllocation'),
        ),
        migrations.AddIndex(
            model_name='iprecord',
            index=models.Index(fields=['device_ip'], name='networkreso_device__e13064_idx'),
        ),
        migrations.AddIndex(
            model_name='iprecord',
            index=models.Index(fields=['logic_port_num'], name='networkreso_logic_p_570a28_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmanresource',
            index=models.Index(fields=['slot'], name='networkreso_slot_aff53b_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmanresource',
            index=models.Index(fields=['mda'], name='networkreso_mda_2a3d16_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmanresource',
            index=models.Index(fields=['logic_port'], name='networkreso_logic_p_2b994b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='ipmanresource',
            unique_together={('device_name', 'port')},
        ),
    ]
