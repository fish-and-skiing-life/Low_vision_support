# Generated by Django 3.1.1 on 2020-09-15 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0002_auto_20200909_0659'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Named_entity',
        ),
        migrations.DeleteModel(
            name='Trend',
        ),
    ]
