import MeCab
import os

m = MeCab.Tagger('-Ochasen')

def get_words_by_mecab(text):
    """
    テキストから、わかち書きで単語をわけたテキストを返す
    
    単語情報のオブジェクト 
    node.feature
    例
    動詞,自立,*,*,五段・ラ行,連用形,巣ごもる,スゴモリ,スゴモリ
    名詞,サ変接続,*,*,*,*,消費,ショウヒ,ショーヒ
    助詞,格助詞,一般,*,*,*,で,デ,デ
    単語毎のlistで変換
    """
    node = m.parseToNode(text)
    words = []
    while node:        
        word_kind = node.feature.split(",")[0]
        if word_kind in ["名詞", "動詞", "形容詞"]:
            # 原型を取得
            origin = node.feature.split(",")[6]
            # 名詞の場合原型がないので、フォロー
            if origin == "*":
                words.append(node.surface)
            else:
                words.append(origin)
        node = node.next
    
    # スペース区切りの文字列（わかち書き）で返す
    return ' '.join(word for word in words)

def get_word_list_and_file_list(file_paths):
    """
    受けとったpdfのファイルパスのlistから、順番に中身を読み取り
    スペース区切りの単語の文字列に変換
    例
    file_paths: ['doc_manage/media/20200531/6.pdf', 'doc_manage/media/20200531/5.pdf'] 
    return
        word_list_every_file: ['Ruby Python PHP Java', 'AWS GCP オンプレ sakura']
        file_list:['6.pdf', '5.pdf']
    """
    from .file_reader import list_to_text, get_all_text_from_pdf
    word_list_every_file = []
    file_list = []
    # ファイルと中身の単語をリストにする
    for i, file_path in  enumerate(file_paths):
        file_name = os.path.basename(file_path)
        text = get_all_text_from_pdf(file_path)

        # listを繋げてスペース区切りの文字列に変化
        text_all = list_to_text(text)

        # スペース区切りの文字列を取得
        words_list = get_words_by_mecab(text_all)

        word_list_every_file.append(words_list)
        file_list.append(file_name)
        print('get_word_list_done from No. {}:{}'.format(i, file_name))

    return word_list_every_file, file_list