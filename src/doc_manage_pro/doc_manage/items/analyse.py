from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.sparse.csr
from scipy.sparse import save_npz
from scipy.io import mmwrite
from scipy.sparse import csr_matrix
import pickle


def calculate_tdidf(corpus, file_names):
    """
    ファイル毎のスペース区切りの単語リストとファイルリストから、コサイン類似度を学習
    例
    corpus: ['Ruby Python PHP Java', 'AWS GCP オンプレ sakura']
    file_names:['djangoでの自然言語処理', 'コサイン類似度計算']
    """
    filepath = "doc_manage/media/"
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    print("in calculate_tdidf")
    # tftidを計算
    tdidf = vectorizer.fit_transform(corpus)
    print('done fit_transform')

    # scipy.sparse.csr.csr_matrixを保存
    save_npz('{}tdidf.npz'.format(filepath), tdidf)
    print("done save tdidf")
    # ファイルリストを保存
    with open('{}pdf_names.txt'.format(filepath), 'wb') as f:
        pickle.dump(file_names, f)
    print("文書数 単語数:{}".format(tdidf.shape))

    # 学習データ（vectorizer）の保存
    with open('{}params.pkl'.format(filepath), 'wb') as f:
        pickle.dump(vectorizer, f)
    print("#save vectorizer OK!")

    
    return tdidf.shape


