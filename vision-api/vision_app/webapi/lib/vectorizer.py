import numpy as np
import spacy

from ..apps import WebapiConfig


class GinzaVectorizer:
    def encode_phrase(self, phrase):
        """フレーズをベクトル化する，
        フレーズベクトルはフレーズ内の単語の平均ベクトル．

        Parameters
        ----------
        phrase : str
            フレーズ

        Returns
        -------
        numpy.ndarray
            フレーズベクトル
        """        
        parsed_phrase = WebapiConfig.ginza_model(phrase, disable=['dep', 'ent'])
        
        return parsed_phrase.vector

    def calc_weighted_article_vector(self, phrase_vectors, phrase_scores, theta=0.8):
        """TrendScoreで重み付けした記事ベクトルを計算する．

        Parameters
        ----------
        phrases : dict[str, numpy.ndarray]
            記事から抽出したキーフレーズのベクトル．
            Key : キーフレーズ
            Value : キーフレーズベクトル
        scores : dict[str, float]
            記事から抽出したキーフレーズのTrendScore．
            Key : キーフレーズ
            Value : TrendScore
        theta : float, default 0.8
            TrendScoreを考慮する度合い．
            値域は [0, 1]

        Returns
        -------
        numpy.ndarray
            記事ベクトル
        """ 

        weighted_phrase_vectors = []
        for keyphrase in phrase_vectors.keys():
            weighted_phrase_vector = (theta * phrase_scores[keyphrase] + (1.0 - theta)) * phrase_vectors[keyphrase]
            weighted_phrase_vectors.append(weighted_phrase_vector)

        return np.array(weighted_phrase_vectors).mean(axis=0)