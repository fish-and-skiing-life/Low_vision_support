import datetime
import spacy
import itertools
from pytrends.request import TrendReq
from dateutil.relativedelta import relativedelta
from webapi.lib.summarizer import LexRank
from webapi.lib.keyphrase_extractor import PositionRank
from ..models import Trend, Article, Named_entity
import numpy as np

def calcArticleVector():
    data = Article.objects.filter(vector = 0.0 )
    is_success = True
    position = PositionRank()
    try:
        for article in data:
            print(article.vector)
            key_list = position([article.content])
            for keyword in key_list:
                named = Named_entity(url = article.url, word = keyword, vector = 0.0)
                keyword_score = get_trend_score(keyword)
                trend = Trend(word = keyword, score = keyword_score)
                sleep(40)
                # named.save()
                # trend.save()
            article.vector = 0.0
            # article.save()

    except Exception as e:
        print(e)
        is_success = False

    return is_success

def summarize(title, body, isTrend = True ):
    # summarization
    model = LexRank()
    summary_list = model.summarize(body)
    res = {'summary': summary_list, 'title': title}
    ne_list = extract_keyword(summary_list)
    res['ne_list'] = ne_list

    # trends
    if( isTrend ):
        res['trends'] = get_trend(ne_list)
    else:
        res['trends'] = ''
    
    return res

def extract_keyword(doc_list):
    position = PositionRank()
    ne_list = []
    for i, doc in enumerate(doc_list):
        ne_list.append(position.extract(str(doc), topn=10, is_join_words=False))

    return list(itertools.chain.from_iterable(ne_list))

def get_trend(ne_list):
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
