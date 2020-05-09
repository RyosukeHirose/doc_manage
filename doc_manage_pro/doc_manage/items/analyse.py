from sklearn.feature_extraction.text import TfidfVectorizer
from get_words import get_words_by_mecab


def get_tfidf_and_feature_names(corpus):
    vectorizer = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')

    X = vectorizer.fit_transform(corpus)
    feature_words = vectorizer.get_feature_names()
    for doc_id, vec in zip(range(len(corpus)), X.toarray()):
        print("doc_id:{}".format(doc_id))
        print("----------------------")
        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True ):
            lemma = feature_words[w_id]
            print('\t{0:s}: {1:f}'.format(lemma, tfidf))

    return vectorizer.fit_transform([get_words_by_mecab(text) for text in corpus]), vectorizer.get_feature_names()



