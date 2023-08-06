# -*- coding: utf-8 -*-
"""
变更日志
-----------
2018-11-12 增加更加详细的基本面数据 api, 见 atrader.fundamental 模块
"""

import pandas as pd
import numpy as np

import atrader.enums as enums
from atrader.calcfactor import *
from atrader.backtest import *
from atrader.realtrade import *
from atrader.api.bpfactor import *
from atrader.api.history import *
from atrader.api.orders import *
from atrader.api.regfuncs import *
from atrader.tframe.snapshot import *
from atrader.setting import set_setting, get_setting, get_version, get_support
from atrader.tframe import clear_cache
from atrader.tframe.snapshot import ContextBackReal as Context
from atrader.api import bpfactor as factors_api, history as history_api, orders as orders_api, regfuncs as reg_api
from atrader.api import fundamental as fundamental_api
# noinspection PyUnresolvedReferences
from atrader.api.fundamental import *
from atrader.api import riskmodel as riskmodel_api
# noinspection PyUnresolvedReferences
from atrader.api.riskmodel import *

__all__ = [
    'np',
    'pd',
    'set_setting',
    'get_setting',
    'get_version',
    'get_support',
    'clear_cache',
    'set_backtest',
    'run_factor',
    'run_backtest',
    'run_realtrade',
    *factors_api.__all__,
    *history_api.__all__,
    *orders_api.__all__,
    *reg_api.__all__,
    *fundamental_api.__all__,
    *riskmodel_api.__all__,
    'Context',
    'ContextFactor',
    'AccountSnapshot',
    'ExecutionSnapshot',
    'OrderSnapshot',
    'enums',
]

__version__ = get_version()
__author__ = 'www.bitpower.com.cn'
__mail__ = 'Contact@bitpower.com.con'
__telephone__ = '0755-86503293'
__address__ = '深圳市南山区粤海街道深圳湾科技生态园6栋413室'

# 不允许换行
pd.set_option('display.expand_frame_repr', False)
# 最大行数 500
pd.set_option('display.max_rows', 500)
# 最大允许列数 35
pd.set_option('display.max_columns', 35)
# 小数显示精度
pd.set_option('precision', 5)
# 绝对值小于0,001统一显示为0.0
pd.set_option('chop_threshold', 0.001)
# 对齐方式
pd.set_option('colheader_justify', 'right')

np.seterr(all='ignore')
