import datetime
import spacy
from pytrends.request import TrendReq

from ..models import Trend, Article

def calcArticleVector():
    data = Article.objects.filter(vector = None)
    print(data)

    for article in data:
        print(article.vector)
        ne_list = extract_named(article['content'])


    # # summarization
    # model = LexRank()
    # summary_list = model.summarize(body)
    # res = {'summary': summary_list, 'title': title}
    # ne_list = extract_named(summary_list)
    # res['ne_list'] = ne_list

    # # trends
    # res['trends'] = get_trend(ne_list)
    # return res

def summarize(title, body ):
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
    # pytrend = TrendReq(hl='jp-JP', tz=-540, proxies=['http://proxy.nagaokaut.ac.jp:8080'])
    pytrend = TrendReq(hl='jp-JP', tz=-540)

    for num in range(0, len(ne_list),5):
        pytrend.build_payload(ne_list[num : num+4], cat=0, timeframe=f'{start_frame} {end_frame}', geo='JP')

        data = pytrend.interest_over_time().drop(['isPartial'], axis=1)
        search_dict.update(data.apply(lambda col: col.sum()).to_dict())

    return search_dict



if __name__ == "__main__":
    calcArticleVector()
