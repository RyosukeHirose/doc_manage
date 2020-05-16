from ..models import File, Word, Tdidf


def search_from_word(search_word):
    feature_word = Word.objects.filter(word_name=search_word)
    datas = Tdidf.objects.filter(word=feature_word[0])

    return datas
