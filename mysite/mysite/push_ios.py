#coding=utf-8
import sys
import apns

def push(msg):
    #推送需要用到的证书
    pem = 'apn.pem'
    token = msg['udid']
    data = msg['data']

    payload = apns.Payload(msg['content'], msg['count'], data)
    return apns.APN(token, payload, pem)

if __name__ == '__main__':
    msg = {
        'data': {'type':'feed', 'id': 123},
        'count': 8,
        'udid': 'f435d683eb9d7e5680938c363ea6e38eba36a553e9b23ddd57f9xxxxxxxxxxxx',
        'content': 'ios推送测试'
    }
    print push(msg)