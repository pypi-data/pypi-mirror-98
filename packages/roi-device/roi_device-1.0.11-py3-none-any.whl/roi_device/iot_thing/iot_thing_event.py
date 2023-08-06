import abc

class IoTingEvent(metaclass=abc.ABCMeta):

    """
    抽象事件
    """

    @abc.abstractmethod
    def get_event_name(self):
        """
        事件名称
        """
        return ""


    @abc.abstractmethod
    def get_event_data(self):
        """
        获取事件值
        """
        return {}
