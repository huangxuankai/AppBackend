# encoding:utf8
from django.test import TestCase

# Create your tests here.


import datetime
import json
import time

data = {
    "name": datetime.datetime.now().now()
}

# print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1457438026727))

# dara_json = json.dumps()
#
# print json.loads(dara_json)
#
l1 = [
    u'56de86d77a74e763f3b29186',
    u'56de86d77a74e763f3b29186',
    u'56de86d77a74e763f3b29186',
    u'56de86d77a74e763f3b29186',
    u'56de86d77a74e763f3b29186',
    u'56de86d77a74e763f3b29186'
]


# print list(set(l1))
#
# list_string1 = ['123','abc','abc','cde']
# list_string2 = ['1','ac','bc','ce']


# list_string = set(list_string)
# print zip(list_string1, list_string2)


# d1 = [
#     {u'sceneId': u'56de86d77a74e763f3b29186', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230\u5f20\u5bb6\u754c', u'_id': {u'$oid': u'56de9cf07a74e708f4bf842f'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457458544670}},
#     {u'sceneId': u'56de882ae82017c1a0556b01', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230jiuzhaigou', u'_id': {u'$oid': u'56deba757a74e71e7dc54b53'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457466101701}},
#     {u'sceneId': u'56de88437a74e76673e2e7b6', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230\u51e4\u51f0\u5c71', u'_id': {u'$oid': u'56debb1c7a74e71f34b0b8c0'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457437444028}},
#     {u'sceneId': u'56de86d77a74e763f3b29186', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230\u5f20\u5bb6\u754c', u'_id': {u'$oid': u'56debb4d7a74e7202b927b5a'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457466317555}},
#     {u'sceneId': u'56de86d77a74e763f3b29186', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230\u5f20\u5bb6\u754c', u'_id': {u'$oid': u'56debb847a74e720b9d82ed8'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457437571990}},
#     {u'sceneId': u'56de86d77a74e763f3b29186', u'content': u'\u6211\u5f88\u5f00\u5fc3\u6765\u5230\u5f20\u5bb6\u754c', u'_id': {u'$oid': u'56debd4a7a74e72208f2eef3'}, u'userId': u'56dc4a407a74e720e5d3ce24', u'commentTime': {u'$date': 1457438026727}}
# ]
#
# d2 = [
#     {"province": "\u6e56\u5357\u7701", "city": "\u5f20\u5bb6\u754c", "name": "\u5f20\u5bb6\u754c", "image": "", "_id": {"$oid": "56de86d77a74e763f3b29186"}, "description": "\u8fd9\u662f\u4e00\u4e2a\u5f88\u597d\u7684\u5730\u65b9"},
#     {"province": "\u56db\u5ddd\u7701", "city": "\u4e5d\u5be8\u6c9f\u53bf", "name": "\u4e5d\u5be8\u6c9f", "image": "", "_id": {"$oid": "56de882ae82017c1a0556b01"}, "description": "\u8fd9\u662f\u4e00\u4e2a\u5f88\u597d\u7684\u5730\u65b9"},
#     {"province": "\u5e7f\u4e1c\u7701", "city": "\u5e7f\u5dde", "name": "\u51e4\u51f0\u5c71", "image": "", "_id": {"$oid": "56de88437a74e76673e2e7b6"}, "description": "\u51e4\u51f0\u51fa\u73b0\u7684\u5730\u65b9"}
# ]
#
# list1 = [1, 2, 3]
# list2 = [1, 3, 3]
#
#
# def x(m, n):
#     if m == n:
#         return m + n
#
# print map(x, list1, list2)
# print data
# data['aa'] = 1213
# print data
# x = {
#     "name": 123,
#     "age": 456
# }
# print x
# x.pop("name")
# print x

L = ['Adam', 'Lisa', 'Bart', 'Paul']
print L[-2: 0]

str1 = '<a href="http://www.fishc.com/dvd" target="_blank">鱼C资源打包</a>'

print str1[-55: -42]
def xx():
    pass