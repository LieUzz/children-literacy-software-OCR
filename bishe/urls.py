"""bishe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfi
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from api import views

urlpatterns = [
    path('api/test/', views.TestView.as_view()),
    path('admin/', admin.site.urls),
    #对usr的url：
    path('api/auth/', views.AuthView.as_view()),                        #POST
    path('api/register/', views.RegView.as_view()),                     #POST
    path('api/userinfo/', views.UserInfoView.as_view()),                #GET
    path('api/modifypassword/', views.ModifyPasswordView.as_view()),    #POST
    path('api/userinfoedit/',views.UserEditView.as_view()),             #POST
    path('api/fogetpassword/',views.FogetPasswordView.as_view()),       #phone，短信
    #对词汇量的url
    path('api/userwordsnum/', views.UserWordsNumView.as_view()),        #POST
    path('api/wordstest/', views.WordsTestView.as_view()),              #GET
    path('api/wordstest/f1/', views.WordsTestOneView.as_view()),        #GET
    path('api/wordstest/f2/', views.WordsTestTwoView.as_view()),        #GET
    #对书籍的url
    path('api/bookrecommend/', views.BookRecommendView.as_view()),      #GET
    path('api/doubanbook/', views.DouBanBookView.as_view()),            #GET
    #识字url
    path('api/wordinfo/', views.WordInfoView.as_view()),                #GET
    path('api/wordhistory/', views.WordHistoryView.as_view()),          #GET/POST
    path('api/wordhistory/del', views.WordHistoryView.as_view()),       #POST

    path('api/usr/', include('usr_api.urls')),
    path('api/word/', include('word_api.urls')),
    path('api/book/', include('book_api.urls')),
    path('api/ocr/', include('ocr_api.urls')),


]
