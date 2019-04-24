from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/api/word/
    path('info/', views.WordInfoView.as_view()),        #POST
    path('history/', views.WordHistoryView.as_view()),              #GET
    path('history/del/', views.HistoryDelView.as_view()),              #GET
]
