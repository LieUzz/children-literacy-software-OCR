from random import sample
from django.shortcuts import HttpResponse
from datetime import *
from django.http import JsonResponse
from rest_framework.views import APIView
from book_api import models, serializers
import usr_api.models
import word_api.models
import json
from urllib.request import Request, urlopen


#书籍相关
class BookRankView(APIView):

    # 用于用户识字量等级
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None, 'rank':None}
        try:
            username = request._request.GET.get('username')
            print(username)
            user_obj = usr_api.models.UserInfo.objects.filter(username=username).first()
            print(user_obj.id)
            userwordsnum = word_api.models.UserWordsNum.objects.filter(user_id=user_obj.id).first().wordsnum
            print(userwordsnum)

            rank = 0
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
                ret['rank'] = rank
            else:
                ret['msg'] = '根据用户词汇量测得用户等级'
                ret['rank'] = rank

        except Exception as e:
            pass
        return JsonResponse(ret)

class BookRecommendView(APIView):

    # 用于用户书籍推荐
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            rank = request._request.GET.get('rank')
            print(rank)
            books = models.RecommendBook.objects.filter(recommendrank=rank)
            print(123)
            ser = serializers.BookRecommendSerializer(instance=books, many=True)
            ret = json.dumps(ser.data, ensure_ascii=False)

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

class IsbnView(APIView):

    # 用于用户书籍推荐
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'title':None, 'author':None, 'publisher':None, 'isbn':None, 'summary':None,
               'simage':None, 'mimage':None, 'limage':None }
        try:
            isbn = request._request.GET.get('isbn')
            print(isbn)
            url = 'https://api.douban.com/v2/book/isbn/' + str(isbn) + '?apikey=0b2bdeda43b5688921839c8ecb20399b'
            # 包装头部
            firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            # 构建请求
            request = Request(url, headers=firefox_headers)
            html = urlopen(request)
            # 获取数据
            data = html.read()
            # 转换成JSON
            data_json = json.loads(data)
            ret['title'] = data_json['title']
            # if data_json['title'] == '':
            #     ret['code'] = 2000
            ret['author'] = data_json['author']
            ret['publisher'] = data_json['publisher']
            ret['isbn'] = data_json['isbn13']
            ret['summary'] = data_json['summary']
            ret['simage'] = data_json['images']['small']
            ret['mimage'] = data_json['images']['medium']
            ret['limage'] = data_json['images']['large']
            print(data_json)
            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class FavoriteView(APIView):

    # 用于用户书架的查询
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.GET.get('username')
            print(username)
            obj = usr_api.models.UserInfo.objects.filter(username=username).first()
            if not obj:
                ret['code'] = 2000
                ret['msg'] = '用户不存在'
                return JsonResponse(ret)
            print(obj.id)
            isbns = models.FavoriteBook.objects.filter(user_id=obj.id)
            print(isbns)
            ser = serializers.FavoriteBookSerializer(instance=isbns, many=True)
            ret = json.dumps(ser.data, ensure_ascii=False)
            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

    # 用于用户书架书籍的添加
    def post(self, request, *args, **kwargs):
        ret = {'code': 1001, 'msg': None}
        try:
            username = request._request.POST.get('username')
            isbn = request._request.POST.get('isbn')
            print(username,isbn)
            obj = models.UserInfo.objects.filter(username=username).first()
            if not obj:
                ret['code'] = 2000
                ret['msg'] = '用户不存在'
                return JsonResponse(ret)
            print(obj.id)
            book_exist = models.FavoriteBook.objects.filter(isbn=isbn).first()
            if book_exist:
                ret['msg'] = '该书籍已存在'
                ret['code'] = 2000
            else:
                print(123)

                url = 'https://api.douban.com/v2/book/isbn/' + str(isbn) + '?apikey=0b2bdeda43b5688921839c8ecb20399b'
                # 包装头部
                firefox_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                # 构建请求
                request = Request(url, headers=firefox_headers)
                html = urlopen(request)
                # 获取数据
                data = html.read()
                # 转换成JSON
                data_json = json.loads(data)
                title = data_json['title']
                author = data_json['author'][0]
                publisher = data_json['publisher']
                isbn = data_json['isbn13']
                summary = data_json['summary']
                simage = data_json['images']['small']
                mimage = data_json['images']['medium']
                limage = data_json['images']['large']


                models.FavoriteBook.objects.create(user_id=obj.id,title=title,author=author,publisher=publisher,
                                                       isbn=isbn,summary=summary,simage=simage,mimage=mimage,limage=limage)
                print(123)
                ret['msg'] = '书籍已导入用户书架'

        except Exception as e:
            pass
        return JsonResponse(ret)

class FavoriteDelView(APIView):

    # 用于用户书架的删除推荐
    def post(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            username = request._request.POST.get('username')
            isbn = request._request.POST.get('isbn')
            print(username, isbn)
            obj = models.UserInfo.objects.filter(username=username).first()
            if not obj:
                ret['code'] = 2000
                ret['msg'] = '用户不存在'
                return JsonResponse(ret)
            print(obj.id)
            book_exist = models.FavoriteBook.objects.filter(user_id=obj.id, isbn=isbn).first()
            print(book_exist)
            if not book_exist:
                ret['code'] = 2000
                ret['msg'] = '该书籍不存在'
            else:
                book_exist.delete()
                ret['msg'] = '该书籍删除成功'
            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return JsonResponse(ret)

class FavoriteSearchView(APIView):

    # 用于书架书籍查询
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            bookname = request._request.GET.get('bookname')
            username = request._request.GET.get('username')
            usr = models.UserInfo.objects.filter(username=username).first()
            if not usr:
                ret['code'] = 2001
                ret['msg'] = '用户不存在'
                return JsonResponse(ret)
            print(bookname)
            obj = models.FavoriteBook.objects.filter(title__contains=bookname,user_id=usr.id)
            if not obj:
                ret['code'] = 2000
                ret['msg'] = '书籍不存在'
                return JsonResponse(ret)
            # print(book)
            ser = serializers.FavoriteBookSerializer(instance=obj, many=True)
            ret = json.dumps(ser.data, ensure_ascii=False)

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)

