import os
from django.views.generic.edit import FormView

from datetime import datetime
import glob
# form
from ..forms import SearchForm
from ..items.get_words import get_word_list_and_file_list
from ..items.file_reader import list_to_text, get_all_text_from_pdf
from ..items.analyse import calculate_tdidf


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
    