import json
import base64
from Crypto.Cipher import AES


class IoTools():

    """
    配置文件读取工具
    """

    def __init__(self):
        # 设备信息配置文件
        self.config_path = 'static/config/'

    def read_json(self, file_name):
        """
        读取 json 文件
        :file_name , 文件名称
        :False,{} , 状态，数据
        """
        try:
            config = self.config_path + file_name
            with open(config, 'r') as file:
                return True, json.load(file)
        except Exception as e:
            print(e)
            return False, {}

    def write_json(self, file_name, content):
        """
        写入 json 文件
        """
        try:
            config = self.config_path + file_name
            with open(config, 'w') as file:
                file.write(json.dumps(content, indent=4))
            return True
        except Exception as e:
            print(e)
            return False

    def read_text(self, file_name):
        """
        读取 文本 文件
        """
        try:
            config = self.config_path + file_name
            with open(config, 'r') as file:
                return True, str(file.read())
        except Exception as e:
            print(e)
            return False, ""

    def write_text(self, file_name, content):
        """
        写入文本文件
        """
        try:
            config = self.config_path + file_name
            with open(config, 'w') as file:
                file.write(str(content))
            return True
        except Exception as e:
            print(e)
            return False

    def string_add_16(self, value):
        """
        字符串不足 16 ，补足 16
        """
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    def aes_encode(self, key, text):
        """
        加密字符串
        :key 秘钥
        :text 要加密的内容
        """
        aes = AES.new(self.string_add_16(key), AES.MODE_ECB)
        encode = aes.encrypt(self.string_add_16(text))
        encode_string = str(base64.encodebytes(encode), encoding='utf-8')
        return encode_string

    def aes_decode(self, key, text):
        """
        解密字符串
        :key 秘钥
        :text 要解密的内容
        """
        aes = AES.new(self.string_add_16(key), AES.MODE_ECB)
        decode_base64 = base64.decodebytes(text.encode(encoding='utf-8'))
        decode_string = str(aes.decrypt(decode_base64),
                            encoding='utf-8').replace('\0', '')
        return decode_string
