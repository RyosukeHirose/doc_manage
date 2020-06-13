# coding: UTF-8
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import scipy.sparse.csr
import pickle


def cos(self):
    """
    ファイル毎のスペース区切りの単語リストとファイルリストから、tdidfを計算してDBに保存する
    例
    corpus: ['Ruby Python PHP Java', 'AWS GCP オンプレ sakura']
    pdf_names:['6.pdf', '5.pdf']
    """
    corpus = [
        '大迫 今日 まじ 半端 ねぇ！',
        '大迫 半端 ない っ て！',
        '大迫 半端 なか った',
        '乾 だって 半端 ない ！',
        '川島 の イエロー も 半端 ない',
        'ね ！ 本田 も 入れた 意味 あった し 上手く 相手 に 刺さった から いいわ 大迫 半端 ない って。',
        'セネガル 人 半端 ない って 泣',
        'うーん 宇佐美 と 酒井 高徳 全然 輝いて ねぇ',
        '香川 の PK も 半端 なか った よ ！ 笑',
        '1 - 0 で コロンビア 勝ち って の は ベスト な 展開 なん す けど ねぇ …',
    ]
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    # tftidを計算
    X = vectorizer.fit_transform(corpus)
    # Numpyでtftidを計算を保存
    np.save('doc_manage/media/test_vector.npy', X.toarray())

    #学習データ（vectorizer）の保存
    file_name="doc_manage/media/params.pkl"
    with open(file_name, 'wb') as f:
        pickle.dump(vectorizer, f)
    print("#save vectorizer OK!")

    # feature_words = vectorizer.get_feature_names()

    # tftid計算の復元 なぜかファイル名は拡張子をつけないとロードできない
    X = scipy.sparse.csr.csr_matrix(np.load('doc_manage/media/test_vector.npy'))

    # 学習データの復元
    vectorizer =None
    with open(file_name, 'rb') as f:
        vectorizer = pickle.load(f)
    print("load vectorizer OK!!")

    sample = ['ホンダ 半端 ねぇ']
    sample_X = vectorizer.transform(sample)
    feature_words = vectorizer.get_feature_names()

    # print("文書数 単語数:{}".format(sample_X.shape))
    # print("feature_words:{}".format(feature_words))

    similarity = cosine_similarity(sample_X, X)[0]

    topn_indices = np.argsort(similarity)[::-1]
    datas = zip(similarity[topn_indices], np.array(corpus)[topn_indices])

    for sim, tweet in zip(similarity[topn_indices], np.array(corpus)[topn_indices]):
        print("({:.2f}): {}".format(sim, "".join(tweet.split())))
        

