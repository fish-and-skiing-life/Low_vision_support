import regex
import datetime
import spacy
import itertools
import time
from pytrends.request import TrendReq
from dateutil.relativedelta import relativedelta
from webapi.lib.summarizer import LexRank
import webapi.lib.scoring as scoring
from webapi.lib.vectorizer import GinzaVectorizer
from webapi.lib.recommender import ArticleRecommender
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
    trend_data = Trend.objects.all()
    trend_word = {}
    for row in trend_data:
        trend_word.setdefault(row.word, row.score)

    data = Article.objects.filter(vector = '' )
    is_success = True
    position = PositionRank()
    vectorizer = GinzaVectorizer()
    named_entity_query = []
    trend_query = []
    article_query = []
    try:
        for index, article in enumerate(data):
            if index % 30 == 0 and index != 0:
                Named_entity.objects.bulk_create(named_entity_query)
                Trend.objects.bulk_create(trend_query)
                Article.objects.bulk_update(article_query, fields=['vector'])
                named_entity_query = []
                trend_query = []
                article_query = []
                print('aaaaaaaaa')
            if index % 100 == 0:
                print(index)

            key_dict = {}
            trend_dict = {}
            key_list = position.extract(article.content)

            for keyword in key_list:
                vector = vectorizer.encode_phrase(keyword)
                vector_str = str(vector.tolist())
                named = Named_entity(url = article.url, word = keyword, vector = vector_str)
                if keyword not in trend_word:
                    keyword_score = get_trend_score(keyword)
                    trend = Trend(word = keyword, score = keyword_score)
                    time.sleep(10)
                    trend_word.setdefault(keyword, keyword_score)
                    trend_query.append(trend)
                else:
                    keyword_score = trend_word[keyword]

                key_dict.setdefault(keyword, vector)
                trend_dict.setdefault(keyword, keyword_score)
                named_entity_query.append(named)

            article_vector = vectorizer.calc_weighted_article_vector(key_dict, trend_dict, theta=0.8)
            article_vector_str = str(article_vector.tolist())

            article.vector = article_vector_str
            article_query.append(article)
            
        Named_entity.objects.bulk_create(named_entity_query)
        Trend.objects.bulk_create(trend_query)
        Article.objects.bulk_update(article_query, fields=['vector'])

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
        score = scoring.calc_trend_score(data)
    except:
        score = 0
    

    return score


def split_sentences(text):
    """正規表現を使用してテキストを文単位で分割する．

    Parameters
    ----------
    text : str
        テキスト

    Returns
    -------
    list[str]
        文のリスト
    """
    return [s.strip() for s in regex.findall(r'[\S\s]+?。', text)]

def get_recommend(url, article):
    """記事をレコメンドする

    Parameters
    ----------
    url : str
        記事のURL
    article: str
        記事本文
    
    Returns
    -------
    dict[str, str]
        各要素は辞書型で `{title: url}`
    """
    try:
        article_info = Article.objects.get(url=url)
        vector_str = article_info.vector
        vector_str.replace('[', '').replace(']', '').replace(' ', '').split(',')
        article_vector = np.array([float(vs) for vs in vector_str])

    except:
        trend_data = Trend.objects.all()
        trend_word = {}
        for row in trend_data:
            trend_word.setdefault(row.word, row.score)
        position = PositionRank()
        vectorizer = GinzaVectorizer()

        key_list = position.extract(article)
        trend_dict = {}
        key_dict = {}

        for keyword in key_list:
            if keyword not in trend_word:
                keyword_score = get_trend_score(keyword)
                trend = Trend(word = keyword, score = keyword_score)
                time.sleep(10)
                trend_word.setdefault(keyword, keyword_score)
            else:
                keyword_score = trend_word[keyword]
            trend_dict.setdefault(keyword, keyword_score)

            vector = vectorizer.encode_phrase(keyword)
            key_dict.setdefault(keyword, vector)

        article_vector = vectorizer.calc_weighted_article_vector(key_dict, trend_dict, theta=0.8)

    recommender = ArticleRecommender()
    recommend_list = recommender.get_similar_articles(url, article_vector)

    recommend = {}
    for recommend_article in recommend_list:
        recommend.update(recommend_article)
    
    return recommend
