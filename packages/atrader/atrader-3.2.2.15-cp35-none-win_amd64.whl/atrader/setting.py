# -*- coding: utf-8 -*-


class Setting:
    # 语言
    LANGUAGE = 'chinese'

    # log 日志信息记录等级: debug<info<warn<error<critical
    LOG_LEVEL = 'info'

    # 允许系统警告在控制台输出: True/False
    ALLOW_CONSOLE_SYSTEM_WARN = True

    # 允许系统提示在控制台输出: True/False
    ALLOW_CONSOLE_SYSTEM_INFO = True

    # 允许系统调试在控制台输出: True/False
    ALLOW_CONSOLE_SYSTEM_DEBUG = False

    # 允许系统错误在控制台输出: True/False
    ALLOW_CONSOLE_SYSTEM_ERROR = True

    # 显示进入函数时的提示信息 True/False
    ALLOW_CONSOLE_ENTER_QUIT_TIPS = False

    # 是否进行参数检查
    ALLOW_ARG_CHECK = True

    # 显示精度控制(小数点个数)
    PRECISION_LEVEL = 3

    # 与Auto-Trader通讯套接字超时时间(s)
    AT_SOCKET_TIMEOUT = 3000

    # 与Auto-Trader订阅套接字超时时间(s)
    AT_SUB_SOCKET_TIMEOUT = 3000

    # 日志设置
    LOGGER_CONFIG = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s FuctionName::%(funcName)s - %(lineno)s - %(name)s :: %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "sys_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "encoding": 'utf-8',
                "formatter": "simple",
                "maxBytes": 10485760,
                "backupCount": 10
            },
            "ana_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "encoding": 'utf-8',
                "formatter": "simple",
                "maxBytes": 10485760,
                "backupCount": 10
            },
            "usr_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "encoding": 'utf-8',
                "formatter": "simple",
                "maxBytes": 10485760,
                "backupCount": 10
            },
        },
        "loggers": {
            "atrader": {
                "level": "DEBUG",
                "handlers": [
                    "sys_handler"
                ],
                "propagate": 0
            },
            "analog": {
                "level": "INFO",
                "handlers": [
                    "ana_handler"
                ],
                "propagate": 0
            },
            "userlog": {
                "level": "DEBUG",
                "handlers": [
                    "usr_handler"
                ],
                "propagate": 0
            },
        }
    }


def set_setting(option, value):
    """ 设置 setting 模块的参数
        具体参数见 setting.py 文件
    """

    from atrader.tframe.utils.logger import user_warning
    if hasattr(Setting, option):
        setattr(Setting, option, value)
    else:
        user_warning('setting.Setting module without the attribute `%s`' % option)


def get_setting(option, default=None):
    """ 获取 setting 模块的参数
        具体参数见 setting.py 文件
    """

    return getattr(Setting, option, default)


def get_version():
    """ 获取版本信息"""

    try:
        from atrader.tframe.sysdefine import self_version
    except ImportError:
        return None
    return self_version()


def get_support():
    """ 获取支持AT客户端版本"""

    try:
        from .tframe.sysdefine import support_at_version
    except ImportError:
        return None
    return support_at_version()
