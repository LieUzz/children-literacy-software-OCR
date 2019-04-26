from django.shortcuts import HttpResponse
from datetime import *
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from urllib.request import Request, urlopen
from PIL import Image
from . import models, serializers
from tool.utils.division import my_division
import json
import urllib.parse
import urllib
import tool.models
import pytesseract
import numpy
import cv2

class WordInfoView(APIView):
    # 用于用户查询词语
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1001, 'word': None, 'gif': None, 'pinyin': None, 'bihua': None, 'bushou': None,
               'yisi1': None, 'yisi2': None, 'yisi3': None}
        try:
            word = request._request.GET.get('word')
            # print(word)
            username = request._request.GET.get('username')
            # print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            word = tool.models.Word.objects.filter(word=word).first()
            wordexit = models.UserWordHistory.objects.filter(user_id=user_obj.id, wordinfo_id=word.id).first()
            if wordexit:
                wordexit.time = datetime.now()
                wordexit.save()
            else:
                print('err')
                models.UserWordHistory.objects.create(user_id=user_obj.id, wordinfo_id=word.id)

            ret['word'] = word.word
            ret['gif'] = word.gif
            ret['pinyin'] = word.pinyin
            ret['bushou'] = word.bushou
            ret['bihua'] = word.bihua
            ret['yisi1'] = word.yisi1
            ret['yisi2'] = word.yisi2
            ret['yisi3'] = word.yisi3

        except Exception as e:
            pass
        return JsonResponse(ret)

class WordInfoToolView(APIView):
    # 用于用户查询词语
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1001, 'word': None, 'pinyin': None, 'bihua': None,
               'yisi1': None, 'yisi2': None, 'yisi3': None}
        try:
            # word = request._request.GET.get('word')
            word = tool.models.Word.objects.all()

            for i in range(566, len(word)):
                print(i)
                if len(word[i].gif) == 0:


                    # print(word)
                    # print(urllib.parse.quote(word))
                    # word = urllib.parse.quote(word)
                    print(word[i].word)
                    word_zi = word[i].word
                    word_url = urllib.parse.quote(word[i].word)
                    #聚合数据的新华字典调用
                    # b58d89a05c7170a092bcc2ef8feb5c3b
                    url = 'http://v.juhe.cn/xhzd/query?key=c98072ebc854fe0849d07ee107330560&word=' + str(word_url)
                    # 包装头部
                    firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                    # 构建请求
                    request = Request(url, headers=firefox_headers)
                    html = urlopen(request)
                    # 获取数据
                    data = html.read()
                    # print(data)
                    # 转换成JSON
                    data_json = json.loads(data)
                    # print(data_json)
                    # print(data_json)
                    # print(data_json['result']['zi'])
                    # print(word[i].word)
                    # word[i].word = data_json['result']['zi']
                    tool.models.Word.objects.filter(word=word_zi).update(pinyin=data_json['result']['pinyin'],
                                                                         bushou=data_json['result']['bushou'],
                                                                         bihua=data_json['result']['bihua'],
                                                                         yisi1=data_json['result']['jijie'][2],
                                                                         yisi2=data_json['result']['jijie'][3],
                                                                         yisi3=data_json['result']['jijie'][4],)





            ret['code'] = 1100

        except Exception as e:
            pass
        return JsonResponse(ret)

class WordHistoryView(APIView):

    # 用于用户查过的词语的获取
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.GET.get('username')
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
    # def post(self, request, *args, **kwargs):
    #     ret = {'code':1001, 'msg':None}
    #     try:
    #         username = request._request.POST.get('username')
    #         print(username)
    #         word = request._request.POST.get('word')
    #         print(word)
    #         #对汉字进行urlcode编码
    #         # word = urllib.parse.quote(word)
    #         print(word)
    #         user_obj = models.UserInfo.objects.filter(username=username).first()
    #         print(user_obj.id)
    #         wordexit = models.UserWordHistory.objects.filter(user_id=user_obj.id, word=word).first()
    #         wordinfo = models.Words.objects.filter(zi=word)
    #         if wordexit:
    #             wordexit.time = datetime.now()
    #             wordexit.save()
    #             ret['msg'] = '该字已存在用户的历史记录，用户历史记录更新成功'
    #         else:
    #             models.UserWordHistory.objects.create(user_id=user_obj.id,word=word)
    #             ret['msg'] = '用户历史记录导入成功'
    #         # print(wordhis)
    #
    #     except Exception as e:
    #         pass
    #     return JsonResponse(ret)

    # # 用于用户历史记录的删除
    # def delete(self, request, *args, **kwargs):
    #     ret = {'code':1001, 'msg':None}
    #     try:
    #         username = request._request.DELETE.get('username')
    #         print(username)
    #         user_obj = models.UserInfo.objects.filter(username=username).first()
    #         print(user_obj.id)
    #         wordhis = models.UserWordHistory.objects.filter(user_id=user_obj.id).delete()
    #         print(wordhis)
    #         ret['msg'] = '用户历史记录删除成功'
    #
    #     except Exception as e:
    #         pass
    #     return JsonResponse(ret)

class HistoryDelView(APIView):

    # 用于用户历史记录的删除
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1001, 'msg': None}
        try:
            word = request._request.POST.get('word')
            # print(word)
            username = request._request.POST.get('username')
            # print(username)
            user_obj = models.UserInfo.objects.filter(username=username).first()
            word = tool.models.Word.objects.filter(word=word).first()
            wordexit = models.UserWordHistory.objects.filter(user_id=user_obj.id, wordinfo_id=word.id).first()
            if wordexit:
                models.UserWordHistory.objects.filter(user_id=user_obj.id, wordinfo_id=word.id).delete()
                ret['msg'] = '用户历史记录删除成功'
            else:
                ret['code'] = 2000
                ret['msg'] = '该条历史记录不存在'

        except Exception as e:
            pass
        return JsonResponse(ret)

class GetImgView(APIView):

    # 用于用户查过的词语的获取
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1001, 'msg': None, 'type': None, 'len': None, 'word': None}
        try:
            # 获取图片FILES
            img_row = request.FILES.get('images')
            ret['type'] = str(type(img_row))
            ret['len'] = str(len(img_row))

            # 将image转化成PILLOW格式，然后再由PILLOW转化成opencv格式
            image_PIL = Image.open(ContentFile(img_row.read()))
            image = cv2.cvtColor(numpy.asarray(image_PIL), cv2.COLOR_RGB2BGR)
            imageo = cv2.cvtColor(numpy.asarray(image_PIL), cv2.COLOR_RGB2BGR)
            point = [55, 55]

            result = my_division(image, imageo, point)

            word = pytesseract.image_to_string(result, lang='chi_sim')
            ret['word'] = word
            print(word)

            ret['msg'] = 'success'


        # ret['msg'] = 'success'

        except Exception as e:
            pass
        return JsonResponse(ret)
