# Generated by Django 3.1.1 on 2020-09-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0004_article_named_entity_trend_wiki'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='vector',
            field=models.TextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='named_entity',
            name='vector',
            field=models.TextField(max_length=4000),
        ),
    ]