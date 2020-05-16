from django.http import HttpResponseRedirect
from django.urls import reverse

# PDF
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

# 手作りメソッド
from .get_words import get_words_by_mecab
from .analyse import get_tfidf_and_feature_names

import collections
import numpy as np
import os
import glob

def get_all_text_from_pdf(filepath:str):
    """
    return list型
    """
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
            # テキストを取得してlistにして返す
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

def register(self):
    print(os.getcwd())
    # file_path = 'doc_manage/media/20200508/ホームページをPDFファイルとして保存する4つの方法を解説｜ferret.pdf'
    file_paths = glob.glob("doc_manage/media/**/*.pdf", recursive=True)
    files_count = len(file_paths)

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        print("file_name:{}".format(file_path))
        text = get_all_text_from_pdf(file_path)
        # listを繋げて文字列に変化
        text_all = list_to_text(text)

        # 単語のlistまたはスペース区切りの文字列を取得
        words_list = get_words_by_mecab(text_all)

        # print("word_list:{}".format(words_list))
        print(type(words_list))
        word_count = 0

        word_count = get_tfidf_and_feature_names([words_list], file_name, word_count)
        print(word_count)
        
        return word_count
 
