class ExtraKeysResolver:

    ignored_record_keys = [
        "name",
        "msg",
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "func_name",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "pathname",
        "process",
        "process_name",
        "relative_created",
        "stack_info",
        "thread",
        "thread_name",
    ]

    @staticmethod
    def get_extra_keys(record):
        return record.__dict__.keys() - ExtraKeysResolver.ignored_record_keys
