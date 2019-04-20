from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/tool/
    path('re/', views.ReView.as_view()),
    path('book/', views.BookView.as_view()),
]
