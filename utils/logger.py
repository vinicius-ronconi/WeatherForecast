from logging import Logger, FileHandler

from django.conf import settings

STRING_FORMAT = u'[{record.time:%Y-%m-%d %H:%M:%S}]{record.level_name}: {record.message}'


def init_logger(file_name):
    """
    :type file_name: str
    :rtype: logging.Logger
    """
    if not file_name.lower().endswith('.log'):
        file_name += '.log'

    handler = FileHandler(file_name)
    handler.setFormatter(STRING_FORMAT)

    log_path = '{}/{}'.format(settings.BASE_LOG_DIR, file_name)
    instance = Logger(log_path)
    instance.handlers.append(handler)
    return instance
