import os
import pdfkit
from .file_register import handle_uploaded_file, upload_date
from datetime import datetime
from ..models import File

def make_pdf_from_url(url, name):
    """
    PDFにしたいサイトのurlと保存したいファイル名を引数に持ってきて
    pathで指定された場所に保存
    """
    UPLOAD_DIR = os.path.dirname('/'.join(os.path.abspath(__file__).split('/')[0:-1])) + '/media/' # アップロードしたファイルを保存するディレクトリ

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'no-outline': None,
        'disable-javascript': None
    }
    make_date = upload_date(datetime.now().strftime('%Y%m%d'))
    path = os.path.join(UPLOAD_DIR + '/' + make_date, name + '.pdf')

    config_path ='/usr/local/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=config_path)
    pdfkit.from_url(url, path, configuration=config, options=options)

    
    return path

# handle_uploaded_file(pdf)
