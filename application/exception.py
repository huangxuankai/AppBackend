# encoding:utf8
""" By Daath """

prefURL = {
    # 以下地址根据你服务器的ip而定
    'ImageURL': 'http://192.168.2.107:8099/static/media/'     # django服务器
    # 'ImageURL': 'http://192.168.0.106:8003/static/media/'     # apache2服务器
}

"""  自定义的返回结果集  """

resultMsg = {
    'NeedParameter': {
        'error': True,
        'msgCode': 1000,
        'msg': "need parameter"
    },
    'ExistUser': {
        'error': True,
        'msgCode': 1001,
        'msg': "exist user"
    },
    'NotExistUser': {
        'error': True,
        'msgCode': 1002,
        'msg': "no exist user"
    },
    'ErrorPassword': {
        'error': True,
        'msgCode': 1003,
        'msg': "error password"
    },
    'NeedLogin': {
        'error': True,
        'msgCode': 1004,
        'msg': "need login"
    },
    'CoordinatesError': {
        'error': True,
        'msgCode': 1005,
        'msg': "coordinates error"
    },
    'AdminAuthorityApplying': {
        'error': True,
        'msgCode': 1006,
        'msg': "admin authority applying"
    },
    'ExistScene': {
        'error': True,
        'msgCode': 1007,
        'msg': "exist scene"
    },
    'NeedSceneImage': {
        'error': True,
        'msgCode': 1008,
        'msg': "need scene image"
    },
    'StatusValueError': {
        'error': True,
        'msgCode': 1009,
        'msg': "status value error"
    },
    'SignUpSuccess': {
        'error': False,
        'msgCode': 0,
        'msg': "sign up success"
    },
    'SignOut': {
        'error': False,
        'msgCode': 1,
        'msg': "sign out"
    },
    'SignCheckSuccessful': {
        'error': False,
        'msgCode': 2,
        'msg': "sign check successful"
    },
    'SaveChannelId': {
        'error': False,
        'msgCode': 3,
        'msg': "save channelId successful"
    },
    'SignInSuccess': {
        'error': False,
        'msgCode': 4,
        'msg': "sign In success"
    },
    'addSceneSuccess': {
        'error': False,
        'msgCode': 5,
        'msg': "add scene success"
    },
    'updateSceneSuccess': {
        'error': False,
        'msgCode': 6,
        'msg': "update scene success"
    },
    'onlineSceneSuccessful': {
        'error': False,
        'msgCode': 7,
        'msg': "online scene success"
    },
    'offlineSceneSuccessful': {
        'error': False,
        'msgCode': 8,
        'msg': "offline scene success"
    },
    'BecomeGuide': {
        'error': False,
        'msgCode': 9,
        'msg': "become guide"
    },
    'BecomeAdmin': {
        'error': False,
        'msgCode': 10,
        'msg': "become admin"
    },
}
