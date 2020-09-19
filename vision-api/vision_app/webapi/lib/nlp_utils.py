import datetime
import spacy
import itertools
from pytrends.request import TrendReq
from dateutil.relativedelta import relativedelta
from webapi.lib.keyphrase_extractor import PositionRank
from ..models import Trend, Article, Named_entity

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

def summarize(title, body ):
    # summarization
    model = LexRank()
    summary_list = model.summarize(body)
    res = {'summary': summary_list, 'title': title}
    ne_list = extract_keyword(summary_list)
    res['ne_list'] = ne_list

    # trends
    res['trends'] = get_trend(ne_list)
    return res

def extract_keyword(doc_list):
    position = PositionRank()
    ne_list = []
    for i, doc in enumerate(doc_list):
        ne_list.append(position(str(doc)))

    return list(set(ne_list))

def get_trend(ne_list):
    search_dict = {}
    dt_now = datetime.datetime.now()
    start_frame = (dt_now - relativedelta(months=6)).strftime('%Y-%m-%d')
    end_frame = dt_now.strftime('%Y-%m-%d')
    pytrend = TrendReq(hl='jp-JP', tz=-540, proxies=['http://proxy.nagaokaut.ac.jp:8080'])
    # pytrend = TrendReq(hl='jp-JP', tz=-540)

    for num in range(0, len(ne_list),5):
        pytrend.build_payload(ne_list[num : num+4], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')

        data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
        search_dict.update(data.apply(lambda col: col.sum()).to_dict())

    return search_dict

def get_trend_score(word):
    search_dict = {}
    dt_now = datetime.datetime.now()
    start_frame = (dt_now - relativedelta(months=6)).strftime('%Y-%m-%d')
    end_frame = dt_now.strftime('%Y-%m-%d')
    pytrend = TrendReq(hl='jp-JP', tz=-540, proxies=['http://proxy.nagaokaut.ac.jp:8080'])
    # pytrend = TrendReq(hl='jp-JP', tz=-540)

    pytrend.build_payload([word], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')

    data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
    data = list(itertools.chain.from_iterable(data.values.tolist()))

    return sum(data[-7 :]) / sum(data)
