from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import scipy.sparse.csr
import pickle

from .get_words import get_words_by_mecab
from .data_register import file_check


def cos_similarity(corpus):
    """
    corpus : アップロードされたスペース区切りの単語リストとファイルリスト
    保存済みのtdidfを復元させて
    引数のcorpusで類似ファイルをコサイン類似値からとってくる
    例
    corpus: ['Ruby Python PHP Java', 'AWS GCP オンプレ sakura']
    pdf_names:['6.pdf', '5.pdf']
    """
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')

    # 計算済みのtftid計算の復元
    tdidf = scipy.sparse.csr.csr_matrix(np.load('doc_manage/media/test_vector.npy'))

    # 実行済みの学習データの復元
    file_name="doc_manage/media/params.pkl"
    vectorizer =None
    with open(file_name, 'rb') as f:
        vectorizer = pickle.load(f)
    print("load vectorizer OK!!")

    # アップロードされたファイルのtdidfを、保存された学習データから計算
    corpus_tdif = vectorizer.transform(corpus)

    # 類似度(TF/IDF),コサイン類似度計算 
    similarity = cosine_similarity(corpus_tdif, tdidf)[0]
    
    # 並び替えたindex番号を取得
    topn_indices = np.argsort(similarity)[::-1]

    # 保存されているファイルリストを取得
    with open("doc_manage/media/pdf_names.txt", 'rb') as f:
        pdf_names = pickle.load(f)

    datas = zip(similarity[topn_indices], np.array(pdf_names)[topn_indices])

    # 類似ファイルを類似順で表示
    # for sim, tweet in datas:
    #     print("({:.2f}): {}".format(sim, "".join(tweet.split())))
    return list(datas)




