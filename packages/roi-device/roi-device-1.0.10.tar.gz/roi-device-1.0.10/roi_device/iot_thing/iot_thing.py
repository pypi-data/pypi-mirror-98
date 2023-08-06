from .iot_thing_service import IoThingService
from .iot_thing_properties import IoThingProperties
from .iot_thing_event import IoTingEvent
from ..iot_topic.iot_topic_thing import IoTopicThing
from ..iot_topic.iot_topic import IoTopic
from ..iot_device.iot_device_info import IoTDeviceInfo
from .iot_thing_shadow import IoThingShadow
from linkkit.linkkit import LinkKit
import logging
import abc


class IoThing(metaclass=abc.ABCMeta):

    """
    抽象物模型，所有设备都集成此函数
    物模型开发: 属性，服务，事件，通用设备联网
    """

    def init_thing(self, lk: LinkKit, device_info: IoTDeviceInfo):
        """
        初始化 物模型
        """
        # 初始化
        self.device_info = device_info
        self.lk = lk
        self.iot_topic = IoTopic(
            self.device_info.product_key, self.device_info.device_name)
        # 物模型
        self.lk.thing_setup(self.device_info.thing_file_name)
        self.lk.on_thing_enable = self.__on_thing_enable
        self.lk.on_thing_disable = self.__on_thing_disable
        # 属性回调
        self.lk.on_thing_prop_post = self.__on_thing_prop_post
        # 属性云端下发回调
        self.lk.on_thing_prop_changed = self.__on_thing_prop_changed
        # 事件回调
        self.lk.on_thing_event_post = self.__on_thing_event_post
        # 服务回调
        self.lk.on_thing_call_service = self.__on_thing_call_service
        # Topic 发送回调
        self.lk.on_publish_topic = self.__on_publish_topic
        # 设备影子
        self.lk.on_thing_shadow_get = self.__on_thing_shadow_get
        # 初始化设备
        self.init_device_thing()

    def __enable_subscribe_topic(self):
        """
        订阅云端消息
        : 连接成功后，开启订阅
        : 订阅与取消订阅，成对出现
        """
        self.get_thing_topics(self.iot_topic)
        for topic in self.iot_topic.thing_sub_topics:
            self.lk.subscribe_topic(topic)
        # 消息接收
        self.lk.on_topic_message = self.__on_topic_message

    def __disable_subscribe_topic(self):
        """
        取消订阅云端消息
        """
        for topic in self.iot_topic.thing_sub_topics:
            self.lk.unsubscribe_topic(topic)

    def __on_thing_enable(self, userdata):
        """
        物模型：开启回调
        :属性、服务、事件，设备监控开始
        """
        self.logger('on thing enable')
        print("Device: 设备运行中")
        # 开启订阅
        self.__enable_subscribe_topic()
        # 开启采集
        self.thing_start()

    def __on_thing_disable(self, userdata):
        """
        物模型：关闭回调
        :属性、服务、事件，设备监控关闭
        """
        self.logger('on_thing_disable')
        # 订阅取消
        self.__disable_subscribe_topic()
        # 停止采集
        self.thing_stop()

    def post_properties(self, props: IoThingProperties):
        """
        属性上传
        ----
        基本原理：建立上传通讯记录，若 rc=0，做记录，待 code=200 则成功；
        """
        self.logger(props.get_properties())
        rc, request_id = self.lk.thing_post_property(props.get_properties())
        self.logger('>> request_id: %s' % (str(request_id)))
        return rc == 0

    def __on_thing_prop_post(self, request_id, code, data, msg, userdata):
        """
        属性上传回调
        """
        # TODO 根据 request_id ，查询上传记录并进行更新
        # 若 code=200 ，则云端接收成功，否则云端解析识别
        self.logger('<< request_id: %s, code: %d' %
                    (str(request_id), code))
        self.thing_post_props_callback(code, request_id)

    def __on_thing_prop_changed(self, params, userdata):
        """
        属性下发回调：云端下放设置属性
        """
        self.logger('params -> '+str(params))
        self.thing_call_props_callback(params)

    def post_event(self, event: IoTingEvent):
        """
        事件上传
        """
        rc, request_id = self.lk.thing_trigger_event(
            (event.get_event_name(), event.get_event_data()))
        # 回调
        # event.on_post_callback(request_id)
        self.logger('>> event request_id: %s' % (str(request_id)))
        return rc == 0

    def __on_thing_event_post(self, event, request_id, code, data, message, userdata):
        """
        事件上传回调
        """
        self.logger('<< event %s request_id: %s, code: %d' %
                    (event, str(request_id), code))
        self.thing_post_event_callback(event, code, request_id)

    def __on_thing_call_service(self, identifier, request_id, params, userdata):
        """
        服务下放回调：云端调用服务
        """
        self.logger("identifier -> "+identifier)
        # 服务下发创建具体实现的服务
        self.thing_call_service_callback(identifier, params, request_id)

    def post_service_answer(self, service: IoThingService):
        """
        服务上传信息：服务异步应答
        """
        rc, request_id = self.lk.thing_answer_service(
            service.get_identifier(),
            service.get_request_id(),
            service.get_code(),
            service.get_out_params()
        )
        self.logger('>> service request_id: %s' % (str(request_id)))
        return rc == 0

    def post_topic_message(self, topic: IoTopicThing):
        """
        Topic 上传信息：发送数据到云端
        """
        rc, mid = self.lk.publish_topic(
            topic.get_post_topic(), topic.get_post_payload_data())
        self.logger('>> topic mid: %s' % (str(mid)))
        return rc == 0

    def __on_publish_topic(self, mid, userdata):
        """
        Topic 上传信息：回调
        """
        self.logger('<< topic mid: %s' % (str(mid)))
        self.thing_post_topic_callback(mid)

    def __on_topic_message(self, topic, payload, qos, userdata):
        """
        Topic 订阅信息：云端下传信息
        """
        self.logger("on_topic_message:" + topic + " payload:" +
                    str(payload) + " qos:" + str(qos))
        self.thing_call_topic_callback(topic, payload)

    def __on_thing_shadow_get(self, payload, userdata):
        """
        设备影子 接收信息
        """
        self.logger("on_thing_shadown_get:"+str(payload))
        self.thing_call_shadow(payload)

    def post_update_thing_shadow(self, shadow: IoThingShadow):
        """
        设备影子 主动更新影子(上报云端)
        """
        res = self.lk.thing_update_shadow(
            shadow.get_reported(), shadow.get_version())
        return res == 0

    def post_get_thing_shadow(self):
        """
        设备影子 主动查询影子(同步云端到本地)
        """
        res = self.lk.thing_get_shadow()
        return res == 0

    def logger(self, msg):
        """
        日志
        """
        logging.debug(msg)

    @abc.abstractmethod
    def init_device_thing(self):
        """
        重写实现：初始化设备物模型
        """
        print("and")
        pass

    @abc.abstractmethod
    def thing_start(self):
        """
        重写实现：开启物模型
        """
        pass

    @abc.abstractmethod
    def thing_stop(self):
        """
        重写实现：关闭物模型
        """
        pass

    @abc.abstractmethod
    def get_thing_topics(self, iotopic: IoTopic):
        """
        重写实现：定义信息，执行 add_thing_topic
        """
        pass

    def thing_post_props_callback(self, code, request_id):
        """
        重写实现：上传物模型属性/回调
        """
        pass

    def thing_call_props_callback(self, params):
        """
        重写实现：云端下放设置属性值
        """
        pass

    def thing_post_event_callback(self, event, code, request_id):
        """
        重写实现: 上传物模型事件/回调
        """
        pass

    def thing_call_service_callback(self, identifier, input_params, request_id):
        """
        重写实现：云端下发调用服务/异步
        """
        pass

    def thing_call_topic_callback(self, topic, payload):
        """
        重写实现：云端下发 Topic 信息
        """
        pass

    def thing_post_topic_callback(self, mid):
        """
        重写实现：发送信息回调
        """
        pass

    def thing_call_shadow(self, payload):
        """
        重写实现：接收影子信息
        """
