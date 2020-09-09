from rest_framework.response import Response
from rest_framework import views

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
        url = request.GET.get('url')

        # crawiling
        crawler = Crawling()
        article = crawler.get_article(int(media), url)

        # summarization
        model = LexRank()
        summary_list = model.summarize(article['body'])
        res = {f'summary_{i}': str(s) for i, s in enumerate(summary_list)}
        res['title'] = article['title']

        return Response(res)

class ArticleCategory(views.APIView):
    def get(self, request):
        media = request.GET.get('media')

        crawler = Crawling()
        article_category = crawler.get_category(int(media))

        return Response(article_category)

class ArticleList(views.APIView):
    def get(self, request):
        media = request.GET.get('media')
        url = request.GET.get('category_url')

        crawler = Crawling()
        article_list = crawler.get_article_list(int(media), url)
        # article_list = ['としまえん最後の週末 惜しむ声', '写真と違う料理 返金は可能？', 'ホンダ，通勤手当を廃止へ', 'マスクの転売規制を解除', '交通安全協会 入るメリットは']

        # res = {f'article_{i}': article for i, article in enumerate(article_list)}
        return Response(article_list)
