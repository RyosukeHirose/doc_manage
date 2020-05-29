from django.urls import path
from . import views
from .items import data_register, file_reader
app_name = 'doc'

urlpatterns = [
    path('', views.index),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('upload_complete/', views.UploadComplete.as_view(), name='upload_complete'),
    path('new/', file_reader.register, name='register'),
    path('search/', views.Search.as_view(), name='search'),
    path('search2/', views.Search2.as_view(), name='search2'),
    path('make_pdf/',views.make_pdf , name='search2')

]

# if setting.DEBUG:
#     urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)