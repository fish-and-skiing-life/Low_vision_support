import numpy as np
import spacy
import torch

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


class BertVectorizer:
    def __init__(self):
        self.tokenizer = WebapiConfig.bert_tokenizer
        self.model = WebapiConfig.bert_model

    def encode_sentence(self, sentence):
        """BERTを利用して sentence vector を得る．

        Parameters
        ----------
        sentence : str
            文

        Returns
        -------
        numpy.ndarray
            sentence vector
        """
        tokens = self.tokenizer.tokenize(sentence) 
        tokens = ['[CLS]'] + tokens + ['[SEP]']

        tokens = self.tokenizer.convert_tokens_to_ids(tokens)

        tokens = torch.tensor([tokens])

        with torch.no_grad():
            outputs = self.model(tokens)
            # [CLS]の分散表現を sentence vector とする
            sent_vec = outputs[0][0, 0]
        
        return sent_vec.numpy()
