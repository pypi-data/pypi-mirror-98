from logging import getLogger
from typing import List
from loggerbundle.handler.HandlerFactoryInterface import HandlerFactoryInterface


class LoggerFactory:
    def __init__(
        self,
        default_log_level: int,
        handler_factories: List[HandlerFactoryInterface],
    ):
        self.__default_log_level = default_log_level
        self.__handler_factories = handler_factories

    def create(self, logger_name: str, log_level: int = None):
        logger = getLogger(logger_name)
        logger.setLevel(log_level if log_level is not None else self.__default_log_level)

        logger.handlers = list(map(lambda handler_factory: handler_factory.create(), self.__handler_factories))
        logger.propagate = False

        return logger
