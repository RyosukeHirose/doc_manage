# PDF
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from get_words import get_words_by_mecab
from analyse import get_tfidf_and_feature_names

import collections

import numpy as np

def get_all_text_from_pdf(filepath:str):
    # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
    laparams = LAParams(detect_vertical=True)
    # 共有のリソースを管理するリソースマネージャーを作成。
    resource_manager = PDFResourceManager()
    # ページを集めるPageAggregatorオブジェクトを作成。
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    # Interpreterオブジェクトを作成。
    interpreter = PDFPageInterpreter(resource_manager, device)

    results = []
    with open(filepath, 'rb') as file:
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
            layout = device.get_result()

            results.append(get_text_list_recursively(layout))
            
        return results




def get_text_list_recursively(layout):
    #テキストならそのまま返す
    if isinstance(layout, LTTextBox):
        return [layout.get_text()]

    # Containerはテキストなどを内包ため再帰探索
    if isinstance(layout, LTContainer):
        text_list = []
        for child in layout:
            text_list.extend(get_text_list_recursively(child))
        return text_list
    return []

def list_to_text(text_list):
    attach_text = ''
    for text in text_list:
        attach_text += ''.join(text)

    return attach_text

text = get_all_text_from_pdf('media/20200507/ホームページをPDFファイルとして保存する4つの方法を解説｜ferret.pdf')
# listを繋げて文字列に変化
text_all = list_to_text(text)

# 単語のlistまたはスペース区切りの文字列を取得
words_list = get_words_by_mecab(text_all)
docs = [
    'ドキュメント 集合 において ドキュメント の 単語 に 付けられる ドキュメント する',
    '情報検索 において 単語 へ の 重み付け に 使える する',
    'ドキュメント で 出現した すべて の 単語 の 総数 する'
    ]
file_list = []
file_list.append(words_list)
for doc in docs:
    file_list.append(doc)

w, feature_names = get_tfidf_and_feature_names(file_list)
# v = np.asarray([word_vectors(word) for word in feature_names])
# 単語の数を集計?
# c = collections.Counter(words_list)

# print(c.most_common(5000))

