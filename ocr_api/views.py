from django.shortcuts import HttpResponse
from datetime import *
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models, serializers
import json
from urllib.request import Request, urlopen
import urllib.parse
import urllib


class WordInfoView(APIView):
    # 用于用户查询词语
    def get(self, request, *args, **kwargs):
        ret = {'code': 1001, 'word': None, 'pinyin': None, 'bihua': None,
               'yisi1': None, 'yisi2': None, 'yisi3': None}
        try:
            word = request._request.GET.get('word')
            print(word)
            print(urllib.parse.quote(word))
            word = urllib.parse.quote(word)

            #聚合数据的新华字典调用
            url = 'http://v.juhe.cn/xhzd/query?key=b58d89a05c7170a092bcc2ef8feb5c3b&word=' + str(word)
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
            zi = data_json['result']['zi']
            print(zi)
            pinyin = data_json['result']['pinyin']
            print(pinyin)
            bihua = data_json['result']['bihua']
            print(bihua)
            yisi1 = data_json['result']['jijie'][2]
            yisi2 = data_json['result']['jijie'][3]
            yisi3 = data_json['result']['jijie'][4]
            print(yisi1)
            print(yisi2)
            print(yisi3)
            ret['word'] = zi
            ret['pinyin'] = pinyin
            ret['bihua'] = bihua
            ret['yisi1'] = yisi1
            ret['yisi2'] = yisi2
            ret['yisi3'] = yisi3

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class WordHistoryView(APIView):

    # 用于用户查过的词语的获取
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.GET.get('username')
            # word = request._request.GET.get('word')
            # print(word)
            # word = urllib.parse.quote(word)
            print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            wordhis = models.UserWordHistory.objects.filter(user_id=user_obj.id).order_by('-time')
            ser = serializers.WordHistorySerializer(instance=wordhis, many=True)
            ret = json.dumps(ser.data, ensure_ascii=False)
            print(wordhis)

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

    # 用于用户查过的词语进行历史添加
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            print(username)
            word = request._request.POST.get('word')
            print(word)
            #对汉字进行urlcode编码
            # word = urllib.parse.quote(word)
            print(word)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            wordexit = models.UserWordHistory.objects.filter(user_id=user_obj.id, word=word).first()
            if wordexit:
                wordexit.time = datetime.now()
                wordexit.save()
                ret['msg'] = '该字已存在用户的历史记录，用户历史记录更新成功'
            else:
                models.UserWordHistory.objects.create(user_id=user_obj.id,word=word)
                ret['msg'] = '用户历史记录导入成功'
            # print(wordhis)

        except Exception as e:
            pass
        return JsonResponse(ret)

    # 用于用户历史记录的删除
    def delete(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.DELETE.get('username')
            print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            wordhis = models.UserWordHistory.objects.filter(user_id=user_obj.id).delete()
            print(wordhis)
            ret['msg'] = '用户历史记录删除成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class HistoryDelView(APIView):

    # 用于用户历史记录的删除
    def post(self, request, *args, **kwargs):
        ret = {'code': 1001, 'msg': None}
        try:
            username = request._request.POST.get('username')
            print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            wordhis = models.UserWordHistory.objects.filter(user_id=user_obj.id).delete()
            print(wordhis)
            ret['msg'] = '用户历史记录删除成功'

        except Exception as e:
            pass
        return JsonResponse(ret)
