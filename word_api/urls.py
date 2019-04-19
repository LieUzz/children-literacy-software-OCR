from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/word/
    path('info/', views.UserWordsNumView.as_view()),        #POST
    path('test/result/', views.WordsTestView.as_view()),              #GET
    path('test/step1/', views.WordsTestOneView.as_view()),        #GET
    path('test/step2/', views.WordsTestTwoView.as_view()),        #GET
]
