#coding=utf-8
import sys
import apns
import urllib2
import os
from django.http import HttpResponse
def push(msg):
    #推送需要用到的证书
    pem = 'source/apns-cer/hongdian-c-push-dev.pem'
    token = msg['udid']
    data = msg['data']
    payload = apns.Payload(msg['content'], msg['count'], data)
    return apns.APN(token, payload, pem)

def startPush(requset):
    msg = {
        'data': {'type':'feed', 'id': 123},
        'count': 8,
        'udid': '23bc82b8a5ad01bcbfc1b7166f2a543d767ace7c36acee1b151fa25d0fb7cde8',
        'content': 'ios推送测试'
    }
    push(msg)
    return HttpResponse("push_success")