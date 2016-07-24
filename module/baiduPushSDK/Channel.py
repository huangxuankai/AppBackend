#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import time

import urllib

import hashlib

import json

import ConfigParser

import os,sys

import platform

from lib.ChannelException import ChannelException

from lib.RequestCore import RequestCore,ResponseCore

from lib.valid import validOptDict,validParam,nullOk

class Channel(object):

    #baidu push 域名
    HOST = 'host'

    #应用key，从百度开发者中心获得,是创建Channel的必须参数
    API_KEY = 'apikey'

    #从百度开发者中心获得，是创建Channel的必须参数
    SECRET_KEY = 'secret_key'

    #设备类型，3:android, 4:ios
    DEVICE_TYPE = 'device_type'

    #Channel常量，用于计算sign，用户不必关注
    SIGN = 'sign'
    METHOD = 'method'
    REQUEST_ID = None

    #curl 连接参数
    CURL_TIMEOUT = 30
    CURL_CONNECTTIMEOUT = 5

    #Channel 错误常量
    CHANNEL_SDK_INIT_ERROR = 1
    CHANNEL_SDK_RUNNING_ERROR = 2
    CHANNEL_SDK_PARAM = 3
    CHANNEL_SDK_HTTP_STATUS_OK_BUT_RESULT_ERROR = 4
    CHANNEL_SDK_HTTP_STATUS_ERROR_AND_RESULT_ERROR = 5

    #操作系统版本信息，用于User-Agent设置
    SYSTEM_INFO = 'system_info'

    #配置文件加载情况
    CONF_ERR = False;

    def __init__(self):
        """init 获得运行linux平台版本信息, 加载conf"""

        Channel.SYSTEM_INFO = str(platform.uname())
        self._loadConf()

    def _loadConf(self):
        """加载配置文件

        加载失败会在调用api时抛出异常ChannelException，errCode=1
        配置文件分为两个section：
        1、SDK，包括推送域名host、apiKey、secretKey
        2、curl，包括建立连接超时和交互超时"""

        try:
            ABSPATH=os.path.abspath(__file__)
            pos = ABSPATH.rfind('/')
            ABSPATH = ABSPATH[:pos + 1]
            cp = ConfigParser.SafeConfigParser()
            cp.read(ABSPATH + 'sdk.conf')
            Channel.API_KEY= cp.get('SDK', 'apiKey')
            Channel.SECRET_KEY = cp.get('SDK', 'secretKey')
            Channel.DEVICE_TYPE = cp.get('SDK', 'deviceType')
            Channel.HOST = cp.get('SDK', 'host')
            Channel.CURL_TIMEOUT = cp.getint('curl', 'timeout')
            Channel.CURL_CONNECTTIMEOUT= cp.getint('curl', 'connecttimeout')
            self._curlOpts = dict(TIMEOUT = Channel.CURL_TIMEOUT,
                                  CONNECTTIMEOUT = Channel.CURL_CONNECTTIMEOUT)
        except Exception as e:
            Channel.CONF_ERR = True

    def setApiKey(self, apiKey):
        """运行期间可以另指定apiKey

        args：
            apiKey--想要指定的apiKey"""

        Channel.API_KEY = apiKey

    def setSecretKey(self, secretKey):
        """运行期间可以另指定secretKey

        args：
            secretKey--想要指定的secretKey"""

        Channel.SECRET_KEY = secretKey

    def setDeviceType(self, deviceType):
        """运行期间可以修改设备类型

        args:
            deviceType--想要指定的deviceType"""

        Channel.DEVICE_TYPE = deviceType

    def getRequestId(self):
        """获得服务器返回的requestId

        return:
            requestId"""

        return Channel.REQUEST_ID
    
    @validParam(channel_id=str, msg=str, opts=nullOk(dict))
    def pushMsgToSingleDevice(self, channel_id, msg, opts=None):
        """向单个设备推送消息

        args:
            channel_id--客户端初始化成功之后返回的channelId
            msg--json格式的通知数据，详见说明文档
            opts--可选字段合集，详见说明文档
        return：
            msg_id--消息id
            send_time--消息的实际推送时间
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'pushMsgToSingleDevice')
        args = self._commonSet()
        args['channel_id'] = channel_id
        args['msg'] = msg
        args.update(opts)
        self._product_name = 'push'
        self._resource_name = 'single_device'

        return self._commonProcess(args)


    @validParam(msg=str, opts=nullOk(dict))
    def pushMsgToAll(self, msg, opts=None):
        """向当前app下所有设备推送一条消息

        args:
            msg--json格式的通知数据，详见说明文档
            opts--可选字段合集，详见说明文档
        return：
            msg_id--消息id
            send_time--消息的实际推送时间
            timer_id(可选)--定时服务ID
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'pushMsgToAll')
        args = self._commonSet()
        args['msg'] = msg
        args.update(opts)
        self._product_name = 'push'
        self._resource_name = 'all'

        return self._commonProcess(args)


    @validParam(type=(int, '0<x<2'), tag=str, msg=str, opts=nullOk(dict))
    def pushMsgToTag(self, tag, msg, type=1, opts=None):
        """推送消息或通知给指定的标签

        args:
            tag--已创建的tag名称
            msg--json格式的通知数据，详见说明文档
            type--推送的标签类型,目前固定值为1
            opts--可选字段合集，详见说明文档
        return：
            msg_id--消息id
            send_time--消息的实际推送时间
            timer_id(可选)--定时服务ID
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'pushMsgToTag')
        args = self._commonSet()
        args['type'] = type
        args['tag'] = tag
        args['msg'] = msg
        args.update(opts)
        self._product_name = 'push'
        self._resource_name = 'tags'
        
        return self._commonProcess(args)


    @validParam(channel_ids=list, msg=str, opts=nullOk(dict))
    def pushBatchUniMsg(self, channel_ids, msg, opts=None):
        """推送消息给批量设备（批量单播）

        args:
            channel_ids--一组channel_id（最多为一万个）组成的json数组字符串
            channel_ids--一组channel_id（最少1个，最多为10个）组成的list，对应一批设备
            msg--json格式的通知数据，详见说明文档
            opts--可选字段合集，详见说明文档
        return：
            msg_id--消息id
            send_time--消息的实际推送时间
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'pushBatchUniMsg')
        args = self._commonSet()
        args['channel_ids'] = json.dumps(channel_ids)
        args['msg'] = msg
        #args['topic_id'] = topic_id
        args.update(opts)
        self._product_name = 'push'
        self._resource_name = 'batch_device'
        
        return self._commonProcess(args)


    @validParam(msg_id=str)
    def queryMsgStatus(self, msg_id):
        """根据msg_id获取消息推送报告

        args:
            msg_id--推送接口返回的msg_id，支持一个由msg_id组成的json数组
        return：
            total_num--结果数量
            result--数组对象，每项内容为一条消息的状态
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档
            
        目前不支持单播msg id查询"""

        self._checkConf()

        args = self._commonSet()
        args['msg_id'] = msg_id
        self._product_name = 'report'
        self._resource_name = 'query_msg_status'
        
        return self._commonProcess(args)


    @validParam(timer_id=str, opts=nullOk(dict))
    def queryTimerRecords(self, timer_id, opts=None):
        """根据timer_id获取消息推送记录

        args:
            timer_id--推送接口返回的timer_id
            opts--可选字段合集，详见说明文档
        return：
            timer_id--定时任务id
            result--数组对象，每项内容为该定时任务所产生的一条消息的状态
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'queryTimerRecords')
        args = self._commonSet()
        args['timer_id'] = timer_id
        args.update(opts)
        self._product_name = 'report'
        self._resource_name = 'query_timer_records'
        
        return self._commonProcess(args)


    @validParam(topic_id=(str, '0<len(x)<129'), opts=nullOk(dict))
    def queryTopicRecords(self, topic_id, opts=None):
        """根据分类主题获取消息推送记录

        args:
            topic_id--分类主题名称
            opts--可选字段合集，详见说明文档
        return：
            topic_id--分类主题名称
            result--数组对象，每项内容为该分类主题下的一条消息的相关信息
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'queryTopicRecords')
        args = self._commonSet()
        args['topic_id'] = topic_id
        args.update(opts)
        self._product_name = 'report'
        self._resource_name = 'query_topic_records'
        
        return self._commonProcess(args)


    @validParam(opts=nullOk(dict))
    def queryTimerList(self, opts=None):
        """查看还未执行的定时任务，每个应用可设置的有效的定时任务有限制(目前为10个)

        args:
            opts--可选字段合集，详见说明文档
        return：
            total_num--定时推送任务的总数量
            result--数组对象，每项表示一个定时任务的相关信息
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'queryTimerList')
        args = self._commonSet()
        args.update(opts)
        self._product_name = 'timer'
        self._resource_name = 'query_list'
        
        return self._commonProcess(args)


    @validParam(opts=nullOk(dict))
    def queryTopicList(self, opts=None):
        """查询推送过程中使用过的分类主题列表

        args:
            opts--可选字段合集，详见说明文档
        return：
            total_num--所使用过的分类主题总数
            result--json数组，数组中每项内容表示一个分类主题的相关信息
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'queryTopicList')
        args = self._commonSet()
        args.update(opts)
        self._product_name = 'topic'
        self._resource_name = 'query_list'
        
        return self._commonProcess(args)


    @validParam(opts=nullOk(dict))
    def queryTags(self, opts=None):
        """查询应用的tag

        args:
            opts--可选字段合集，详见说明文档
        return：
            total_num--Tag总数
            result--数组对象，每项内容表示一个Tag的详细信息
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        validOptDict(opts, 'queryTags')
        args = self._commonSet()
        args.update(opts)
        self._product_name = 'app'
        self._resource_name = 'query_tags'
        
        return self._commonProcess(args)


    @validParam(tag=(str, '0<len(x)<129'))
    def createTag(self, tag):
        """创建一个空的标签组

        args:
            tag--标签名称
        return：
            tag--标签名称
            result--状态 0：创建成功； 1：创建失败；
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['tag'] = tag
        self._product_name = 'app'
        self._resource_name = 'create_tag'
        
        return self._commonProcess(args)


    @validParam(tag=(str, '0<len(x)<129'))
    def deleteTag(self, tag):
        """删除一个已存在的tag

        args:
            tag--标签名称
        return：
            tag--标签名称
            result--状态 0：删除成功； 1：删除失败；
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['tag'] = tag
        self._product_name = 'app'
        self._resource_name = 'del_tag'
        
        return self._commonProcess(args)


    @validParam(tag=(str, '0<len(x)<129'), channel_ids=list)
    def addDevicesToTag(self, tag, channel_ids):
        """向tag中批量添加设备

        args:
            tag--标签名称
            channel_ids--一组channel_id（最少1个，最多为10个）组成的list，对应一批设备
        return：
            devices--数组对象，每个元素表示对应的一个channel_id是否添加成功
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['tag'] = tag
        args['channel_ids'] = json.dumps(channel_ids)
        self._product_name = 'tag'
        self._resource_name = 'add_devices'
        
        return self._commonProcess(args)


    @validParam(tag=(str, '0<len(x)<129'), channel_ids=list)
    def deleteDevicesFromTag(self, tag, channel_ids):
        """从tag中批量解绑设备

        args:
            tag--标签名称
            channel_ids--一组channel_id（最少1个，最多为10个）组成的list，对应一批设备
        return：
            devices--数组对象，每个元素表示对应的一个channel_id是否删除成功
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['tag'] = tag
        args['channel_ids'] = json.dumps(channel_ids)
        self._product_name = 'tag'
        self._resource_name = 'del_devices'
        
        return self._commonProcess(args)


    @validParam(tag=(str, '0<len(x)<129'))
    def queryDeviceNumInTag(self, tag):
        """查询某个tag关联的设备数量

        args:
            tag--标签名称
        return：
            device_num--标签中设备的数量
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['tag'] = tag
        self._product_name = 'tag'
        self._resource_name = 'device_num'
        
        return self._commonProcess(args)


    @validParam(topic_id=(str, '0<len(x)<129'))
    def queryStatisticTopic(self, topic_id):
        """统计当前应用下一个分类主题的消息数量

        args:
            topic_id--一个已使用过的分类主题
        return：
            total_num--所发的分类主题总数
            result--dic对象，key为统计信息当天的0点0分的时间戳，value包含(ack：当天消息到达数)
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        args['topic_id'] = topic_id
        self._product_name = 'report'
        self._resource_name = 'statistic_topic'
        
        return self._commonProcess(args)


    def queryStatisticDevice(self):
        """统计APP 设备数

        return：
            total_num--统计结果集的条数
            result--dic对象，详见说明文档
        Exception：
            参数错误或者http错误，会抛出此异常，异常信息详见说明文档"""

        self._checkConf()

        args = self._commonSet()
        self._product_name = 'report'
        self._resource_name = 'statistic_device'
        
        return self._commonProcess(args)


    def _commonSet(self):
        """公共参数设置"""

        args = dict()
        args['apikey'] = Channel.API_KEY
        args['secretKey'] = Channel.SECRET_KEY
        args['device_type'] = Channel.DEVICE_TYPE
        args['timestamp'] = int(time.time())
        
        return args
    

    def _genSign(self, method, url, arrContent):
        """签名计算"""

        gather = method + url
        keys = arrContent.keys()
        keys.sort()
        for key in keys:
            gather += key + '=' + str(arrContent[key])
        gather += Channel.SECRET_KEY
        sign = hashlib.md5(urllib.quote_plus(gather))  
        
        return sign.hexdigest()


    def _baseControl(self, opt):
        """http交互"""

        host = Channel.HOST
        url = 'http://' + host + '/rest/3.0/' + self._product_name + '/' + self._resource_name
        http_method = 'POST'
        opt[Channel.SIGN] = self._genSign(http_method, url, opt)
        request = RequestCore(url)
        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        headers['User-Agent'] = 'BCCS_SDK/3.0' +\
                                Channel.SYSTEM_INFO +\
                                'python/2.7.3 (Baidu Push Server SDK V3.0.0) cli/Unknown'
        for (headerKey , headerValue) in headers.items():
            headerValue = headerValue.replace('\r', '')
            headerValue = headerValue.replace('\n', '')
            if (headerValue is not None):
                request.add_header(headerKey, headerValue)
        
        request.set_method(http_method)
        request.set_body(urllib.urlencode(opt))
        
        if(isinstance(self._curlOpts, dict)):
            request.set_curlopts(self._curlOpts)

        request.handle_request()
        
        return ResponseCore(request.get_response_header(),
                            request.get_response_body(),
                            request.get_response_code())

    def _commonProcess(self, paramOpt):
        """返回结果处理"""

        ret = self._baseControl(paramOpt)
        if( ret is None):
            raise ChannelException('base control returned None object',\
                    Channel.CHANNEL_SDK_RUNNING_ERROR)
        if(ret.isOK()):
            result = json.loads(ret.body.encode("utf-8"))
            if (result is None):
                raise ChannelException(ret.body, 
                    Channel.CHANNEL_SDK_HTTP_STATUS_OK_BUT_RESULT_ERROR)
            Channel.REQUEST_ID= result['request_id']
            if (not 'response_params' in result):
                return None
            else:
                return self._byteify(result['response_params'])
        result = json.loads(ret.body)
        if(result is None):
            raise ChannelException('ret body:' + ret.body,
                Channel.CHANNEL_SDK_HTTP_STATUS_ERROR_AND_RESULT_ERROR)
        Channel.REQUEST_ID= result['request_id']
        raise ChannelException(result['error_msg'], result['error_code'])
    

    def _checkConf(self):
        Channel.REQUEST_ID = None
        if (Channel.CONF_ERR):
            raise ChannelException(
                    'Channel init error', 
                    Channel.CHANNEL_SDK_INIT_ERROR) 

    def _byteify(self, input):
        if isinstance(input, dict):
            return {self._byteify(key): self._byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self._byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
