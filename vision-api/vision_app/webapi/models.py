from django.db import models

class Article(models.Model):
    url = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=4000)
    vector = models.TextField(max_length=4000)


class Named_entity(models.Model):
    url = models.CharField(max_length=256)
    word = models.TextField(max_length=256)
    vector = models.TextField(max_length=4000)


class Trend(models.Model):
    word = models.CharField(max_length=256)
    score = models.IntegerField()


class Wiki(models.Model):
    title = models.CharField(max_length=256)
    abst = models.TextField(max_length=4000)
