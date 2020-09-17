import datetime

from rest_framework.response import Response
from rest_framework import views
import spacy
import pandas as pd
from pytrends.request import TrendReq

from webapi.lib.summarizer import LexRank
from webapi.lib.crawling import Crawling

from .models import Wiki


def summariz(title, body ):
    # summarization
    model = LexRank()
    summary_list = model.summarize(body)
    res = {'summary': summary_list, 'title': title}
    ne_list = extract_named(summary_list)
    res['ne_list'] = ne_list

    # trends
    res['trends'] = get_trend(ne_list)
    return res

def extract_named(doc_list):
    nlp = spacy.load('ja_ginza')
    ne_list = []
    for i, doc in enumerate(doc_list):
        doc_split = nlp(str(doc))
        for ent in doc_split.ents:
            ne_list.append(str(ent.text))

    return list(set(ne_list))

def get_trend(ne_list):
    search_dict = {}
    dt_now = datetime.datetime.now()
    start_frame = (dt_now - datetime.timedelta(weeks=2)).strftime('%Y-%m-%d')
    end_frame = dt_now.strftime('%Y-%m-%d')
    pytrend = TrendReq(hl='jp-JP', tz=-540)

    for num in range(0, len(ne_list),5):
        pytrend.build_payload(ne_list[num : num+4], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')

        data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
        search_dict.update(data.apply(lambda col: col.sum()).to_dict())

    return search_dict


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

        summariz(article['title'], article['body'])

        return Response(summariz(article['title'], article['body']))

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
        ne_list = extract_named(article_list)
        res = {'article_list': article_list, 'ne_list': ne_list, 'trends': get_trend(ne_list) } 
        return Response(res)

class RecommendList(views.APIView):
    def get(self, request):
        url = request.GET.get('news_url')
        res = {'recommend':
                    {
                        "日本人CA150人、失職の危機　米ユナイテッド、成田勤務": "https://news.yahoo.co.jp/articles/bc6e2bbf2000ee2c636c67f56aee6faa24dac0e3",
                        '観光政策変わる？自民総裁選、京都の業界も熱視線　「日本人客を大切にするべき」声も': 'https://news.yahoo.co.jp/pickup/6371062',
                        '「倒産・廃業の予備軍多い」　年末ごろから急増の恐れも': 'https://news.yahoo.co.jp/articles/adec416d5e9fc7b662d7b9abc0336628c44f1f90'
                    }
                }

        return Response(res)

class Recommend(views.APIView):
    def get(self, request):
        url = request.GET.get('news_url')
        res = {'recommend':
                    {
                        "日本人CA150人、失職の危機　米ユナイテッド、成田勤務": "https://news.yahoo.co.jp/articles/bc6e2bbf2000ee2c636c67f56aee6faa24dac0e3",
                        '観光政策変わる？自民総裁選、京都の業界も熱視線　「日本人客を大切にするべき」声も': 'https://news.yahoo.co.jp/pickup/6371062',
                        '「倒産・廃業の予備軍多い」　年末ごろから急増の恐れも': 'https://news.yahoo.co.jp/articles/adec416d5e9fc7b662d7b9abc0336628c44f1f90'
                    }
                }

        return Response(res)

class Wiki(views.APIView):
    def get(self, request):
        word = request.GET.get('word')
        wiki = Wiki.objects.filter(title = word)
        print(wiki)
        res = {'word': word,
                "summary": 'summary'
                   
                }

        return Response(res)
