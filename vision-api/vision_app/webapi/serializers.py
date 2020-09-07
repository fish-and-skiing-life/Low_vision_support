from rest_framework import serializers
from webapi.models import Summarization, ArticleCategory, ArticleList

class SummarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summarization
        fields = ('media', 'url')

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ('media')

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleList
        fields = ('media', 'category_url')
