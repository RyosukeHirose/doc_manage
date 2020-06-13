from django.urls import path
from . import views
app_name = 'doc'

urlpatterns = [
    path('', views.views.index),
    path('upload/', views.upload.Upload.as_view(), name='upload'),
    path('upload_complete/', views.upload.UploadComplete.as_view(), name='upload_complete'),
    path('calculate/', views.search.Calculate.as_view(), name='calculate'),
    path('make_pdf/',views.make_pdf.MakePdf.as_view() , name='make_pdf'),
    # path('cos/',views.views.cos_test)

]

