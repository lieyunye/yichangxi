#coding=utf-8
import sys
import apns
import urllib2
from django.http import HttpResponse
def push(msg):
    #推送需要用到的证书
    pem = 'hongdian-c-push-dev.pem'
    token = msg['udid']
    data = msg['data']
    print(os.path.exists(path))
    payload = apns.Payload(msg['content'], msg['count'], data)
    return apns.APN(token, payload, pem)

def startPush(requset):
    msg = {
        'data': {'type':'feed', 'id': 123},
        'count': 8,
        'udid': 'f435d683eb9d7e5680938c363ea6e38eba36a553e9b23ddd57f9',
        'content': 'ios推送测试'
    }
    print push(msg)
    return HttpResponse("push_success")