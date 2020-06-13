from django.contrib import admin

# Register your models here.
from doc_manage.models import File, LastFile
admin.site.register(File)
admin.site.register(LastFile)
