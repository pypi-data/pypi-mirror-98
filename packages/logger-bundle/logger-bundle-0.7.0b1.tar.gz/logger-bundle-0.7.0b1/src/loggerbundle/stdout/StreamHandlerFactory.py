from logging import StreamHandler
from loggerbundle.extra.ExtraFieldsFormatter import ExtraFieldsFormatter
from loggerbundle.handler.HandlerFactoryInterface import HandlerFactoryInterface


class StreamHandlerFactory(HandlerFactoryInterface):
    def __init__(
        self,
        format_str: str,
        date_format: str,
    ):
        self.__format_str = format_str
        self.__date_format = date_format

    def create(self):
        cformat = "%(log_color)s" + self.__format_str
        formatter = ExtraFieldsFormatter(cformat, self.__date_format)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)

        return stream_handler
