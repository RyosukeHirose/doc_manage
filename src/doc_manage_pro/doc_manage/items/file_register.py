import os
from datetime import datetime
from ..models import File

UPLOAD_DIR = os.path.dirname('/'.join(os.path.abspath(__file__).split('/')[0:-1])) + '/media/' # アップロードしたファイルを保存するディレクトリ

# アップロードされた日のフォルダがあればそのままreturn 、なければ作成してreturn
def upload_date(date):
    date_file = os.listdir(path=UPLOAD_DIR)
    if date in date_file:
        return date
    else:
        os.makedirs(UPLOAD_DIR + date)
        return date



# アップロードされたファイルのハンドル
def handle_uploaded_file(f):
    update_date = upload_date(datetime.now().strftime('%Y%m%d'))
    path = os.path.join(UPLOAD_DIR + '/' + update_date, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    file = File.objects.update_or_create(
        file_name=f.name
    )

    