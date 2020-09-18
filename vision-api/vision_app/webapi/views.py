import itertools

from rest_framework.response import Response
from rest_framework import views

from webapi.lib.summarizer import LexRank
from webapi.lib.crawling import Crawling
import webapi.lib.nlp_utils as nlp_utils
from .models import Wiki, Trend, Article


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

        return Response(nlp_utils.summarize(article['title'], article['body']))

class ArticleCategory(views.APIView):
    def get(self, request):
        media = request.GET.get('media')

        nlp_utils.calcArticleVector()

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
        article_list = dict(itertools.islice(article_list.items(), 10))
        
        ne_list = nlp_utils.extract_named(article_list)
        res = {'article_list': article_list, 'ne_list': ne_list, 'trends': nlp_utils.get_trend(ne_list) } 
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

class Wikipedia(views.APIView):
    def get(self, request):
        words = request.GET.get('word')
        hoge = Article.objects.filter(title= "陸上イージス代替策、「洋上」で検討　専用艦新造案も")
        print(hoge)
        wiki = Wiki.objects.filter(title__contains= 'ドラムマシン')
        print(wiki)
        res = {'word': words,
                "summary": 'summary'
                   
                }

        return Response(res)

class CalcDb(views.APIView):
    def get(self, request):
        
        result = nlp_utils.calcArticleVector()
        return Response({'result': result})
