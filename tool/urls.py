from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/tool/
    path('re/', views.ReView.as_view()),
    path('book/', views.BookView.as_view()),
    path('word/', views.WordView.as_view()),
    path('baiduhanzi/', views.BaiDuHanZiView.as_view()),
    path('ocr/',views.OCRView.as_view()),
    path('img/',views.GetImgView.as_view()),
    path('img/1/',views.GetImgOneView.as_view()),
]
