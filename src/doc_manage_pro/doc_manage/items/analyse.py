from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from .get_words import get_words_by_mecab
from .data_register import register, file_check

def get_tfidf_and_feature_names(corpus, pdf_names):
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    # tftidを計算
    X = vectorizer.fit_transform(corpus)
    feature_words = vectorizer.get_feature_names()
    # 単語の数をカウントする
    word_count = 0
    for word_list in corpus:
        word_count += len(word_list)
    for doc_id, vec in zip(range(len(corpus)), X.toarray()):
        pdf_name = file_check(pdf_names[doc_id])

        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True ):
            feature_word = feature_words[w_id]
            if tfidf > 0: register(doc_id, feature_word, tfidf, pdf_name)

    print("単語数:{}".format(word_count))
    return word_count


