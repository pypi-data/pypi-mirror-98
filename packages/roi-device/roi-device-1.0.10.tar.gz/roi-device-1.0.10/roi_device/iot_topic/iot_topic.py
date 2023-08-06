import abc
from .iot_topic_thing import IoTopicThing


class IoTopic():

    """
    Topic 统一管理
    """

    def __init__(self, product_key, device_name):
        # 基本配置
        self.product_key = product_key
        self.device_name = device_name
        # 自定义 topic
        self.thing_sub_topics = []

    def add_thing_topic(self, topic_thing: IoTopicThing):
        # 初始化 topic
        topic_thing.init_topic(self.product_key, self.device_name)
        # 订阅 topic 数组
        self.thing_sub_topics.append(topic_thing.get_subscribe_topic())
