from django.urls import path
from . import views

app_name = 'doc'

urlpatterns = [
    path('upload/', views.Upload.as_view(), name='upload'),
    path('doc/upload_complete/', views.UploadComplete.as_view(), name='upload_complete'),
]

# if setting.DEBUG:
#     urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)