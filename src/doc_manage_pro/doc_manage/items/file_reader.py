from django.http import HttpResponseRedirect
from django.urls import reverse

# PDF
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

# 手作りメソッド
from .get_words import get_words_by_mecab
from .analyse import calculate_tdidf

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

 
