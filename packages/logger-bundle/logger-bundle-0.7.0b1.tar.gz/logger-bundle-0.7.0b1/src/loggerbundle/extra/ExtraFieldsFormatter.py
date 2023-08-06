import colorlog
from logging import PercentStyle
from loggerbundle.extra.ExtraKeysResolver import ExtraKeysResolver


class ExtraFieldsFormatter(colorlog.ColoredFormatter):
    def __init__(self, *args, **kwargs):
        self.__orig_fmt = args[0]

        super().__init__(*args, **kwargs)

    def format(self, record):
        extra_keys = ExtraKeysResolver.get_extra_keys(record)

        if not extra_keys:
            return super().format(record)

        def map_placeholder(field_name):
            return "{}: %({})s".format(field_name, field_name)

        extra_keys_placeholders = list(map(map_placeholder, extra_keys))

        self.__set_format(self.__orig_fmt + "\n" + "{" + ", ".join(extra_keys_placeholders) + "}")
        formated = super().format(record)
        self.__set_format(self.__orig_fmt)

        return formated

    def __set_format(self, fmt: str):
        self._fmt = fmt
        self._style = PercentStyle(self._fmt)
