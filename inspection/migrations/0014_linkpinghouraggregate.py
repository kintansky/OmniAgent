# Generated by Django 2.2.5 on 2019-11-06 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0013_porterrorfullrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkPingHourAggregate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(max_length=20)),
                ('h0', models.FloatField()),
                ('h1', models.FloatField()),
                ('h2', models.FloatField()),
                ('h3', models.FloatField()),
                ('h4', models.FloatField()),
                ('h5', models.FloatField()),
                ('h6', models.FloatField()),
                ('h7', models.FloatField()),
                ('h8', models.FloatField()),
                ('h9', models.FloatField()),
                ('h10', models.FloatField()),
                ('h11', models.FloatField()),
                ('h12', models.FloatField()),
                ('h13', models.FloatField()),
                ('h14', models.FloatField()),
                ('h15', models.FloatField()),
                ('h16', models.FloatField()),
                ('h17', models.FloatField()),
                ('h18', models.FloatField()),
                ('h19', models.FloatField()),
                ('h20', models.FloatField()),
                ('h21', models.FloatField()),
                ('h22', models.FloatField()),
                ('h23', models.FloatField()),
            ],
            options={
                'db_table': 'OM_REP_ping_hour_aggregate',
            },
        ),
    ]
