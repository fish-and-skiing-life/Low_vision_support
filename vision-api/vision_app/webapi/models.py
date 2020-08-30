from django.db import models

class Summarization(models.Model):
    """
    必要なパラメータ
        記事媒体 (Yahoo!, livedoor)
        ID (記事のURLについている数字の羅列とか)
    """
    media = models.CharField(max_length=128, null=False, default='unknown')
    article_id = models.TextField()

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
        url:    記事一覧のURL
    """
    media = models.CharField(max_length=128, null=False, default='unknown')
    url = models.CharField(max_length=128, null=False, default='unknown')
