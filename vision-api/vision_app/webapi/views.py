from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse

from webapi.models import Summarization
from webapi.serializers import SummarizationSerializer
from webapi.lib.summarizer import LexRank

class ArticleSummarization(viewsets.ViewSet):
    queryset = Summarization.objects.all()
    serializer_class = SummarizationSerializer

    @action(detail=False, methods=['get'])
    def predict_summarization(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        media_dict = {
            '0': 'https://news.yahoo.co.jp/articles/',
            '1': 'https://news.livedoor.com/article/detail/',
            '2': 'https://mainichi.jp/articles/',
            '3': 'https://www.asahi.com/articles/',
            '4': 'https://www.yomiuri.co.jp/',
            '5': 'https://www.nikkei.com/article/'
        }

        media = request.data['media']
        article_id = request.data['article_id']

        # scraping
        article = ScrapingArticle.scrape_article(media, media_dict[media]+article_id)

        # summarization
        model = LexRank()
        summary_list = model.summarize(article)
        res = {f'summary_{i}': s for i, s in enumerate(summary_list)}

        return JsonResponse(res, safe=False)