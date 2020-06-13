from datetime import datetime
import glob

from items import get_words
from items.analyse import calculate_tdidf


def calculate():
    start_time = datetime.now()
    print("Calculate start at {}".format(start_time))
    file_paths = glob.glob("doc_manage/media/**/*.pdf", recursive=True)  
    print("get filepath done")
    file_count, word_count = make_tdidf(file_paths)
    print("make pdidf done")


    # 開始時間から処理のかかった時間を計測
    finish_time = datetime.now() - start_time
    total_time = round(finish_time.total_seconds(),1 )
    print(total_time)


def make_tdidf(file_paths):

    # ファイルパスのリストから、ファイルの単語リストとファイルネームのリストを取得
    word_list_every_file, file_list = get_words.get_word_list_and_file_list(file_paths)
    print("get_word_list_and_file_list done")
    # tdidfを計測して、単語数を取得
    file_count, word_count   = calculate_tdidf(word_list_every_file, file_list)
    print("calculate_tdidf done")

    return file_count, word_count

    
    


if __name__ == '__main__':
    calculate()