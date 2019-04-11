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
from django.urls import path
from api import views

urlpatterns = [ 
    path('admin/', admin.site.urls),
    #对usr的url：
    path('api/auth/', views.AuthView.as_view()),
    path('api/register/', views.RegView.as_view()),
    path('api/userinfo/', views.UserInfoView.as_view()),
    path('api/userinfoedit/',views.UserEditView.as_view()),
    #对词汇量的url
    path('api/userwordsnum/', views.UserWordsNumView.as_view()),
    path('api/wordstest/', views.WordsTestView.as_view()),
    path('api/wordstest/f1/', views.WordsTestOneView.as_view()),
    path('api/wordstest/f2/', views.WordsTestTwoView.as_view()),
    #对书籍的url
    path('api/bookrecommend/', views.BookRecommendView.as_view()),
]
