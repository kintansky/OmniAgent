# Generated by Django 2.1.7 on 2019-03-14 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchdog', '0004_auto_20190313_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateIpAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(blank=True, max_length=50, null=True)),
                ('community', models.CharField(blank=True, max_length=20, null=True)),
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
                ('alc_time', models.DateTimeField(auto_now_add=True)),
                ('adj_order', models.CharField(blank=True, max_length=255, null=True)),
                ('adj_time', models.DateTimeField(blank=True, null=True)),
                ('close_order', models.CharField(blank=True, max_length=255, null=True)),
                ('close_time', models.DateTimeField(blank=True, null=True)),
                ('adj_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prvip_adj_user', to=settings.AUTH_USER_MODEL)),
                ('alc_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='prvip_alc_user', to=settings.AUTH_USER_MODEL)),
                ('close_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prvip_close_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['alc_time'],
            },
        ),
    ]
