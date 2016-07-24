from django.test import TestCase
import json
# Create your tests here.

from mongoengine import queryset

# ll = [
#     {
#         "name": 123,
#         "age": 654},
#     {
#         "name": 789,
#         "age": 55
#     }
# ]
# l1 = json.dumps(ll)
#
# l2 = json.loads(l1)
# print ll[0]
# print l1
# print l2[0]


class A (object):

    def xx(self):
        return 'aa'

a = A()
print a.xx()

