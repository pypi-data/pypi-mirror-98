# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:34:37 2018

@author: kunlin.l
"""

# noinspection PyUnresolvedReferences
from collections import Iterable
# noinspection PyUnresolvedReferences
import atrader.enums as enums
# noinspection PyUnresolvedReferences
from atrader.tframe import sysclsbase as cnt
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import smm
# noinspection PyUnresolvedReferences
from atrader.tframe.sysclsbase import gv
# noinspection PyUnresolvedReferences
from atrader.tframe.utils.argchecker import apply_rule, verify_that, convert_targets
from atrader.tframe.utils.utilcls import OrderedDotDict
from atrader.tframe.udefs import ONE_YEAR_AGO, ZERO_YEAR_AGO
from atrader.tframe.ufuncs import convert_str_or_datetime_to_int_date

__all__ = [
    'set_backtest',
    'run_backtest',
]


@smm.force_mode(gv.RUNMODE_CONSOLE)
@smm.force_phase(gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('strategy_name').is_instance_of(str),
            verify_that('target_list').is_instance_of(Iterable),
            verify_that('frequency').is_valid_frequency(),
            verify_that('fre_num').is_instance_of(int).is_greater_than(0),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date(allow_empty_str=True),
            verify_that('fq').is_in((enums.FQ_BACKWARD,
                                     enums.FQ_FORWARD,
                                     enums.FQ_NA)))
def run_backtest(strategy_name='',
                 file_path='.',
                 target_list=(),
                 frequency='day',
                 fre_num=1,
                 begin_date=ONE_YEAR_AGO,
                 end_date=ZERO_YEAR_AGO,
                 fq=enums.FQ_NA):
    if isinstance(begin_date, str) and begin_date.strip() == '':
        begin_date = ONE_YEAR_AGO

    if isinstance(end_date, str) and end_date.strip() == '':
        end_date = ZERO_YEAR_AGO
    config, strategyInfo = OrderedDotDict(), OrderedDotDict()
    strategyInfo.fq = fq
    strategyInfo.frequency = frequency
    strategyInfo.freq_num = fre_num
    strategyInfo.begin_date = convert_str_or_datetime_to_int_date(begin_date)
    strategyInfo.end_date = convert_str_or_datetime_to_int_date(end_date)
    strategyInfo.strategy_name = strategy_name
    strategyInfo.targets = list(convert_targets(target_list))
    strategyInfo.strategy_path = file_path
    config.entry = strategyInfo
    config.entry_point = 'run_backtest'

    from .main import main_run_back_test
    return str(main_run_back_test(dict(config)))


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT)
@smm.force_mode(gv.RUNMODE_BEFORE_BACKTEST, gv.RUNMODE_BEFORE_REALTRADE)
@apply_rule(verify_that('initial_cash').is_greater_than(0.0),
            verify_that('future_cost_fee').is_greater_or_equal_than(0.0),
            verify_that('stock_cost_fee').is_greater_or_equal_than(0.0),
            verify_that('rate').is_greater_than(0.0),
            verify_that('margin_rate').is_greater_or_equal_than(0.0),
            verify_that('slide_price').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('price_loc').is_instance_of(int).is_greater_or_equal_than(0),
            verify_that('deal_type').is_in((enums.MARKETORDER_DIRECT,
                                            enums.MARKETORDER_NONME_BEST_PRICE,
                                            enums.MARKETORDER_ME_BEST_PRICE)),
            verify_that('limit_type').is_in((enums.LIMITORDER_DIRECT,
                                             enums.LIMITORDER_NOPRICE_CANCEL)))
def set_backtest(initial_cash=1e7,
                 future_cost_fee=1.0,
                 stock_cost_fee=2.5,
                 rate=0.02,
                 margin_rate=1.0,
                 slide_price=0,
                 price_loc=1,
                 deal_type=0,
                 limit_type=0):
    if hasattr(cnt.env, 'set_back_test'):
        return cnt.env.set_back_test(initial_cash, future_cost_fee, stock_cost_fee, rate, margin_rate, slide_price, price_loc, deal_type, limit_type)
    return None
