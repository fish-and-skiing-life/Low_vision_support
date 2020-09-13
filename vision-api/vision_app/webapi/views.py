import datetime

from rest_framework.response import Response
from rest_framework import views
import spacy
import pandas as pd
from pytrends.request import TrendReq

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
        print(article)
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

        ne_list = list(set(ne_list))
        res['ne_list'] = ne_list

        # trends
        search_dict = {}
        dt_now = datetime.datetime.now()
        start_frame = (dt_now - datetime.timedelta(weeks=2)).strftime('%Y-%m-%d')
        end_frame = dt_now.strftime('%Y-%m-%d')
        pytrend = TrendReq(hl='jp-JP', tz=-540)

        for num in range(0, len(ne_list),5):
            pytrend.build_payload(ne_list[num : num+4], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')

            data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
            search_dict.update(data.apply(lambda col: col.sum()).to_dict())
        res['trends'] = search_dict

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
