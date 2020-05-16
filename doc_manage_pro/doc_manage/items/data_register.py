import os
import sys
from ..models import File, Word, Tdidf

def file_check(file_name):
    file_name, create_check = File.objects.get_or_create(
        file_name=file_name
    )
    if create_check: print("created new file: {}".format(file_name))
    return file_name



def register(doc_id, feature_word, tfidf, file_name):
    # 該当ファイルを取得
    file = File.objects.filter(file_name=file_name)

    word, word_create_check = Word.objects.get_or_create(
        word_name=feature_word
    )
    if word_create_check: print("created word: {}".format(word))


    tdidf, tdidf_create_check= Tdidf.objects.update_or_create(
        file=file[0],
        word=word,
        defaults={"tdidf":tfidf}
    )
    # print("register_word:{}, tdif{}".format(word, tfidf)) if tdidf_create_check else print("update_word:{}, tdif{}".format(word, tfidf))

    return True

    # データ取得
    # word.files.all()

    # データ削除
    # word.files.remove(file)

# def register(request):
    # word = Word.objects.all().filter(word_name="word10")
    # file = word[0].files.all()
    # print(word)

    # file = File.objects.create(file_name="file3")
    # word = Word.objects.create(word_name="word3")
    # tdidf = Tdidf(file=file, word=word, tdidf=0.89)
    # tdidf.save()
    # return HttpResponseRedirect(reverse('doc:upload_complete'))