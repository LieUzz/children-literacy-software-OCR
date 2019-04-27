from django.core.files.storage import default_storage
from django.http import JsonResponse
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from urllib.request import Request, urlopen
from django.core.files.base import ContentFile
from tool.utils.division import my_division,cut
from PIL import Image
from . import models
import json
import urllib.parse
import urllib
import re
import book_api.models
import word_api.models
import ocr_api.models
import usr_api.models
import pytesseract
import cv2
from datetime import *
import numpy
import os



def open_url(url):

    # 包装头部
    firefox_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # print(1)
    # 构建请求
    request = Request(url, headers=firefox_headers)
    # print(2)
    html = urlopen(request)
    # print(3)
    # 获取数据
    data = html.read()
    # print(4)
    return data


class ReView(APIView):
    #用于正则获取儿童专栏书籍的id
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}

        try:
            # result = re.search(r'.','I love u.')
            # print(result)
            book_id_list=['']*900
            print(book_id_list)
            for i in range(330, 900):
                url = 'https://book.douban.com/tag/%E7%AB%A5%E8%AF%9D?start=' + str(i) + '&type=T'
                html = open_url(url)
                html = html.decode('utf-8')
                result = r'https://book.douban.com/subject/([0-9]{7}|[0-9]{8})'
                book_id = re.findall(result,html)
                book_id_list[i] = book_id[0]
                models.KidsBook.objects.update_or_create(id = i+1, isbn=book_id_list[i])
                # html = open_url(book_id[0])
                # print(html)
            print(book_id_list)
            ret['msg'] = 'success'

            # #获取出版社名称
            # row_publisher = r'<span class="pl">出版社:</span>([\s\S]*)<span class="pl">原作名:</span>'
            # publisher = re.findall(row_publisher,html)
            # publisher = re.findall(r'[^\x00-\xff]',publisher[0])
            # #
            # # print(publisher)
            # # print(len(publisher))
            # real_publisher = ''
            # for i in range(len(publisher)):
            #     real_publisher = real_publisher+publisher[i]
            # # print(real_publisher)
            #
            #
            # # 获取书籍ISBN
            # row_isbn = r'<span class="pl">ISBN:</span>([\s\S]*)<div id="interest_sectl" class="">'
            # isbn = re.findall(row_isbn, html)
            # # print(isbn)
            # isbn = re.findall(r'[\d]', isbn[0])
            #
            # # print(isbn)
            # # print(len(isbn))
            # real_isbn = ''
            # for i in range(len(isbn)):
            #     real_isbn = real_isbn + isbn[i]
            # # print(real_isbn)


            # # 获取书籍内容简介59
            # row_summary = r'<span class="">内容简介</span>([\s\S]*)<span class="">作者简介</span>'
            # summary = re.findall(row_summary, html)
            # summary = re.findall(r'<div class="intro">([\s\S]*)', summary[0])
            # summary = re.findall(r'[^\x00-\xff]',summary[0])
            # print(len(summary))
            # real_summary = ''
            # for i in range(len(summary)):
            #     real_summary = real_summary + summary[i]
            # print(real_summary)



        except Exception as e:
            pass

        return JsonResponse(ret)

class BookView(APIView):
    #用于获取书籍详情
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}

        try:
            book_id = book_api.models.KidsBook.objects.all()
            for i in range(293):
                url = 'https://api.douban.com/v2/book/isbn/' + str(book_id[i].isbn) + '?apikey=0b2bdeda43b5688921839c8ecb20399b'
                # 包装头部
                firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                # 构建请求
                request = Request(url, headers=firefox_headers)
                html = urlopen(request)
                # 获取数据
                data = html.read()
                # 转换成JSON
                data_json = json.loads(data)
                print(data_json)

                votes = data_json['rating']['numRaters']
                print(votes)
                rating = data_json['rating']['average']
                print(rating)

                # title = data_json['title']
                # # print(title)
                # author = data_json['author'][0]
                # # author = '无'
                # isbn13 = data_json['isbn13']
                # # print(isbn13)
                # publisher = data_json['publisher']
                # # print(publisher)
                # summary = data_json['summary']
                # simage = data_json['images']['small']
                # mimage = data_json['images']['medium']
                # limage = data_json['images']['large']
                # print(title,author,isbn13,publisher,summary,simage,mimage,limage)
                book = book_api.models.KidsBook.objects.filter(isbn=book_id[i].isbn).first()
                book.rating = rating
                book.votes = votes
                book.save()

            ret['msg'] = 'success'

            # print('作者',author)
            # print('ISBN',isbn13)
            # print('出版社',publisher)
            # print('简介',summary)
            # print('图片',simage)
            # print('图片', mimage)
            # print('图片', limage)

        except Exception as e:
            pass

        return JsonResponse(ret)

