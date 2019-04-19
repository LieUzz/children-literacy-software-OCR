import json
from urllib.request import urlopen, quote

def main():
    appkey = 'ea6cbc41a00baf9a77da24c28492d1e6'  # 您申请的短信服务appkey
    mobile = '17376566754'  # 短信接受者的手机号码
    tpl_id = '441'  # 申请的短信模板ID,根据实际情况修改
    tpl_value = '#code#=5678&#company#=JuheData'  # 短信模板变量,根据实际情况修改

    sendsms(appkey, mobile, tpl_id, tpl_value)  # 请求发送短信


def sendsms(appkey, mobile, tpl_id, tpl_value):
    sendurl = 'http://v.juhe.cn/sms/send'  # 短信发送的URL,无需修改

    params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
             (appkey, mobile, tpl_id, quote(tpl_value))  # 组合参数

    wp = urlopen(sendurl + "?" + params)
    content = wp.read()  # 获取接口返回内容

    result = json.loads(content)

    if result:
        error_code = result['error_code']
        if error_code == 0:
            # 发送成功
            smsid = result['result']['sid']
            print("sendsms success,smsid: %s" % (smsid))
        else:
            # 发送失败
            print("sendsms error :(%s) %s" % (error_code, result['reason']))
    else:
        # 请求失败
        print("request sendsms error")


if __name__ == '__main__':
    main()