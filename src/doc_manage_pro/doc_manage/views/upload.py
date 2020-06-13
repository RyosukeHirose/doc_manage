import os
from django.views.generic.edit import FormView
from django.shortcuts import redirect
import glob
from urllib.parse import urlencode, unquote
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import render_to_response

from ..forms import UploadFileForm
from ..items.file_register import handle_uploaded_file
from ..items.file_reader import get_all_text_from_pdf
from ..items.con_similarity import cos_similarity
from ..items.get_words import get_word_list_and_file_list

# ファイルアップロードして類似ファイルを検索
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
        # ファイルを保存して、保存したファイルのパスをリストに格納
        file_path = handle_uploaded_file(self.request.FILES['file'])

        base_url = reverse('doc:upload_complete')
        query_string =  urlencode({'file_path': file_path})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)  # 4

        # context = {                                                                    
        #     'test' : 'やる夫の日記',                                               
        #     'content'    : 'ケーキを食べた。',
        #     'form': form,

        # }
        
        # return self.render_to_response( 
        #     context                                                                      
        # )


# ファイルアップロード完了
class UploadComplete(FormView):
    template_name = 'upload_complete.html'
    form_class = UploadFileForm

    def get(self, request, **kwargs):
        file_path = request.GET.get('file_path')

        word_list_every_file, file_list = get_word_list_and_file_list([file_path])
        print('get_word_list_and_file_list done')
        datas = cos_similarity(word_list_every_file)

        context = {
            'datas' : datas, 
        }
        return self.render_to_response(context)