class WordView(APIView):
    #用于汉字数据库的建立
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}

        try:
            print(123)
            # # 获取3000个汉字的zi
            # word = word_api.models.BaseWords.objects.all()
            # for i in range(0,2995):
            #     ocr_api.models.Words.objects.update_or_create(id=word[i].id,zi=word[i].word)

            #获取汉字的笔画数，拼音，意思等
            word = word_api.models.BaseWords.objects.all()
            for i in range(100,2995):
                print(word[i].word)
                obj = ocr_api.models.Words.objects.filter(zi=word[i].word).first()
                print(123)
                wordurl = urllib.parse.quote(word[i].word)
                print(wordurl)
                # 聚合数据的新华字典调用
                    #b58d89a05c7170a092bcc2ef8feb5c3b
                    #c98072ebc854fe0849d07ee107330560
                    #
                url = 'http://v.juhe.cn/xhzd/query?key=c98072ebc854fe0849d07ee107330560&word=' + str(wordurl)
                # 包装头部
                firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                # 构建请求
                request = Request(url, headers=firefox_headers)
                html = urlopen(request)
                # 获取数据
                data = html.read()
                # 转换成JSON
                data_json = json.loads(data)
                print(data_json)
                zi = data_json['result']['zi']
                print(zi)
                pinyin = data_json['result']['pinyin']
                bihua = data_json['result']['bihua']
                yisi1 = data_json['result']['jijie'][2]
                yisi2 = data_json['result']['jijie'][3]
                yisi3 = data_json['result']['jijie'][4]
                obj.pinyin = pinyin
                print(pinyin)
                obj.bihua = bihua
                print(bihua)
                obj.yisi1 = yisi1
                print(yisi1)
                obj.yisi2 = yisi2
                print(yisi2)
                obj.yisi3 = yisi3
                print(yisi3)
                obj.save()
                # ret['word'] = zi
                # ret['pinyin'] = pinyin
                # ret['bihua'] = bihua
                # ret['yisi1'] = yisi1
                # ret['yisi2'] = yisi2
                # ret['yisi3'] = yisi3


            # # 获取汉字部首
            # word = word_api.models.BaseWords.objects.all()
            # for i in range(0,1):
            #     print(word[i].word)
            #     obj = ocr_api.models.Words.objects.filter(zi=word[i].word).first()
            #     bushou =



        except Exception as e:
            pass
        return JsonResponse(ret)

