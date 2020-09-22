import numpy as np
import pandas as pd
import scipy.spatial

from django.db import connection
from ..models import Article


class ArticleRecommender:
    def __init__(self):
        query = """
            SELECT url, title, vector 
            FROM webapi_article
            WHERE vector != ''
        """
        self.article_df = pd.read_sql_query(query, connection)

    def get_similar_articles(self, article_url, article_vector, topn=5):
        # 読んでいる記事以外の記事の情報を取得する
        other_df = self.article_df.loc[self.article_df['url'] != article_url].reset_index(drop=True)
        other_vecs = self._get_vectors(other_df)

        # 類似度計算
        similarities = self.calc_similarities(article_vector, other_vecs)
        most_similar_indices = similarities.argsort()[:topn]

        # 類似記事抽出
        similar_article_df = other_df.loc[most_similar_indices, ['url', 'title']]

        return [{url: title} for _, (url, title) in similar_article_df.iterrows()]

    def calc_similarities(self, target, others):
        similarities =  [scipy.spatial.distance.cosine(target, other) for other in others]
        return np.array(similarities)

    def _get_vectors(self, df):
        return np.array(df['vector'].tolist())