from django.db import models

class Summarization(models.Model):
    """
    必要なパラメータ
        media: 記事媒体 (Yahoo!, livedoor)
        url: 記事URL
    """
    media = models.CharField(max_length=128, null=False, default='unknown')
    url = models.TextField()

class ArticleCategory(models.Model):
    """
    パラメータ
        media: 記事媒体 (Yahoo!, livedoor)
    """
    media = models.CharField(max_length=128, null=False, default='unknown')

class ArticleList(models.Model):
    """
    パラメータ
        media:  記事媒体 (Yahoo!, livedoor)
        category_url:    任意のカテゴリの記事一覧のURL
    """
    media = models.CharField(max_length=128, null=False, default='unknown')
    category_url = models.CharField(max_length=128, null=False, default='unknown')
