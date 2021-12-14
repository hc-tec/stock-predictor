
from django.urls import path
from . import views

urlpatterns = [

    path('imageUpload', views.Upload.as_view()),

]
