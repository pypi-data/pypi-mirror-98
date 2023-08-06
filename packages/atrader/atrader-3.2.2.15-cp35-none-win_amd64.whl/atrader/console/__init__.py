# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:52:56 2018

@author: kunlin.l
"""

import atrader.enums as enums
from atrader.setting import get_setting, get_support, set_setting, get_version
from atrader.api.history import *
from atrader.api.bpfactor import *
from atrader.api import fundamental as fundamental_api
from atrader.api import riskmodel as riskmodel_api
# noinspection PyUnresolvedReferences
from atrader.api.fundamental import *
# noinspection PyUnresolvedReferences
from atrader.api.riskmodel import *

__all__ = [
    'get_kdata_n',
    'get_kdata',
    'get_tick_data',
    'get_code_list',
    'get_main_contract',
    'get_future_info',
    'get_future_contracts',
    'get_stock_info',
    'get_trading_days',
    'get_trading_time',
    'get_factor_by_factor',
    'get_factor_by_day',
    'get_factor_by_code',
    'get_setting',
    'get_support',
    'set_setting',
    'get_version',
    'enums',
    *fundamental_api.__all__,
    *riskmodel_api.__all__,
]
