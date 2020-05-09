import MeCab

m = MeCab.Tagger('-Ochasen')

def get_words_by_mecab(text):
    """
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
    # listで返す
    # return words
    # スペース区切りの文字列（わかち書き）で返す
    return ' '.join(word for word in words)

