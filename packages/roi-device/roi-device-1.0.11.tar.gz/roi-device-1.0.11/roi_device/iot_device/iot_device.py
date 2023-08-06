from ..iot_thing.iot_thing import IoThing
from .iot_device_info import IoTDeviceInfo
from linkkit import linkkit
import logging


class IoTDevice():

    def __init__(self, device_info: IoTDeviceInfo, device_thing: IoThing):
        """
        初始化
        :秘钥不等0 = 设备已激活
        """
        # 设备信息
        self.device_info = device_info
        # 物模型信息
        self.device_thing = device_thing
        # 连接状态
        self.is_conn = False
        # 设备接入
        self.init_device()
        # 设备物模型
        self.device_thing.init_thing(self.lk, device_info)

    def init_device(self):
        """
        初始化设备连接
        """
        self.lk = linkkit.LinkKit(
            host_name=self.device_info.host_name,
            product_key=self.device_info.product_key,
            product_secret=self.device_info.product_secret,
            device_name=self.device_info.device_name,
            device_secret=self.device_info.device_secret
        )
        # 日志
        if self.device_info.is_debug:
            self.lk.enable_logger(logging.DEBUG)
        # 接入点
        endpoint = self.device_info.endpoint
        if len(endpoint) != 0:
            # 企业实例
            self.lk.config_mqtt(secure="", endpoint=endpoint)
        # 连接回调
        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        # 动态激活: 设备已激活，不需要进行注册
        device_secret = self.device_info.device_secret
        if len(device_secret) == 0:
            self.lk.on_device_dynamic_register = self.on_device_dynamic_register

    def is_debug(self, is_enable):
        """
        是否开启日志
        """
        if is_enable:
            self.lk.enable_logger(logging.DEBUG)

    def connect(self):
        """
        设备连接
        """
        try:
            self.logger('ali device connect...')
            print("Device: 设备连接中..")
            self.lk.connect_async()
        except Exception as e:
            print(e)
            print("Device: 设备连接异常")
            self.logger('ali device connect error ')

    def on_device_dynamic_register(self, rc, value, userdata):
        """
        动态注册
        """
        if rc == 0:
            self.logger(
                "dynamic register device success, rc:%d, value:%s" % (rc, value))
            self.device_info.device_secret = value
            # 保存设备秘钥
            self.device_info.save_device_info()
            print("Device: 设备注册成功: 设备秘钥已保存")
        else:
            self.logger(
                "dynamic register device fail,rc:%d, value:%s" % (rc, value))
            print("Device: 设备注册失败: 设备不存在 或 设备已激活！")

    def on_connect(self, flag, rc, userdata):
        """
        连接回调
        """
        self.logger("ali device on_connect:%d,rc:%d,userdata:" % (flag, rc))
        if rc == 0:
            self.is_conn = True
            print("Device: 设备连接成功")
        else:
            self.is_conn = False
            print("Device: 设备连接失败")

    def on_disconnect(self, rc, userdata):
        """
        断开回调
        """
        self.logger("ali device on_disconnect:rc:%d,userdata:" % rc)
        if rc == 0:
            self.is_conn = False
            print('Device: 设备连接断开')

    def logger(self, msg):
        """
        打印日志
        """
        logging.debug(msg)
