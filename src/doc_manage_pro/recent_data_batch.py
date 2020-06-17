import requests
import os
import django
from datetime import datetime
from django.utils.timezone import localtime
import MySQLdb
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')



def get_aricle_from_qiita():
    """
    QiitaのAPIで記事データ（タイトル,URL,記事作成日）を取得
    article['body']:本文のマークダウン形式の文字列
    """
    word_list_every_file = []
    file_list = []
    start_time = datetime.now()
    registeres_articles = File.objects.all().order_by('-created_of_article')
    last_article_date = localtime(registeres_articles[0].created_of_article) if registeres_articles.count() >=1 else datetime.strptime('2000-01-01T12:36:10+09:00', '%Y-%m-%dT%H:%M:%S%z')
    count = 1
    break_flag =False
    # QiitaAPIで文字列取得
    for i in range(1,101):
        try:
            if break_flag:
                break
            headers = {
                'Authorization': 'Bearer {}'.format(os.environ['QiitaAccess']),
            }
            params = (
                ('per_page', '100'),
                ('page', i),
            )
            responses = requests.get('https://qiita.com/api/v2/items', headers=headers, params=params)
            

            if responses:
                for article in responses.json():
                    body = article['body']
                    url = article["url"]                    
                    # pdf作成時のタイトルに/があったらエラーが出るので取り除く
                    title = article["title"].replace("/", "")
                    # 作成日はタイムゾーンつきのdateオブジェクトに変換
                    created_of_article = datetime.strptime(article["created_at"], '%Y-%m-%dT%H:%M:%S%z')
                    
                    # すでにデータベースに登録されている記事を記事作成日で降順に並べ、今回取得してきた記事とくらべる
                    # 過去に取得している記事に入ったらそれ以降はすでに取得ずみなのでbreak
                    if created_of_article <=  last_article_date:
                        print('This page of Qiita API done!')
                        break_flag = True
                        break
                    # データベースに必要情報を登録
                    else:
                        """
                        pdfとして保存する場合。今回は保存せずAPIのreturnから取得する
        
                        # file_path = make_pdf_from_url(url, title)
                        # file_name = os.path.basename(file_path)
                        # text = get_all_text_from_pdf(file_path)
                        # listを繋げてスペース区切りの文字列に変化
                        # text_all = list_to_text(text)
                        """
                        # APIを利用して本文を取得
                        # 本文からurlを削除
                        text_all = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" ,body)
                        # 本文からタグを削除
                        text_all = re.sub(r"<[^>]*?>", "" ,text_all)

                        # # スペース区切りの文字列を取得
                        words_list = get_words_by_mecab(text_all)

                        # # 次回からの計算の簡略化のためにデータベースの保存
                        file = File.objects.update_or_create(
                            file_name=title,
                            words_list=words_list,
                            # file_path=file_path,
                            created_of_article=article["created_at"],
                            url=url
                        )
                        print('No.{} file:{}, registered'.format(count, title))
                        count += 1
        except MySQLdb.OperationalError as e:
            print('get OperationalError')
        except Exception as e:
            print('get unknownerror:{}'.format(e))


    
    all_articles = File.objects.all()
    for article in all_articles:
        word_list_every_file.append(article.words_list)
        file_name = article.file_name
        file_list.append(file_name)

    # コサイン類似度を学習して、単語数を取得
    file_count, word_count   = calculate_tdidf(word_list_every_file, file_list)
    print("calculate_tdidf done")

    # 開始時間から処理のかかった時間を計測
    finish_time = datetime.now() - start_time
    total_time = round(finish_time.total_seconds(),1 )
    print(total_time)
        


if __name__ == '__main__':
    django.setup()
    from doc_manage.models import File, LastFile
    from doc_manage.items.make_pdf import make_pdf_from_url
    from doc_manage.items.file_reader import list_to_text, get_all_text_from_pdf
    from doc_manage.items.get_words import get_words_by_mecab
    from doc_manage.items.analyse import calculate_tdidf

    get_aricle_from_qiita()