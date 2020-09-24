import os

import spacy
from gensim.models import KeyedVectors
from wikipedia2vec import Wikipedia2Vec
from transformers.modeling_bert import BertModel, BertForMaskedLM

from django.conf import settings
from django.apps import AppConfig


class WebapiConfig(AppConfig):
    name = 'webapi'

    print('load stop words...')
    file_path = os.path.join(settings.BASE_DIR, 'webapi/res/stopwords.txt')
    with open(file_path, 'r') as f:
        stop_words = f.read().split()

    print('load Bert...')
    file_path = os.path.join(settings.BASE_DIR, 'webapi/models/bert-base-japanese-whole-word-masking')

    bert_tokenizer = BertJapaneseTokenizer.from_pretrained(file_path)
    bert_model = BertForMaskedLM.from_pretrained(file_path)
    bert_model.eval()

    print('Load GiNZA model...')

    file_path = os.path.join(settings.BASE_DIR, 'webapi/models/chive-1.1-mc5-20200318.bin')

    w2v_model = KeyedVectors.load_word2vec_format(file_path,  binary=True)
    ginza_model = spacy.load('ja_ginza')

    ginza_model.vocab.reset_vectors(width=w2v_model.vectors.shape[1])
    for word in w2v_model.vocab.keys():
        ginza_model.vocab[word]
        ginza_model.vocab.set_vector(word, w2v_model[word])

    print('Load wiki2vec model...')

    file_path = os.path.join(settings.BASE_DIR, 'webapi/models/jawiki_20180420_100d.pkl')
    
    wiki2vec_model = Wikipedia2Vec.load(file_path)

    print('done')


    # @staticmethod
    # def load_bert():
    #     print('Load BERT model...')

    #     file_path = os.path.join(settings.BASE_DIR, 'webapi/models/bert-base-japanese-whole-word-masking')

    #     tokenizer = BertJapaneseTokenizer.from_pretrained(file_path)
    #     model = BertForMaskedLM.from_pretrained(file_path)
    #     model.eval()

    #     return model, tokenizer

    # @staticmethod
    # def load_ginza():
    #     print('Load GiNZA model...')

    #     file_path = os.path.join(settings.BASE_DIR, 'webapi/models/chive-1.1-mc5-20200318.bin')

    #     w2v_model = KeyedVectors.load_word2vec_format(file_path,  binary=True)
    #     nlp = spacy.load('ja_ginza')

    #     nlp.vocab.reset_vectors(width=w2v_model.vectors.shape[1])
    #     for word in w2v_model.vocab.keys():
    #         nlp.vocab[word]
    #         nlp.vocab.set_vector(word, w2v_model[word])

    #     return nlp

    # @staticmethod
    # def load_wiki2vec():
    #     print('Load wiki2vec model...')

    #     file_path = os.path.join(settings.BASE_DIR, 'webapi/modeles/jawiki_20180420_100d.pkl')
        
    #     wiki2vec_model = Wikipedia2Vec.load(file_path)

<<<<<<< HEAD
    #     return wiki2vec_model
=======
    #     return wiki2vec_model
>>>>>>> bf65619a2a7dfe15f3d20845d1923e311ba804c5
