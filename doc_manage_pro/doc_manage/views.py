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

# 手作り
from .items.file_reader import register
from .items.search import search_from_word

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/media/'  # アップロードしたファイルを保存するディレクトリ

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


class Search(FormView):
    template_name = "result.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        search_word = self.request.POST.get('query')
        context = super().get_context_data(**kwargs)
        datas = search_from_word(search_word)

        files_and_tdidf = {}
        for data in datas:
            files_and_tdidf[data.file] = data.tdidf
            print(files_and_tdidf)
            
        return context

