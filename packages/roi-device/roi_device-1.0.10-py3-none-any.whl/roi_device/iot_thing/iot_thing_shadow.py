import abc


class IoThingShadow(metaclass=abc.ABCMeta):

    """
    设备影子：重写实现（影子数据）
    """

    @abc.abstractmethod
    def get_reported(self):
        """
        上报的影子数据
        """
        return {}

    @abc.abstractmethod
    def get_version(self):
        """
        影子版本号
        """
        return 1
