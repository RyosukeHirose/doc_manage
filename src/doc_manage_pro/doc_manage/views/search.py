import os
from django.views.generic.edit import FormView
from django.contrib import messages
from datetime import datetime
import glob
import re
# form
from ..forms import SearchForm
from ..items.get_words import get_word_list_and_file_list, get_words_by_mecab
from ..items.file_reader import list_to_text, get_all_text_from_pdf
from ..items.analyse import calculate_tdidf
from ..items.make_pdf import make_pdf_from_url
from ..items.con_similarity import cos_similarity

from ..models import File
import environ

env = environ.Env()
env.read_env('.env')


class Calculate(FormView):
    """
    保存されているファイルから、tftdf計算を行うメソッド
    """
    template_name = "result.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        start_time = datetime.now()
        print("Calculate start at {}".format(start_time))
        context = super().get_context_data(**kwargs)
        # 保存されているpdfのパスを取得
        file_paths = glob.glob("doc_manage/media/**/*.pdf", recursive=True)  
        print("get filepath done : {}".format(file_paths))
        file_count, word_count = self.make_tdidf(file_paths)

        # 開始時間から処理のかかった時間を計測
        finish_time = datetime.now() - start_time
        total_time = round(finish_time.total_seconds(),1 )

        context = {
            "total_time": total_time,
            "file_count": file_count,
            "word_count": word_count,
        }

        
        return context

    def make_tdidf(self, file_paths):

        # ファイルパスのリストから、ファイルの単語リストとファイルネームのリストを取得
        word_list_every_file, file_list = get_word_list_and_file_list(file_paths)
        
        # tdidfを計測して、単語数を取得
        file_count, word_count   = calculate_tdidf(word_list_every_file, file_list)

        return file_count, word_count
    
class SerchQiita(FormView):
    """
    受け取ったURLのサイトと類似しているQiita記事を探す
    """
    template_name = "upload.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        web_url = self.request.POST.get('pdf')
        qiita_pattern = "https?://qiita.com/[\w/:%#\$&\?\(\)~\.=\+\-]+"
        if re.match(qiita_pattern, web_url): 
            # qitta のURLから記事idを抜く
            qiita_data = re.match(r'https?://qiita.com/(?P<user_name>.+)/items/(?P<items_id>.+).*', web_url)
            item_id = qiita_data.group('items_id')
            word_list = self.qiita_article_get(item_id)
            
        else:
            context = super().get_context_data(**kwargs)
            name = 'search'
            try:
                file_path = make_pdf_from_url(web_url, name)
                word_list, file_list = get_word_list_and_file_list([file_path])
            except Exception as e:
                print(e)
                messages.error(self.request, '修正内容の保存に失敗しました。')
                context = {
                    "request": self.request,
                }

                return context
        print('start cos_similarity')
        datas = cos_similarity(word_list)
        results  = []
        for data in datas:
            try:
                title = data[1]
                tdidf = data[0]
                url = File.objects.filter(file_name=title)[0].url
                result = (title, tdidf, url)
                results.append(result)
            except IndexError as e:
                print('IndexError:{}'.format(e))
        print(results)
        context = {
            "results": results,
        }

        return context

    def qiita_article_get(seld, item_id):
        import requests
        headers = {
            'Authorization': 'Bearer {}'.format(env('QiitaAccess')),
        }
        print('qiita API start')
        responses = requests.get('https://qiita.com/api/v2/items/{}'.format(item_id), headers=headers)
        body = responses.json()['body']
        # 本文からurlを削除
        text_all = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" ,body)
        # 本文からタグを削除
        text_all = re.sub(r"<[^>]*?>", "" ,text_all)
        # スペース区切りの文字列を取得
        words_list = get_words_by_mecab(text_all)
        return [words_list]

