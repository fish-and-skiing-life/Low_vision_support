from rest_framework import serializers
from webapi.models import Summarization

class SummarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summarization
        fields = ('media', 'article_id', 'summary')
        read_only_fields = ('summary')