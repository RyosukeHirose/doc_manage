import pdfkit

# def make_pdf_from_url(self):
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
}

config_path ='/usr/local/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=config_path)
pdfkit.from_url('https://nsmr.tk/pythonpdf.html', 'google.pdf', configuration=config)

# pdfkit.from_string('Hello!', 'out.pdf', configuration=config)