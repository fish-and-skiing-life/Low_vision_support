import spacy
import nltk
import pke


class PositionRank:
    """
    PositionRankを用いてテキストからキーフレーズを抽出する．
    """
    def __init__(self):
        # ストップワード登録
        pke.base.ISO_to_language['ja_ginza'] = 'japanese'
        stop_words = self._load_stopwords()
        nltk.corpus.stopwords.words = lambda lang : stop_words

    def _load_stopwords(self):
        with open('../res/stopwords.txt') as f:
            stopwords = f.read().split()

        return stopwords

    def extract(self, text, topn=10):
        """テキストからキーフレーズをtopn個抽出する．

        Parameters
        ----------
        text : str
            抽出対象のテキスト
        topn : int, default 10
            抽出するキーフレーズの件数

        Returns
        -------
        List[str]
            キーフレーズのリスト
        """
        extractor = pke.unsupervised.PositionRank()
        extractor.load_document(text, language='ja_ginza', normalization=None)
        extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ'})
        extractor.candidate_weighting(window=3)
        
        return extractor.get_n_best(n=topn)