import abc


class IoThingProperties(metaclass=abc.ABCMeta):

    """
    抽象属性：设备
    """

    @abc.abstractmethod
    def get_properties(self):
        """
        获取属性值
        """
        return {}

