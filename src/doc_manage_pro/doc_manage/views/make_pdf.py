from django.views.generic.edit import FormView
from ..items.make_pdf import make_pdf_from_url
from ..forms import SearchForm
from ..items.get_words import get_word_list_and_file_list
from ..items.con_similarity import cos_similarity

class MakePdf(FormView):
    template_name = "upload_complete.html"
    form_class = SearchForm
    def get_context_data(self, **kwargs):
        web_url = self.request.POST.get('pdf')
        name = self.request.POST.get('name')
        context = super().get_context_data(**kwargs)
        file_path = make_pdf_from_url(web_url, name)
        word_list_every_file, file_list = get_word_list_and_file_list([file_path])
        datas = cos_similarity(word_list_every_file)

        context = {
            "datas": datas,
        }

        return context