from random import sample

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from api import models, serializers
import json
from urllib.request import Request, urlopen

def md5(user):
    #token的hash
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):
    #用于用户的登录认证

    authentication_classes = [ ]
    def post(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None,'token':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username = user, password = pwd).first()
            if not obj:
                ret['code']=2000
                ret['msg'] = "用户名或密码错误"
            else:
                # 为登录用户创建token
                token = md5(user)
                # 更新或创建
                models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
                ret['msg'] = "用户登录成功"
                ret['token'] = token

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
                ret['msg'] = "用户名已存在"
            else:
                obj = models.UserInfo(username = user, password = pwd, phone = phone,
                                      mail = mail, sex = sex, age = age)
                obj.save()
                models.UserWordsNum.objects.update_or_create(user=obj, defaults={'wordsnum': 0})
                ret['msg'] = "用户注册成功"

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
    #用于用户信息编辑
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该用户不存在'
            else:
                print(user_obj.username)
                user_obj.password = pwd
                user_obj.save()
                ret['msg'] = '用户密码修改成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class FogetPasswordView(APIView):
    #用于忘记密码
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if not user_obj:
                ret['code'] = 2000
                ret['msg'] = '该用户不存在'
            else:
                print(user_obj.username)
                user_obj.password = pwd
                user_obj.save()
                ret['msg'] = '用户密码修改成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class UserWordsNumView(APIView):
    #用于用户的识字量的导入
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            wordsnum = request._request.POST.get('wordsnum')
            user = request._request.POST.get('username')
            obj = models.UserInfo.objects.filter(username=user).first()
            if not obj:
                ret['code'] = 2000
                ret['msg'] = "用户名不存在"
            # 更新或创建
            models.UserWordsNum.objects.update_or_create(user=obj, defaults={'wordsnum': wordsnum})
            ret['msg'] = "用户识字量导入成功"
        except Exception as e:
            pass
        return JsonResponse(ret)

    # 用于词汇量的获取
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None, 'wordsnum':None}
        try:
            user = request._request.GET.get('username')
            print(user)
            obj = models.UserInfo.objects.filter(username=user).first()
            print(obj.id)
            wordsnum = models.UserWordsNum.objects.filter(user_id=obj.id).first()
            print(wordsnum.wordsnum)
            ret['msg'] = "用户识字量读取成功"
            ret['wordsnum'] = wordsnum.wordsnum
        except Exception as e:
            pass
        return JsonResponse(ret)

class WordsTestOneView(APIView):

    # 用于词汇量测试的第一步
    def get(self, request, *args, **kwargs):
        # ret = {'code':1001, 'msg':None}
        try:
            rand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    ]
            for i in range(0,29):
                rand[i] = sample(range(i*100+1, i*100+100), 1)
            rand[29] = sample(range(2901, 2994), 1)
            print(rand)
            rand_all = sample(range(1, 100), 0)
            for i in range(0,30):
                rand_all = rand_all +rand[i]
            print(rand_all)
            word_obj = models.BaseWords.objects.filter(id__in=rand_all)
            ser1 = serializers.WordsSerializer(instance=word_obj, many=True)
            ret = json.dumps(ser1.data, ensure_ascii=False)

        except Exception as e:
            pass
        return HttpResponse(ret)

class WordsTestTwoView(APIView):

    # 用于词汇量测试的第二步
    def get(self, request, *args, **kwargs):
        # ret = {'code':1001, 'msg':None}
        try:
            wordfirst = request._request.GET.get('wordfirst')
            wordlow = int(wordfirst)*100 - 100
            wordhigh = int(wordfirst)*100 + 100
            print(wordlow,wordhigh)
            rand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    ]
            for i in range(0,20):
                rand[i] = sample(range(i*10+1+wordlow, i*10+10+wordlow), 1)
            print(rand)
            rand_all = sample(range(1, 100), 0)
            for i in range(0,20):
                rand_all = rand_all +rand[i]
            print(rand_all)
            word_obj = models.BaseWords.objects.filter(id__in=rand_all)
            ser1 = serializers.WordsSerializer(instance=word_obj, many=True)
            ret = json.dumps(ser1.data, ensure_ascii=False)

        except Exception as e:
            pass
        return HttpResponse(ret)

