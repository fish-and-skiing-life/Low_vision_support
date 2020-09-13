from rest_framework.response import Response
from rest_framework import views
import spacy

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
        res = {'summary': summary_list, 'title': article['title']}

        # ner
        nlp = spacy.load('ja_ginza')
        ne_list = []
        for i, summary in enumerate(summary_list):
            doc = nlp(str(summary))
            for ent in doc.ents:
                ne_list.append(str(ent.text))
            
        res['ne_list'] = ne_list
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

        return Response(article_list)