class BaiDuHanZiView(APIView):
    #用于正则获取百度汉字详情
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            # 新建词汇表
            # word_pre = api.models.BaseWords.objects.all()
            # for i in range(2995):
            #     models.Word.objects.update_or_create(word=word_pre[i].word)

            obj = models.Word.objects.all()
            # print(len(obj))

            for i in range(len(obj)):
                print('start')
                # 去除数据库里的多余字段
                # yisi1 = obj[i].yisi1.replace('<strong>', '').replace('</strong>', '')
                # yisi2 = obj[i].yisi2.replace('<strong>', '').replace('</strong>', '')
                # yisi3 = obj[i].yisi3.replace('<strong>', '').replace('</strong>', '')
                # obj[i].yisi1 = yisi1
                # obj[i].yisi2 = yisi2
                # obj[i].yisi3 = yisi3
                # obj[i].save()

                # print(i)
                # print(obj[i].word)
                # word = obj[i].word
                # url = 'https://hanyu.baidu.com/s?wd='+str(urllib.parse.quote(word))+'&from=zici'
                # html = open_url(url)
                # html = html.decode('utf-8')
                # word_obj = models.Word.objects.filter(word=word).first()
                # # print(html)
                #
                # # 获取汉字gif
                # row_gif = r' <img id="word_bishun" class="bishun" data-gif="(.*?)" src="/static/asset/img_wise/video-stroke.png"/>'
                # gif = re.findall(row_gif,html)
                # # print(gif[0])
                # print(len(gif))
                # if len(gif) == 0:
                #     word_obj.gif = ' '
                #     word_obj.save()
                # else:
                #     print(gif[0])
                #     word_obj.gif = gif[0]
                #     word_obj.save()
                #
                # # 获取汉字拼音
                # re_pinyin = r'<label>拼 音</label>([\s\S]*)<label>部 首</label>'
                # pinyin = re.findall(re_pinyin, html)
                # if len(pinyin)==0:
                #     word_obj.pinyin = ' '
                #     word_obj.save()
                # else:
                #     word_obj.pinyin = ''
                #     word_obj.save()
                #     soup = BeautifulSoup(pinyin[0],'html.parser')
                #     # print(soup.prettify())
                #     pinyin = soup.find_all('b')
                #     # print(123)
                #     # print(pinyin)
                #     # print(pinyin[0])
                #     word_obj = models.Word.objects.filter(word=word).first()
                #     for i in range(len(pinyin)):
                #         pinyin_ci = str(pinyin[i])[3:-4]
                #         print(pinyin_ci)
                #         word_obj.pinyin = word_obj.pinyin + pinyin_ci + ' '
                #         word_obj.save()
                #
                #     word_obj.pinyin = word_obj.pinyin.lstrip()
                #     word_obj.save()
                #
                # # 获取汉字部首
                # re_bushou = r'<label>部 首</label>([\s\S]*)<label>笔 画</label>'
                # bushou = re.findall(re_bushou, html)
                # # print(bushou)
                # if len(bushou) ==0:
                #     word_obj.bushou = ' '
                #     word_obj.save()
                # else:
                #     soup = BeautifulSoup(bushou[0], 'html.parser')
                #     bushou = soup.find_all('span')
                #     # print(bushou[0])
                #     bushou_ci = str(bushou[0])[6:-7]
                #     print(bushou_ci)
                #     word_obj = models.Word.objects.filter(word=word).first()
                #     word_obj.bushou = bushou_ci
                #     word_obj.save()
                #
                # # 获取部首笔画
                # re_bihua = r'<label>笔 画</label>([\s\S]*)<label>五 行</label>'
                # bihua = re.findall(re_bihua, html)
                # # print(bihua)
                # if len(bihua) ==0:
                #     continue
                # else:
                #     soup = BeautifulSoup(bihua[0],'html.parser')
                #     bihua = soup.find_all('span')
                #     # print(bihua[0])
                #     bihua_ci = str(bihua[0])[6:-7]
                #     print(bihua_ci)
                #     word_obj.bihua = bihua_ci
                #     word_obj.save()
                #
                # # 获取词汇意思
                # re_yisi = r'基本释义([\s\S]*)查看更多'
                # yisi = re.findall(re_yisi,html)
                # # print(yisi)
                # if len(yisi) == 0:
                #     word_obj.yisi1 = ' '
                #     word_obj.yisi2 = ' '
                #     word_obj.yisi3 = ' '
                #     word_obj.save()
                # else:
                #     soup = BeautifulSoup(yisi[0],'html.parser')
                #     yisi = soup.find_all('p')
                #     # print(yisi[0])
                #     yisi1 = ''
                #     yisi2 = ''
                #     yisi3 = ''
                #     if yisi[0] != None:
                #         yisi1 = str(yisi[0]).replace('<span>', '').replace('</span>', '').replace('<p>', '').replace('</p>', '')
                #     if yisi[1] != None:
                #         yisi2 = str(yisi[1]).replace('<span>', '').replace('</span>', '').replace('<p>', '').replace('</p>', '')
                #     if yisi[2] != None:
                #         yisi3 = str(yisi[2]).replace('<span>', '').replace('</span>', '').replace('<p>', '').replace('</p>', '')
                #     word_obj.yisi1 = yisi1
                #     word_obj.yisi2 = yisi2
                #     word_obj.yisi3 = yisi3
                #     word_obj.save()

            ret['msg'] = 'success'


        except Exception as e:
            pass

        return JsonResponse(ret)

