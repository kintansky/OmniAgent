# Generated by Django 3.0.1 on 2020-03-10 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networkresource', '0024_publicipsegmentschema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicipsegmentschema',
            name='alc_user',
            field=models.CharField(max_length=10, null=True),
        ),
    ]