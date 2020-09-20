import datetime
import spacy
import itertools
import time
from pytrends.request import TrendReq
from dateutil.relativedelta import relativedelta
from webapi.lib.summarizer import LexRank
from webapi.lib.vectorizer import GinzaVectorizer
from webapi.lib.keyphrase_extractor import PositionRank
from ..models import Trend, Article, Named_entity
import numpy as np

def calcArticleVector():
    """Articleテーブルのvectorが'''の値を全部取得し、vector計算する

        Returns
        -------
        Boolian
          成功か失敗か
    """
    data = Article.objects.filter(vector = '' )
    is_success = True
    position = PositionRank()
    vectorizer = GinzaVectorizer()
    named_entity_query = []
    trend_query = []
    article_query = []
    try:
        for article in data:
            key_dict = {}
            trend_dict = {}
            key_list = position.extract(article.content)
            for keyword in key_list:
                vector = vectorizer.encode_phrase(keyword)
                vector_str = str(vector.tolist())
                named = Named_entity(url = article.url, word = keyword, vector = 0.0)
                keyword_score = get_trend_score(keyword)
                trend = Trend(word = keyword, score = keyword_score)
                key_dict.setdefault(keyword, vector)
                trend_dict.setdefault(keyword, keyword_score)
                named_entity_query.append(named)
                trend_query.append(trend)
                time.sleep(40)

            article_vector = vectorizer.calc_weighted_article_vector(key_dict, trend_dict, theta=0.8)
            article_vector_str = str(article_vector.tolist())

            article.vector = 0.0
            article_query.append(article)
            break
        # Named_entity.objects.bulk_create(named_entity_query)
        # Trend.objects.bulk_create(trend_query)
        # Article.objects.bulk_update(article_query, fields=['vector'])

    except Exception as e:
        print(e)
        is_success = False

    return is_success

def summarize(title, body, isTrend = True ):
    """本文の内容を３行に要約、keywordの抽出, keywordのtrend値の計算

        Parameters
        ----------
        title : str
            記事のタイトル
        body : str
            記事の本文
        isTrend : bool, default True
            キーフレーズの単語を結合するか否か

        Returns
        -------
        dict
          {summary: list, ne_list: list, trend: list}
    """
    # summarization
    model = LexRank()
    summary_list = model.summarize(body)
    res = {'summary': summary_list, 'title': title}
    ne_list = extract_keyword(summary_list, True)
    res['ne_list'] = ne_list

    # trends
    if( isTrend ):
        res['trends'] = get_trend(ne_list)
    else:
        res['trends'] = ''
    
    return res

def extract_keyword(doc_list, isContent):
    """本文からキーフレーズの抽出

        Parameters
        ----------
        doc_list : list
            記事の文章
        isContent: boolian
            本文か

        Returns
        -------
        list
          キーフレーズのリスト   
    """
    position = PositionRank()
    ne_list = []
    for i, doc in enumerate(doc_list):
        if isContent:
            ne_list.append(position.extract(str(doc), topn=10, is_join_words=False))
        else:
            ne_list.append(position.extract(str(doc), topn=4, is_join_words=False))

    return list(itertools.chain.from_iterable(ne_list))

def get_trend(ne_list):
    """キーフレーズのトレンド計算

        Parameters
        ----------
        ne_list : list
            キーフレーズのリスト

        Returns
        -------
        dict
            {keyword: score(int)}
    """
    search_dict = {}
    dt_now = datetime.datetime.now()
    start_frame = (dt_now - relativedelta(months=6)).strftime('%Y-%m-%d')
    end_frame = dt_now.strftime('%Y-%m-%d')
    pytrend = TrendReq(hl='jp-JP', tz=-540, proxies=['http://proxy.nagaokaut.ac.jp:8080'])
    # pytrend = TrendReq(hl='jp-JP', tz=-540)
    
    for word in ne_list:
        score = get_trend_score(word)
        search_dict.update({word: score})
    return search_dict

def get_trend_score(word):
    """キーフレーズのトレンド計算

        Parameters
        ----------
        word : str
            キーワード

        Returns
        -------
        int
            トレンドの値
    """
    search_dict = {}
    dt_now = datetime.datetime.now()
    start_frame = (dt_now - relativedelta(months=6)).strftime('%Y-%m-%d')
    end_frame = dt_now.strftime('%Y-%m-%d')
    pytrend = TrendReq(hl='jp-JP', tz=-540, proxies=['http://proxy.nagaokaut.ac.jp:8080'])
    # pytrend = TrendReq(hl='jp-JP', tz=-540)

    pytrend.build_payload([word], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')
    try:
        data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
        data = list(itertools.chain.from_iterable(data.values.tolist()))
        if(sum(data) != 0):
            score = sum(data[-7 :]) / sum(data)
        else: score =0
    except:
        score = 0
    

    return score
