from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/usr/
    path('auth/',views.AuthView.as_view()),
    path('register/',views.RegView.as_view()),
    path('register/msg/',views.MsgView.as_view()),
    path('info/',views.UserInfoView.as_view()),
    path('info/edit/',views.UserEditView.as_view()),
    path('pwd/modification/',views.ModifyPasswordView.as_view()),
    path('pwd/lost/',views.FogetPasswordView.as_view()),
]
