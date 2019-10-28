# Generated by Django 2.2.5 on 2019-10-28 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0012_auto_20191028_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpticalMoudle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=30)),
                ('moudle', models.CharField(max_length=60)),
                ('record_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'MR_REC_optical_moudle_record',
            },
        ),
        migrations.RemoveIndex(
            model_name='ipallocation',
            name='networkreso_ip_0eb81d_idx',
        ),
        migrations.RemoveIndex(
            model_name='ipmod',
            name='networkreso_ip_c2cd15_idx',
        ),
        migrations.RemoveIndex(
            model_name='ipmod',
            name='networkreso_client__e0ceca_idx',
        ),
        migrations.RemoveIndex(
            model_name='ipmod',
            name='networkreso_product_209ab8_idx',
        ),
        migrations.RemoveIndex(
            model_name='iprecord',
            name='networkreso_device__e13064_idx',
        ),
        migrations.RemoveIndex(
            model_name='iprecord',
            name='networkreso_logic_p_570a28_idx',
        ),
        migrations.RemoveIndex(
            model_name='zxclientinfo',
            name='networkreso_ip_ac310d_idx',
        ),
        migrations.AddIndex(
            model_name='ipallocation',
            index=models.Index(fields=['ip'], name='MR_REC_ip_a_ip_206eee_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmod',
            index=models.Index(fields=['ip'], name='MR_REC_ip_m_ip_0e21b1_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmod',
            index=models.Index(fields=['client_name'], name='MR_REC_ip_m_client__0a7704_idx'),
        ),
        migrations.AddIndex(
            model_name='ipmod',
            index=models.Index(fields=['product_id'], name='MR_REC_ip_m_product_b2067a_idx'),
        ),
        migrations.AddIndex(
            model_name='iprecord',
            index=models.Index(fields=['device_ip'], name='MR_REC_ip_r_device__c96b92_idx'),
        ),
        migrations.AddIndex(
            model_name='iprecord',
            index=models.Index(fields=['logic_port_num'], name='MR_REC_ip_r_logic_p_1eff30_idx'),
        ),
        migrations.AddIndex(
            model_name='zxclientinfo',
            index=models.Index(fields=['ip'], name='MR_REC_grou_ip_6f0850_idx'),
        ),
        migrations.AlterModelTable(
            name='ipallocation',
            table='MR_REC_ip_allocation',
        ),
        migrations.AlterModelTable(
            name='ipmod',
            table='MR_REC_ip_mod_record',
        ),
        migrations.AlterModelTable(
            name='iprecord',
            table='MR_REC_ip_record',
        ),
        migrations.AlterModelTable(
            name='publicipgateway',
            table='MR_REC_public_ip_gateway',
        ),
        migrations.AlterModelTable(
            name='publicipsegment',
            table='MR_REC_public_ip_segment',
        ),
        migrations.AlterModelTable(
            name='zxclientinfo',
            table='MR_REC_group_client_info',
        ),
        migrations.AddIndex(
            model_name='opticalmoudle',
            index=models.Index(fields=['device'], name='MR_REC_opti_device_c2246e_idx'),
        ),
        migrations.AddIndex(
            model_name='opticalmoudle',
            index=models.Index(fields=['port'], name='MR_REC_opti_port_549530_idx'),
        ),
    ]
