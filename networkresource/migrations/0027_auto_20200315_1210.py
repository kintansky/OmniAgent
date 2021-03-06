# Generated by Django 3.0.1 on 2020-03-15 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0026_auto_20200310_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='ICP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify_id', models.CharField(max_length=100)),
                ('guard_level', models.CharField(max_length=10, null=True)),
                ('city', models.CharField(max_length=10, null=True)),
                ('district', models.CharField(max_length=10, null=True)),
                ('distributor', models.CharField(max_length=10, null=True)),
                ('distributor_contact', models.CharField(max_length=20, null=True)),
                ('demand', models.TextField(null=True)),
                ('bandwidth_up', models.PositiveIntegerField(default=0)),
                ('bandwidth_dwn', models.PositiveIntegerField(default=0)),
                ('client_tech', models.CharField(max_length=10, null=True)),
                ('client_tech_contact', models.CharField(max_length=20, null=True)),
                ('demand_ipv4_amount', models.PositiveIntegerField(default=0)),
                ('demand_ipv6_amount', models.PositiveIntegerField(default=0)),
                ('client_address', models.CharField(max_length=255, null=True)),
                ('businessman', models.CharField(max_length=10, null=True)),
                ('businessman_contact', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'MR_REC_icp_info',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='ipallocation',
            name='icp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='networkresource.ICP'),
        ),
    ]