class OCRView(APIView):
    #用于ocr检测
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            img_row = request.FILES.get('images')
            image_PIL = Image.open(ContentFile(img_row.read()))
            image = cv2.cvtColor(numpy.asarray(image_PIL), cv2.COLOR_RGB2BGR)
            print(type(image))
            sp = image.shape
            print(sp)
            word = pytesseract.image_to_string(image, lang='chi_sim',
                                               config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')

            ret['msg'] = 'success'
            ret['word'] = word

        except Exception as e:
            pass

        return JsonResponse(ret)

class GetPiontView(APIView):
    #用于ocr检测
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        ret = {'code': 1001, 'word': None, 'gif': None, 'pinyin': None, 'bihua': None, 'bushou': None,
               'yisi1': None, 'yisi2': None, 'yisi3': None}

        try:
            point_x = request._request.GET.get('point_x')
            point_y = request._request.GET.get('point_y')
            username = request._request.GET.get('username')
            user_obj = usr_api.models.UserInfo.objects.filter(username=username).first()
            print(user_obj)

            # print(type(point_x))
            print('X:',point_x)
            print('Y:', point_y)
            point = [0,0]
            # print(point)
            img = cv2.imread("/Users/zhengjiayu/DjangoProject/bishe/media/images.png")
            imgo = cv2.imread("/Users/zhengjiayu/DjangoProject/bishe/media/images.png", 0)
            # img = cv2.imread("/home/OCR/media/images.png")
            # imgo = cv2.imread("/home/OCR/media/images.png", 0)
            point[0] = int(point_x)
            point[1] = int(point_y)
            print('2 point:',point)
            ###########

            image_cut = cut(img, int(point_x),int(point_y))
            imageo_cut = cut(imgo, int(point_x), int(point_y))
            image = Image.fromarray(cv2.cvtColor(image_cut, cv2.COLOR_BGR2RGB))
            image.show()
            #
            #
            print('success cut')




            result = my_division(image_cut, imageo_cut)
            image = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            image.show()


            print('success division')

            word = pytesseract.image_to_string(result, lang='chi_sim',
                                               config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
            print('汉字：',word)
            if(len(word) == 0):
                ret['code'] = 2000
                print('无汉字')

            word_obj = models.Word.objects.filter(word=word).first()
            print(word_obj)
            wordexit = ocr_api.models.UserWordHistory.objects.filter(user_id=user_obj.id, wordinfo_id=word_obj.id).first()
            print(123)
            if wordexit:
                wordexit.time = datetime.now()
                wordexit.save()
            else:
                print('create')
                ocr_api.models.UserWordHistory.objects.create(user_id=user_obj.id, wordinfo_id=word_obj.id)

            ret['word'] = word_obj.word
            ret['gif'] = word_obj.gif
            ret['pinyin'] = word_obj.pinyin
            ret['bushou'] = word_obj.bushou
            ret['bihua'] = word_obj.bihua
            ret['yisi1'] = word_obj.yisi1
            ret['yisi2'] = word_obj.yisi2
            ret['yisi3'] = word_obj.yisi3

        except Exception as e:
            pass

        return JsonResponse(ret)

class GetImgOneView(APIView):
    # 用于获取并识别汉字
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1001, 'msg': None, 'print':None, 'len':None, 'word':None}
        try:
            # 获取图片FILES
            img_row = request.FILES.get('images')
            ret['print'] = str(type(img_row))
            ret['len'] = str(len(img_row))
            if os.path.exists('/home/OCR/media/images.png'):
                os.remove('/home/OCR/media/images.png')
                print('已删除图片')


            # if os.path.exists('/Users/zhengjiayu/DjangoProject/bishe/media/origin9.png'):
            #     os.remove('/Users/zhengjiayu/DjangoProject/bishe/media/origin9.png')
            #     print('已删除图片')
            # # 将image转化成PILLOW格式，然后再由PILLOW转化成opencv格式
            # image_PIL = Image.open(ContentFile(img_row.read()))
            # image = cv2.cvtColor(numpy.asarray(image_PIL), cv2.COLOR_RGB2BGR)
            # imageo = cv2.cvtColor(numpy.asarray(image_PIL), cv2.COLOR_RGB2BGR)
            # point = [55,125]
            #
            # result =  my_division(image, imageo, point)
            #
            # word = pytesseract.image_to_string(result, lang='chi_sim')
            # ret['word'] = word
            # print(word)


            # 保存图片
            # 方法一
            # 服务端
            default_storage.save('/home/OCR/media/' + img_row.name,
                                 ContentFile(img_row.read()))
            # 本地
            # default_storage.save('/Users/zhengjiayu/DjangoProject/bishe/media/' + img_row.name,
            #                      ContentFile(img_row.read()))


            # 方法二
            # image = Image.open(ContentFile(img_row.read()))
            # image.show()

            # # print(1)
            # image.save(img_row.name)
            # print(2)


            # 方法三
            # with open('cat.jpg', 'wb') as f:
            #     f.write(img)


            ret['msg'] = 'success'

        except Exception as e:
            pass
        return JsonResponse(ret)
