from django.urls import path
from . import  views

urlpatterns = [
    path('', views.upload_and_compress_image, name="upload_image")
]