class KidsBookView(APIView):

    # 用于用户每日推荐
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            user = request._request.GET.get('username')
            print(user)
            user_obj = models.UserInfo.objects.filter(username=user).first()
            print(user_obj.id)
            time_obj = models.TimeGap.objects.filter(user_id=user_obj.id).first()
            day = date.today().day
            day = int(day)
            print(day)
            daygap = 0
            if not time_obj:
                models.TimeGap.objects.update_or_create(user=user_obj,
                                                        defaults={'lasttime': day, 'one': 1, 'two': 2, 'three': 3,
                                                                  'four': 4,
                                                                  'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                                                                  'nine': 9, 'ten': 10})
            else:
                daygap = day - time_obj.lasttime
            print(daygap)
            if daygap != 0:
                rand = sample(range(1, 292), 10)
                time_obj.one = rand[0]
                time_obj.two = rand[1]
                time_obj.three = rand[2]
                time_obj.four = rand[3]
                time_obj.five = rand[4]
                time_obj.six = rand[5]
                time_obj.seven = rand[6]
                time_obj.eight = rand[7]
                time_obj.nine = rand[8]
                time_obj.ten = rand[9]
                time_obj.save()
            time_obj.lasttime = day
            time_obj.save()
            print(time_obj.one)
            books = [0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0]
            books[0] = time_obj.one
            books[1] = time_obj.two
            books[2] = time_obj.three
            books[3] = time_obj.four
            books[4] = time_obj.five
            books[5] = time_obj.six
            books[6] = time_obj.seven
            books[7] = time_obj.eight
            books[8] = time_obj.nine
            books[9] = time_obj.ten

            print(books)
            book_obj = models.KidsBook.objects.filter(id__in=books)
            ser1 = serializers.KidsBookSerializer(instance=book_obj, many=True)
            ret = json.dumps(ser1.data, ensure_ascii=False)
            ret['msg'] = 'success'

        except Exception as e:
            pass
        return HttpResponse(ret)

class SearchView(APIView):

    # 用于书籍查询
    def get(self, request, *args, **kwargs):
        ret = {'code':1001, 'msg':None}
        try:
            bookname = request._request.GET.get('bookname')
            print(bookname)
            obj = models.KidsBook.objects.filter(title__contains=bookname)
            if not obj:
                ret['code'] = 2000
                ret['msg'] = '书籍不存在'
                return JsonResponse(ret)
            # print(book)
            ser = serializers.KidsBookSerializer(instance=obj, many=True)
            ret = json.dumps(ser.data, ensure_ascii=False)

            # ret['msg'] = '用户查找成功'

        except Exception as e:
            pass
        return HttpResponse(ret)


# class TestView(APIView):
#
#     authentication_classes = []
#     def get(self, request, *args, **kwargs):
#         ret = {'code':1000, 'msg':None,'token':None}
#         try:
#             # isbn = request._request.GET.get('isbn')
#             # 豆瓣网站获取数据Api
#             #431 / 675 /
#             #131 /174/220/319/337/--431/519/647/797
#                 flag = 695
#             # while flag < 131:
#                 print(flag)
#                 obj_id = models.DouBanBook.objects.filter(id = flag).first()
#                 bookid = obj_id.bookid
#                 print(bookid)
#                 url = 'https://api.douban.com/v2/book/'+str(bookid)+'?apikey=0b2bdeda43b5688921839c8ecb20399b'
#                 # 包装头部
#                 firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#                 # 构建请求
#                 request = Request(url, headers=firefox_headers)
#                 html = urlopen(request)
#                 # 获取数据
#                 data = html.read()
#                 # 转换成JSON
#                 data_json = json.loads(data)
#                 # print(data_json)
#                 title = data_json['title']
#                 print(title)
#                 author = data_json['author'][0]
#                 # author = '无'
#                 isbn13 = data_json['isbn13']
#                 # print(isbn13)
#                 publisher = data_json['publisher']
#                 # print(publisher)
#                 summary = data_json['summary']
#                 simage = data_json['images']['small']
#                 mimage = data_json['images']['medium']
#                 limage = data_json['images']['large']
#                 print('书名',title)
#                 obj_id.title = title
#                 obj_id.author = author
#                 obj_id.isbn = isbn13
#                 obj_id.publisher = publisher #431/675/695
#                 obj_id.summary = summary
#                 obj_id.simage = simage
#                 obj_id.mimage = mimage
#                 obj_id.limage = limage
#                 obj_id.save()
#                 flag = flag + 1
#             # print('作者',author)
#             # print('ISBN',isbn13)
#             # print('出版社',publisher)
#             # print('简介',summary)
#             # print('图片',simage)
#             # print('图片', mimage)
#             # print('图片', limage)
#             # datas = json.dumps(data,ensure_ascii=False)
#                 obj = models.RecommendBook.objects.filter(id=1).first()
#
#             # models.RecommendBook.objects.create(title= title,author=author,isbn=isbn13,recommendrank=6,
#             #                                     publisher=publisher,summary=summary,image=images)
#             # obj.title = title
#             # obj.author = author
#             # obj.isbn = isbn13
#             # obj.publisher = publisher
#             # obj.summary = summary
#             # obj.image = images
#             # obj.save()
#                 ret['msg']='查找数据成功'
#
#
#         except Exception as e:
#             pass
#         return JsonResponse(ret)
