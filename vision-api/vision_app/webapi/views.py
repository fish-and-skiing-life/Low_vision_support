from rest_framework.response import Response
from rest_framework import views

from webapi.models import Summarization, ArticleCategory
from webapi.serializers import SummarizationSerializer, ArticleCategorySerializer
from webapi.lib.summarizer import LexRank
from webapi.lib.crawling import Crawling

class ArticleSummarization(views.APIView):
    def get(self, request):
        media_dict = {
            '0': 'https://news.yahoo.co.jp/articles/',
            '1': 'https://www.asahi.com/articles/',
            '2': 'https://www.yomiuri.co.jp/',
            '3': 'https://www.nikkei.com/article/'
        }
        media = request.GET.get('media')
        article_id = request.GET.get('article_id')

        # crawiling
        crawler = Crawling()
        article = crawler.scraping_article(media, media_dict[media]+article_id)

        # summarization
        model = LexRank()
        summary_list = model.summarize(article)
        res = {f'summary_{i}': str(s) for i, s in enumerate(summary_list)}

        return Response(res)

class ArticleCategory(views.APIView):
    def get(self, request):
        media = request.GET.get('media')

        crawler = Crawling()
        article_category = crawler.get_category(int(media))


        res = {f'category_{i}': str(c) for i, c in enumerate(article_category)}
        return Response(res)
