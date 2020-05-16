from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from .get_words import get_words_by_mecab
from .data_register import register, file_check

def get_tfidf_and_feature_names(corpus, file_name):
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    # tftidを計算
    X = vectorizer.fit_transform(corpus)
    feature_words = vectorizer.get_feature_names()
    print("feature_words:{}".format(feature_words))

    # 単語の数をカウントする
    word_count = 0
    for word_list in corpus:
        print(len(word_list))
        word_count += len(word_list)

    for doc_id, vec in zip(range(len(corpus)), X.toarray()):
        file_name = file_check(file_name)
        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True ):
            feature_word = feature_words[w_id]
            if tfidf > 0: register(doc_id, feature_word, tfidf, file_name)

    print("単語数:{}".format(word_count))
    return word_count


