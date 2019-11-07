# Generated by Django 2.2.5 on 2019-10-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0013_auto_20191028_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='OltBngRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bng', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=40)),
                ('logic_port', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=255)),
                ('olt_num', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=10)),
                ('olt', models.CharField(max_length=255)),
                ('olt_state', models.CharField(max_length=20, null=True)),
                ('olt_type', models.CharField(max_length=10, null=True)),
                ('olt_ip', models.GenericIPAddressField()),
            ],
            options={
                'db_table': 'MR_REP_olt_bng_references',
            },
        ),
        migrations.CreateModel(
            name='OltInfoWG',
            fields=[
                ('olt_num', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('district', models.CharField(max_length=10)),
                ('olt_zh', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20, null=True)),
                ('olt_type', models.CharField(max_length=10, null=True)),
                ('ip', models.GenericIPAddressField()),
            ],
            options={
                'db_table': 'MR_REC_olt_info_wg',
            },
        ),
        migrations.AddIndex(
            model_name='oltinfowg',
            index=models.Index(fields=['ip'], name='MR_REC_olt__ip_7f774c_idx'),
        ),
    ]