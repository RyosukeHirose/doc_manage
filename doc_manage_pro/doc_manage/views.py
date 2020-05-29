import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
# form
from .forms import UploadFileForm
from .forms import SearchForm
# view
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

# others
from datetime import datetime
import glob
# 手作り
from .items.file_reader import register
from .items.search import search_from_word
from .items.analyse import get_tfidf_and_feature_names
from .items.file_reader import get_all_text_from_pdf, list_to_text
from .items.get_words import get_words_by_mecab
from .items.make_pdf import make_pdf_from_url

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/media/'  # アップロードしたファイルを保存するディレクトリ

def make_pdf(self):
    make_pdf_from_url(self)
    return redirect('doc:upload_complete')  

def index(self):
    return redirect('doc:upload') 

# アップロードされた日のフォルダがあればそのままreturn 、なければ作成してreturn
def upload_date(date):
    date_file = os.listdir(path=UPLOAD_DIR)
    print("date_file:{}".format(date_file))
    if date in date_file:
        return date
    else:
        os.makedirs(UPLOAD_DIR + date)
        return date



# アップロードされたファイルのハンドル
def handle_uploaded_file(f):
    update_date = upload_date(datetime.now().strftime('%Y%m%d'))
    print("now:{}".format(datetime.now()))
    path = os.path.join(UPLOAD_DIR + '/' + update_date, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# ファイルアップロード
class Upload(FormView):
    template_name = 'upload.html'
    form_class = UploadFileForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context = {
            'form': form,
        }
        return context

    def form_valid(self, form):
        handle_uploaded_file(self.request.FILES['file'])
        return redirect('doc:upload_complete')  # アップロード完了画面にリダイレクト

# ファイルアップロード完了
class UploadComplete(FormView):
    template_name = 'upload_complete.html'
    form_class = UploadFileForm

    def get(self, request, **kwargs):
        
        context = {
        }
        return self.render_to_response(context)

# 登録されているデータから検索する
class Search(FormView):
    template_name = "result.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        start_time = datetime.now()
        search_word = self.request.POST.get('query')
        context = super().get_context_data(**kwargs)
        datas = search_from_word(search_word)

        files_and_tdidf= {}
        if datas:
            for data in datas:
                files_and_tdidf[data.file] = data.tdidf

        finish_time = datetime.now() - start_time
        finish_time = round(finish_time.total_seconds(),1 )

        context = {
            "datas": datas,
            "total_time": finish_time
        }

        return context

# tdidfを計算し直してから計算する
class Search2(FormView):
    template_name = "result.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        start_time = datetime.now()
        search_word = self.request.POST.get('query')
        context = super().get_context_data(**kwargs)
        # 保存されているパスを取得
        file_paths = glob.glob("doc_manage/media/**/*.pdf", recursive=True)    
        print(file_paths)

        word_list_every_file = []
        file_list = []

        # ファイルと中身の単語をリストにする
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            text = get_all_text_from_pdf(file_path)
            # listを繋げてスペース区切りの文字列に変化
            text_all = list_to_text(text)

            # 単語のlistまたはスペース区切りの文字列を取得
            words_list = get_words_by_mecab(text_all)

            word_list_every_file.append(words_list)
            file_list.append(file_name)

        # tdidfを計測して、単語数を取得
        word_count = get_tfidf_and_feature_names(word_list_every_file, file_name)
        # Tdidfテーブルから該当のデータを取得
        datas = search_from_word(search_word)

        files_and_tdidf= {}
        # 取得したデータを辞書に入れる
        if datas:
            for data in datas:
                files_and_tdidf[data.file] = data.tdidf

        # 開始時間から処理のかかって時間を計測
        finish_time = datetime.now() - start_time
        total_time = round(finish_time.total_seconds(),1 )

        context = {
            "total_time": total_time,
            "file_count": len(file_list),
            "word_count": word_count,
            "datas": datas
        }
        
        return context
