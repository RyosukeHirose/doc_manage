from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.sparse.csr
import pickle


def calculate_tdidf(corpus, pdf_names):
    """
    ファイル毎のスペース区切りの単語リストとファイルリストから、コサイン類似度を学習
    例
    corpus: ['Ruby Python PHP Java', 'AWS GCP オンプレ sakura']
    pdf_names:['6.pdf', '5.pdf']
    """
    filepath = "doc_manage/media/"
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    print("in calculate_tdidf")
    # tftidを計算
    tdidf = vectorizer.fit_transform(corpus)

    # Numpyでtftid計算を保存
    np.save('{}test_vector.npy'.format(filepath), tdidf.toarray()) 
    print("done tdidf")
    # ファイルリストを保存
    with open('{}pdf_names.txt'.format(filepath), 'wb') as f:
        pickle.dump(pdf_names, f)
    print("文書数 単語数:{}".format(tdidf.shape))

    # 学習データ（vectorizer）の保存
    with open('{}params.pkl'.format(filepath), 'wb') as f:
        pickle.dump(vectorizer, f)
    print("#save vectorizer OK!")

    
    return tdidf.shape


