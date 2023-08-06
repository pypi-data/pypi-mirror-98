from .iot_tools import IoTools
import json
import logging


class IoTDeviceInfo():

    """
    设备运行必要信息
    : 加密解密获得
    : 缓存配置: 开发时，config/device.json ；生产时，config/device.roi
    """

    def __init__(self, is_debug=False):
        # 工具
        self.tools = IoTools()
        # 设备存储文件
        self.config_file_name = 'device.ini'
        # 必要内容: 运行时赋值
        self.host_name = "cn-shanghai"
        self.product_key = ""
        self.product_secret = ""
        self.endpoint = ""
        # 设备信息
        self.device_name = ""
        self.device_secret = ""
        # 是否调试
        self.is_debug = is_debug
        if self.is_debug:
            logging.basicConfig(
                format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
        # 物模型文件路径
        self.thing_file_name = "thing.json"

    def init_info(self, device_name, device_key, secret_info):
        """
        初始化设备信息
        : device_name : 设备名称，标识设备与云端保持一致性
        : device_key  : 加密 key
        : secret_info : 加密 产品信息，下面的字典生成的加密信息
        {
            "product_key":"",
            "product_secret":"",
            "endpoint":""
        }
        : 要求，加密后的字符串，这里进行解密
        """
        self.device_name = device_name
        self.config_file_name = "%s.ini" % (device_name.replace(" ", ""))
        product_info = self.tools.aes_decode(device_key, secret_info)
        product = json.loads(product_info)
        # 产品 key
        keys = product.keys()
        if 'product_key' in keys:
            self.product_key = product['product_key']
        else:
            raise Exception('未知设备')
        # 产品 secret
        if 'product_secret' in keys:
            self.product_secret = product['product_secret']
        else:
            raise Exception('未知设备')
        # 产品 接入点
        if 'endpoint' in keys:
            self.endpoint = product['endpoint']
        # # 产品 区域
        # if product.has_key('host_name'):
        #     self.host_name = product['host_name']
        # 读取设备信息: device 配置相关
        self.__read_device_info()

    def save_device_info(self):
        """
        保存运行时：设备信息
        :1) 设备信息，name 和 secret
        :2) 加密设备信息
        :3) 保存成文件
        """
        device = {
            "device_name": self.device_name,
            "device_secret": self.device_secret
        }
        device_encode = self.tools.aes_encode(
            self.product_secret, json.dumps(device))
        self.tools.write_text(self.config_file_name, device_encode)

    def __read_device_info(self):
        """
        读取设备信息
        :1) 不存在，跳过
        :2) 若存在，赋值
        """
        has, device = self.tools.read_text(self.config_file_name)
        if has:
            device_decode = self.tools.aes_decode(self.product_secret, device)
            device_json = json.loads(device_decode)
            self.device_secret = device_json['device_secret']
        else:
            self.device_secret = ""
