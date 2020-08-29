from rest_framework import serializers
from webapi.models import Summarization, ArticleCategory

class SummarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summarization
        fields = ('media', 'article_id')

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ('media')
