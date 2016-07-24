#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import sys
import time
import json
sys.path.append("..")

from module.baiduPushSDK.Channel import *

# channel_id = '3812879988317808329' #android
channel_id = '4244463061771694833' #android
# channel_id = '3812879988317808329' #android

msg = '{"title":"Message from Push","description":"hello world"}'
#msg_ios = '{"aps":{"alert":"iOS Message from Push","sound":"","badge":1},"key1":"value1","key2":"value2"}'
opts = {'msg_type':1, 'expires':300}

c = Channel()



# travelApp
c.setApiKey('ljYNLqCZdMzY6DsyCyzXEgdss8YmtOFL')
c.setSecretKey('8sGfm4SSDL1KFuLaPyrdHqNs9Qp9nPkG')

test_msg = {
    'title': '这是一个测试的push',
    'description': '只是个测试',
    'custom_content': {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'
    },
}
push_msg = {
    'title': '系统通知',
    'description': '距离您5000米最近的景区是：' + 'aa',
    'custom_content': {
        'content': 'value1',
    },
}
try:
    ret = c.pushMsgToSingleDevice(channel_id, json.dumps(push_msg), opts)
    print 'ret: ',
    print ret
    print c.getRequestId()
except ChannelException as e:
    print '[code]',
    print e.getLastErrorCode()
    print '[msg]',
    print e.getLastErrorMsg()
    print '[request id]',
    print c.getRequestId()

# try:
#     ret = c.pushMsgToAll(msg, opts)
#     print 'ret: ',
#     print ret
#     print c.getRequestId()
# except ChannelException as e:
#     print '[code]',
#     print e.getLastErrorCode()
#     print '[msg]',
#     print e.getLastErrorMsg()
#     print '[request id]',
#     print c.getRequestId()

# try:
#     ret = c.pushMsgToTag('test_tag', msg, 1, opts)
#     print 'ret: ',
#     print ret
#     print '[request id]',
#     print c.getRequestId()
# except ChannelException as e:
#     print '[code]',
#     print e.getLastErrorCode()
#     print '[msg]',
#     print e.getLastErrorMsg()
#     print '[request id]',
#     print c.getRequestId()

