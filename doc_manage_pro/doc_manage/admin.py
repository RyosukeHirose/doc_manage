from django.contrib import admin

# Register your models here.
from doc_manage.models import File, Word, Tdidf
admin.site.register(File)
admin.site.register(Word)
admin.site.register(Tdidf)