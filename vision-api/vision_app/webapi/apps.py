import os

import spacy
from gensim.models import KeyedVectors
from transformers import BertJapaneseTokenizer, BertForMaskedLM

from django.apps import AppConfig


class WebapiConfig(AppConfig):
    name = 'webapi'

    bert_model = load_bert()
    ginza_model = load_ginza()
    wiki2vec_model = load_wiki2vec()

    @staticmethod
    def load_bert():
        print('Load BERT model...')

        file_path = os.path.join(settings.BASE_DIR, 'webapi/models/bert-base-japanese-whole-word-masking')

        tokenizer = BertJapaneseTokenizer.from_pretrained(file_path)
        model = BertForMaskedLM.from_pretrained(file_path)
        model.eval()

        return model, tokenizer

    @staticmethod
    def load_ginza():
        print('Load GiNZA model...')

        file_path = os.path.join(settings.BASE_DIR, 'webapi/models/chive-1.1-mc5-20200318.bin)

        w2v_model = KeyedVectors.load_word2vec_format(file_path,  binary=True)
        nlp = spacy.load('ja_ginza')

        nlp.vocab.reset_vectors(width=w2v_model.vectors.shape[1])
        for word in w2v_model.vocab.keys():
            nlp.vocab[word]
            nlp.vocab.set_vector(word, w2v_model[word])

        return nlp

    @staticmethod
    def load_wiki2vec():
        print('Load wiki2vec model...')

        file_path = os.path.join(settings.BASE_DIR, 'webapi/modeles/jawiki_20180420_100d.pkl')
        
        wiki2vec_model = Wikipedia2Vec.load(file_path)

        return wiki2vec_model