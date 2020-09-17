import numpy as np
import scipy
import scipy.spatial
import spacy


class LexRank:
    def __init__(self, threshold=0.1, max_iter=100, tol=1e-06, req_pos=['NOUN']):
        self.nlp = spacy.load('ja_ginza')

        self.max_iter = max_iter
        self.tol = tol
        self.threshold = threshold
        self.req_pos = req_pos.copy()

    def summarize(self, text, topn=3):
        """
        テキスト中の重要文をtopn件返す

        Parameters
        ----------
        text : str
            要約対象となるテキスト
        topn : int
            抽出する重要文の件数

        Returns
        -------
        summary : List[str]
            重要文のリスト
        """
        doc = self.nlp(text)
        sent_text = np.array([sent.text for sent in doc.sents])

        # 文単位に分割してベクトル化
        sent_vectors = np.array([self.vectorize_sentence(sent) for sent in doc.sents])
        # lexrankを計算
        scores = self.calc_scores(sent_vectors)
        # 上位topn件の文を返す
        topn_indexes = scores.argsort()[::-1][:topn]

        return sent_text[topn_indexes]

    def vectorize_sentence(self, sentence):
        # 必要な品詞の単語のみ抽出して word vector の平均値を求める
        vecs = [token.vector for token in sentence if token.pos_ in self.req_pos]
        return np.mean(vecs, axis=0)

    def calc_scores(self, sent_vectors):
        N = len(sent_vectors)
        cos_mat = np.zeros((N, N))
        degree = np.zeros(N)

        # 隣接行列を求める
        for i in range(N):
            for j in range(N):
                cos_mat[i, j] = scipy.spatial.distance.cosine(sent_vectors[i], sent_vectors[j])
                
                if cos_mat[i, j] > self.threshold:
                    cos_mat[i, j] = 1
                    degree[i] += 1
                else:
                    cos_mat[i, j] = 0

        # 隣接行列を確率行列に変換
        for i in range(N):
            for j in range(N):
                if degree[i] > 0:
                    cos_mat[i, j] = cos_mat[i, j] / degree[i]

        return self._power_method(cos_mat, N)

    def _power_method(self, cos_mat, N):
        p_old = np.ones(N) / N
        delta = 1
        iter = 0

        while delta > self.tol:
            assert iter < self.max_iter, f'power iteration failed to converge within {self.max_iter} iterations'
            
            p = np.dot(cos_mat.T, p_old)
            delta = np.linalg.norm(p - p_old)
            p_old = p.copy()

            iter += 1

        return p

    