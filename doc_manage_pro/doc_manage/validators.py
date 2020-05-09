import os
from django.core.exceptions import ValidationError

def validate_is_file(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in['.ptt', '.pdf', '.docx']:
        raise ValidationError('Only picure pdf, ptt, docx files are availables.')
