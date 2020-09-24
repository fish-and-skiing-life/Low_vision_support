import itertools
import os
from rest_framework.response import Response
from rest_framework import views


from webapi.lib.crawling import Crawling
from django.conf import settings
from webapi.apps import WebapiConfig
import webapi.lib.nlp_utils as nlp_utils
from .models import Wiki, Trend, Article
import pandas as pd


class Summarization(views.APIView):
    def get(self, request):
        media = request.GET.get('media')
        url = request.GET.get('url')
        mode = request.GET.get('mode')
        print(mode)
        print(media)
        # crawiling
        if mode == 'news':
            crawler = Crawling()
            article = crawler.get_article(int(media), url)
        elif mode == 'recommend':
            article = Article.objects.filter(url = url)
        print(article)

        return Response(nlp_utils.summarize(article['title'], article['body']))

class Recommendation(views.APIView):
    def get(self, request):
        media = request.GET.get('media')
        url = request.GET.get('url')
        mode = request.GET.get('mode')
        print(mode)
        # crawiling
        if mode == 'news':
            crawler = Crawling()
            article = crawler.get_article(int(media), url)
        elif mode == 'recommend':
            article = Article.objects.filter(url = url)

        print(article)
        return Response(nlp_utils.get_recommend(url, article['body']))


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

        ne_list = []
        crawler = Crawling()
        article_list = crawler.get_article_list(int(media), url)
        article_list = dict(itertools.islice(article_list.items(), 5))
        
        ne_list = nlp_utils.extract_keyword(article_list, False)
        res = {'article_list': article_list, 'ne_list': ne_list, 'trends': nlp_utils.get_trend(ne_list) } 
        return Response(res)

class Wikipedia(views.APIView):
    def get(self, request):
        words = request.GET.get('word')
        wiki2vec = WebapiConfig.wiki2vec_model
        similar_list = wiki2vec.most_similar(wiki2vec.get_entity(words), 5)
        result = ''

        for row in similar_list:
            if(row[0].__class__.__name__ == 'Entity'):
                result = row[0].title
                break

        wiki = Wiki.objects.filter(title = result)
        print(wiki)

        if len(wiki) == 0:
            res = {'title': 'error', 'summary': ['error']}
        else:
            res = nlp_utils.summarize(wiki[0].title, wiki[0].abst, False)
        return Response(res)

class CalcDb(views.APIView):
    def get(self, request):
        print('start calcDB')
        result = nlp_utils.calcArticleVector()
        print('end calcDB')
        return Response({'result': result})

class InsertWiki(views.APIView):
    def get(self, request):
        df = pd.read_csv('/myapp/vision_app/webapi/wiki_data.csv')
        error = []
        for i in range(len(df)):
            wiki_data = Wiki(title=df.iloc[i, 1], abst=df.iloc[i, 2])
            try:
                wiki_data.save()
            except:
                error.append(df.iloc[i, 1])

        print(error)
        return Response({'result': 'OK'})

