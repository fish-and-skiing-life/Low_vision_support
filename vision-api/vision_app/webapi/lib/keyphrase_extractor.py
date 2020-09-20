import spacy
import nltk
import pke
import os

from django.conf import settings


class PositionRank:
    """
    PositionRankを用いてテキストからキーフレーズを抽出する．
    """
    def __init__(self):
        # ストップワード登録
        pke.base.ISO_to_language['ja_ginza'] = 'japanese'
        stop_words = self._load_stopwords()
        nltk.corpus.stopwords.words = lambda lang : stop_words

    def extract(self, text, topn=10, is_join_words=True):
        """テキストからキーフレーズをtopn個抽出する．

        Parameters
        ----------
        text : str
            抽出対象のテキスト
        topn : int, default 10
            抽出するキーフレーズの件数
        is_join_words : bool, default True
            キーフレーズの単語を結合するか否か

        Returns
        -------
        List[str]
            キーフレーズのリスト
        """
        extractor = pke.unsupervised.PositionRank()
        extractor.load_document(text, language='ja_ginza', normalization=None)
        extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ'})
        extractor.candidate_weighting(window=3)
        keyphrases = extractor.get_n_best(n=topn)

        return self._postprocessing(keyphrases, is_join_words)

    def _load_stopwords(self):
        file_path = os.path.join(
            settings.BASE_DIR, 'webapi/res/stopwords.txt'
            )
        with open(file_path) as f:
            stopwords = f.read().split()

        return stopwords

    def _postprocessing(self, keyphrases, is_join_words=True):
        _keyphrases = keyphrases.copy()

        if is_join_words:
            _keyphrases = self._join_words(_keyphrases)

        _keyphrases = self._without_score(_keyphrases)

        return _keyphrases

    def _without_score(self, keyphrases):
        return [keyphrase for keyphrase, _ in keyphrases]

    def _join_words(self, keyphrases):
        return [(''.join(keyphrase.split()), score) for keyphrase, score in keyphrases]