class WordsTestView(APIView):
    # 用于词汇量测试结果
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg1':None, 'msg2':None, 'wordnum':None}
        try:
            user = request._request.GET.get('username')
            obj = models.UserInfo.objects.filter(username=user).first()
            wordfirst = request._request.GET.get('wordfirst')
            wordsecond = request._request.GET.get('wordsecond')
            wordrandom = sample(range(1, 10), 1)
            wordnum = int(wordfirst)*100 - 100 + int(wordsecond)*10 + wordrandom[0]
            print(wordfirst,wordsecond,wordnum,wordrandom)
            if not obj:
                ret['code'] = 2000
                ret['msg1'] = "用户名不存在"
            else:
                ret['msg1'] = '用户词汇量测试结果成功'
                ret['wordnum'] = wordnum
                models.UserWordsNum.objects.update_or_create(user=obj, defaults={'wordsnum': wordnum})
                ret['msg2'] = "用户识字量导入成功"

        except Exception as e:
            pass
        return JsonResponse(ret)

class BookRecommendView(APIView):

    # 用于用户书籍推荐
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.GET.get('username')
            print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            userwordsnum = models.UserWordsNum.objects.filter(user_id=user_obj.id).first().wordsnum
            print(userwordsnum)

            rank =0
            flag = 0
            if userwordsnum == 0:
                flag = 1
            elif userwordsnum < 1000:
                rank = 1
            elif userwordsnum < 1800:
                rank = 2
            elif userwordsnum < 2150:
                rank = 3
            elif userwordsnum < 2500:
                rank = 4
            elif userwordsnum < 2750:
                rank = 5
            else:
                rank = 6
            if flag==1:
                ret['msg'] = '用户未检测词汇量'
                ret['code'] = 2000
                return JsonResponse(ret)
            else:
                books = models.RecommendBook.objects.filter(recommendrank=rank)
                ser = serializers.BookRecommendSerializer(instance=books, many=True)
                ret = json.dumps(ser.data, ensure_ascii=False)

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

class TestView(APIView):

    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None,'token':None}
        try:
            # isbn = request._request.GET.get('isbn')
            # 豆瓣网站获取数据Api
            obj_id = models.RecommendBook.objects.filter(id=1).first()
            i = 1
            while obj_id:
                i = i + 1
                obj_id = models.RecommendBook.objects.filter(id = i).first()
                isbn = obj_id.isbn
                url = 'https://api.douban.com/v2/book/isbn/'+isbn+'?apikey=0b2bdeda43b5688921839c8ecb20399b'
                # 包装头部
                firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                # 构建请求
                request = Request(url, headers=firefox_headers)
                html = urlopen(request)
                # 获取数据
                data = html.read()
                # 转换成JSON
                data_json = json.loads(data)
                # print(data_json)
                title = data_json['title']
            # author = data_json['author'][0]
            # isbn13 = data_json['isbn13']
            # publisher = data_json['publisher']
            # summary = data_json['summary']
                simage = data_json['images']['small']
                mimage = data_json['images']['medium']
                limage = data_json['images']['large']
                print('书名',title)
                obj_id.simage = simage
                obj_id.mimage = mimage
                obj_id.limage = limage
                obj_id.save()
            # print('作者',author)
            # print('ISBN',isbn13)
            # print('出版社',publisher)
            # print('简介',summary)
            # print('图片',simage)
            # print('图片', mimage)
            # print('图片', limage)
            # datas = json.dumps(data,ensure_ascii=False)
            obj = models.RecommendBook.objects.filter(id=1).first()

            # models.RecommendBook.objects.create(title= title,author=author,isbn=isbn13,recommendrank=6,
            #                                     publisher=publisher,summary=summary,image=images)
            # obj.title = title
            # obj.author = author
            # obj.isbn = isbn13
            # obj.publisher = publisher
            # obj.summary = summary
            # obj.image = images
            # obj.save()
            ret['msg']='查找数据成功'


        except Exception as e:
            pass
        return JsonResponse(ret)