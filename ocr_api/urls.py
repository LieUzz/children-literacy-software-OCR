from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/api/ocr/
    path('info/', views.WordInfoView.as_view()),        #POST
    path('history/', views.WordHistoryView.as_view()),              #GET
    path('history/del/', views.HistoryDelView.as_view()),              #POST
    path('img/', views.GetImgView.as_view()),
]
