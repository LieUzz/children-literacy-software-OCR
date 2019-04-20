from random import sample
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models, serializers
import word_api.models
import json
from api.utils.msg import sendsms

def md5(user):
    #token的hash
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

#用户相关
class AuthView(APIView):
    #用于用户的登录认证

    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None,'token':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            print(user,pwd)
            obj = models.UserInfo.objects.filter(username = user, password = pwd).first()
            print(obj)
            if not obj:
                ret['code']=2000
                ret['msg'] = "用户名或密码错误"
            else:
                # 为登录用户创建token
                token = md5(user)
                print(token)
                # 更新或创建
                models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
                print(123)
                ret['msg'] = "用户登录成功"
                ret['token'] = token

                #创建用户推荐书籍
                # day = date.today().day
                # day = int(day)
                # print(obj.id)
                # time_obj = models.TimeGap.objects.filter(user_id=obj.id).first()
                # print(time_obj)
                # if not time_obj:
                #     models.TimeGap.objects.create(user=obj,lasttime = day, one = 1, two = 2, three=3, four =4,five = 5, six= 6,seven= 7,eight= 8,
                #                                                       nine= 9, ten= 10)


        except Exception as e:
            pass
        return JsonResponse(ret)

class MsgView(APIView):
    #用于用户注册短信验证
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            phone = request._request.GET.get('phone')
            obj = models.UserInfo.objects.filter(phone=int(phone)).first()
            print(obj)

            # 产生随机码
            msg_num = sample(range(100000, 999999), 1)
            print(msg_num[0])

            appkey = 'ea6cbc41a00baf9a77da24c28492d1e6'  # 您申请的短信服务appkey
            mobile = str(phone)  # 短信接受者的手机号码
            tpl_id = '151712'  # 申请的短信模板ID,根据实际情况修改
            tpl_value = '#code#=' + str(msg_num[0]) + '&#company#=OCR'  # 短信模板变量,根据实际情况修改

            if obj:
                ret['code']=2000
                ret['msg'] = "该手机已注册，请换一个手机注册"
            else:
                sendsms(appkey, mobile, tpl_id, tpl_value)
                models.PhoneCode.objects.update_or_create(phone = phone, defaults={'code': msg_num[0]})
                ret['msg'] = '已发送验证码'

        except Exception as e:
            pass
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            phone = request._request.POST.get('phone')
            code = request._request.POST.get('code')
            print(phone,code)

            code_db = models.PhoneCode.objects.filter(phone=phone).first().code
            if int(code) == int(code_db):
                ret['code']=1000
                ret['msg'] = "验证码正确"
            else:
                ret['code']=2000
                ret['msg'] = "验证码错误,请重新输入"

        except Exception as e:
            pass
        return JsonResponse(ret)

class RegView(APIView):
    #用于用户注册
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            phone = request._request.POST.get('phone')
            mail = request._request.POST.get('mail')
            sex = request._request.POST.get('sex')
            age = request._request.POST.get('age')

            objjudge = models.UserInfo.objects.filter(username=user).first()
            if objjudge:
                ret['code']=2000
                ret['msg'] = "用户名已注册，请更改用户名"
            else:
                obj = models.UserInfo(username = user, password = pwd, phone = phone,
                                      mail = mail, sex = sex, age = age)
                obj.save()
                word_api.models.UserWordsNum.objects.update_or_create(user=obj, defaults={'wordsnum': 0})
                ret['msg'] = "注册成功"

        except Exception as e:
            pass
        return JsonResponse(ret)

class UserInfoView(APIView):
    #用于用户信息查找
    def get(self, request, *args, **kwargs):
        # ret = {'code':1001, 'msg':None, 'data': None}
        try:
            username = request._request.GET.get('username')
            user_obj = models.UserInfo.objects.filter(username=username).first()
            ret = None
            if not user_obj:
                user = models.UserInfo.objects.all()
                ser = serializers.UserSerializer(instance=user, many=True)
                ret = json.dumps(ser.data, ensure_ascii=False)
            else:
                ser = serializers.UserSerializer(instance=user_obj, many=False)
                ret = json.dumps(ser.data,ensure_ascii=False)
            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

class UserEditView(APIView):
    #用于用户信息编辑
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            phone = request._request.POST.get('phone')
            mail = request._request.POST.get('mail')
            sex = request._request.POST.get('sex')
            age = request._request.POST.get('age')
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该用户不存在'
            else:
                print(user_obj.username)
                user_obj.phone = phone
                user_obj.mail = mail
                user_obj.sex = sex
                user_obj.age = age
                user_obj.save()
                ret['msg'] = '用户信息修改成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class ModifyPasswordView(APIView):
    #用于用户修改密码
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            old_pwd = request._request.POST.get('oldpassword')
            pwd = request._request.POST.get('password')
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该用户不存在'
            else:
                print(old_pwd,user_obj.password)
                if int(old_pwd)==int(user_obj.password):
                    print(user_obj.username)
                    user_obj.password = pwd
                    user_obj.save()
                    ret['msg'] = '用户密码修改成功'
                else:
                    ret['code'] = 2000
                    ret['msg'] = '用户原密码错误'

        except Exception as e:
            pass
        return JsonResponse(ret)

class FogetPasswordView(APIView):
    #用于忘记密码
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None}
        try:
            phone = request._request.GET.get('phone')
            user_obj = models.UserInfo.objects.filter(phone=phone).first()
            print(user_obj.username)
            #产生随机码
            msg_num = sample(range(100000, 999999), 1)
            print(msg_num[0])

            appkey = 'ea6cbc41a00baf9a77da24c28492d1e6'  # 您申请的短信服务appkey
            mobile = user_obj.phone  # 短信接受者的手机号码
            tpl_id = '151713'  # 申请的短信模板ID,根据实际情况修改
            tpl_value = '#code#=' + str(msg_num[0]) + '&#company#=OCR'  # 短信模板变量,根据实际情况修改

            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该手机未注册，用户不存在'
            else:
                print(user_obj.phone)
                models.PhoneCode.objects.update_or_create(phone=user_obj.phone, defaults={'code': msg_num[0]})
                ret['msg'] = '用户手机查找成功，已发送短信'
                sendsms(appkey, mobile, tpl_id, tpl_value)

            # ret['code'] = 1000
            # ret['msg'] = '发送短信成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            phone = request._request.POST.get('phone')
            code = request._request.POST.get('code')
            user_obj = models.UserInfo.objects.filter(phone=phone).first()
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该用户不存在'
            else:
                code_db = models.PhoneCode.objects.filter(phone=user_obj.phone).first().code
                if int(code) == int(code_db):
                    ret['msg'] = '用户验证码正确'
                else:
                    ret['code'] = 2001
                    ret['msg'] = '用户验证码输入错误'

        except Exception as e:
            pass
        return JsonResponse(ret)

class ChangePasswordView(APIView):
    #用于用户修改密码
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            phone = request._request.POST.get('phone')
            pwd = request._request.POST.get('password')
            user_obj = models.UserInfo.objects.filter(phone=phone).first()
            print(user_obj.username)
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该手机未注册'
            else:
                print(user_obj.username)
                user_obj.password = pwd
                user_obj.save()
                ret['msg'] = '用户密码修改成功'

        except Exception as e:
            pass
        return JsonResponse(ret)
