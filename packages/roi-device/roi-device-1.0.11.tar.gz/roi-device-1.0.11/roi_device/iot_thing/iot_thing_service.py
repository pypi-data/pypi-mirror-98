import abc

class IoThingService(metaclass=abc.ABCMeta):

    """
    抽象服务：设备服务
    """

    def __init__(self):
        # 服务标配
        self.res_code = 200
        self.request_id = 0
        self.output_params = {}
        self.identifier = ""
        # 服务自定义
        self.init_service()

    @abc.abstractmethod
    def init_service(self):
        """
        服务初始化
        """
    
    @abc.abstractmethod
    def set_output_params(self):
        """
        获取输出参数
        """
        pass
    
    def get_identifier(self):
        """
        服务标识
        """
        return self.identifier

    def get_request_id(self):
        """
        服务请求 Id
        """
        return self.request_id

    def get_code(self):
        """
        服务状态码
        """
        return self.res_code

    def get_out_params(self):
        """
        获取 输出参数
        """
        return self.output_params

