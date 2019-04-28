from urllib.request import Request, urlopen
import json
import urllib.parse
import urllib

def my_xinhua(word_zi):
    word_zi = '园'
    word_url = urllib.parse.quote(word_zi)
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
    print(data_json)
    pinyin = data_json['result']['pinyin']
    bihua = data_json['result']['bihua']
    bushou = data_json['result']['bushou']
    yisi1 = data_json['result']['jijie'][2]
    yisi2 = data_json['result']['jijie'][3]
    yisi3 = data_json['result']['jijie'][4]
    return pinyin,bihua,bushou,yisi1,yisi2,yisi3

if __name__ == '__main__':
    word_zi = '园'
    my_xinhua(word_zi)
