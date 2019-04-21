from django.shortcuts import render
import xml.etree.ElementTree as ET
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from urllib.request import Request, urlopen
from . import models
import urllib.parse
import urllib
import re
import book_api.models


def open_url(url):

    # 包装头部
    firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # 构建请求
    request = Request(url, headers=firefox_headers)
    html = urlopen(request)
    # 获取数据
    data = html.read()
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