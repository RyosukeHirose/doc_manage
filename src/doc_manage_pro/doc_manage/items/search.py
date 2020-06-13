# from ..models import File, Word, Tdidf


# def search_from_word(search_word):
#     feature_word = Word.objects.filter(word_name=search_word)
#     if len(feature_word) > 0:
#         datas = Tdidf.objects.filter(word=feature_word[0]).order_by('tdidf').reverse()
#         return datas
#     else:
#         return None
