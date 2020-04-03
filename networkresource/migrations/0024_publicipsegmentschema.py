# Generated by Django 3.0.1 on 2020-03-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0023_auto_20200310_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicIPSegmentSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('upper_segment', models.GenericIPAddressField()),
                ('upper_mask', models.PositiveSmallIntegerField()),
                ('state', models.SmallIntegerField(null=True)),
                ('subnet_gateway', models.CharField(max_length=10, null=True)),
                ('subnet_mask', models.PositiveSmallIntegerField(null=True)),
                ('access_bng', models.CharField(max_length=255, null=True)),
                ('access_olt', models.CharField(max_length=255, null=True)),
                ('access_type', models.CharField(max_length=10, null=True)),
                ('alc_user', models.CharField(max_length=10)),
                ('alc_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'MR_REC_public_segment_schema',
            },
        ),
    ]
