from sklearn.feature_extraction.text import TfidfVectorizer
from .get_words import get_words_by_mecab
from .data_register import register, file_check

def get_tfidf_and_feature_names(corpus, file_name, word_count):
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    # tftidを計算
    X = vectorizer.fit_transform(corpus)
    feature_words = vectorizer.get_feature_names()
    word_count += len(feature_words)
    print("feature_words:{}".format(feature_words))
    for doc_id, vec in zip(range(len(corpus)), X.toarray()):
        # print("doc_id:{}".format(doc_id))
        # print("----------------------")
        file_name = file_check(file_name)
        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True ):
            feature_word = feature_words[w_id]
            # print('\t{0:s}: {1:f}'.format(feature_word, tfidf))
            if tfidf > 0: register(doc_id, feature_word, tfidf, file_name)

    return word_count


