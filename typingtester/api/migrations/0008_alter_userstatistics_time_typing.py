# Generated by Django 4.0.1 on 2022-01-28 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_usertest_cpm_alter_usertest_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatistics',
            name='time_typing',
            field=models.FloatField(default=0),
        ),
    ]
