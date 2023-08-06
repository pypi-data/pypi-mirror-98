import abc


class IoTopicThing(metaclass=abc.ABCMeta):

    """
    抽象Topic: topic 消息 , 消息体发送
    根据topic操作事宜，均需要继承该类
    """

    def __init__(self):
        # 产品 key
        self.product_key = ""
        # 设备 名
        self.device_name = ""

    def init_topic(self, product_key, device_name):
        """
        初始化，设备信息
        """
        self.product_key = product_key
        self.device_name = device_name

    @abc.abstractmethod
    def get_post_topic(self):
        """
        获取 request topic
        """
        pass

    @abc.abstractmethod
    def get_post_payload_data(self):
        """
        获取 request payload data
        """
        pass

    @abc.abstractmethod
    def get_subscribe_topic(self):
        """
        获取 reponse topic
        """
        pass
