# Generated by Django 3.1.1 on 2020-09-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webapi', '0003_auto_20200915_0617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('content', models.TextField(max_length=4000)),
                ('vector', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Named_entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('word', models.TextField(max_length=256)),
                ('vector', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=256)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('abst', models.TextField(max_length=4000)),
            ],
        ),
    ]
