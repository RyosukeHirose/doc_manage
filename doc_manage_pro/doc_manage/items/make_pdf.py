import pdfkit

# 指定できる出力オプション https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
options = {
    'page-size': 'A4',
    'margin-top': '0.1in',
    'margin-right': '0.1in',
    'margin-bottom': '0.1in',
    'margin-left': '0.1in',
    'encoding': "UTF-8",
    'no-outline': None,
    'disable-smart-shrinking': '',
}

config_path ='/code/wkhtmltox/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=config_path)
pdfkit.from_url('https://google.com', 'google.pdf', options=options, configuration=config)