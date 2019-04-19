from random import sample
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models, serializers
import book_api.models
import json


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
        ret = {'code':1001, 'msg':None, 'wordnum':None}
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
                ret['msg'] = "用户名不存在"
            else:
                ret['msg'] = '用户词汇量测试结果成功'
                ret['wordnum'] = wordnum
                # models.UserWordsNum.objects.update_or_create(user=obj, defaults={'wordsnum': wordnum})
                # ret['msg2'] = "用户识字量导入成功"

        except Exception as e:
            pass
        return JsonResponse(ret)


