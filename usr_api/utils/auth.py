from rest_framework import exceptions
from usr_api import models
from rest_framework.authentication import BaseAuthentication

class Authentication(BaseAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        if not token:
            token = request._request.POST.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user,token_obj)

    def authenticate_header(self,request):
        pass
