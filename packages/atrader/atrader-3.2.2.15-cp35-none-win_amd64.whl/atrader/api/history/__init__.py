# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:32:28 2018

@author: kunlin.l
"""

import pandas as pd
import numpy as np

import atrader.enums as enums
from atrader.tframe.sysclsbase import smm
from atrader.tframe.convertor import convert_internal_fq_to_atcore
from atrader.tframe.sysclsbase import gv
from atrader.tframe.ufuncs import (todict, todictmc, convert_str_or_datetime_to_int_date, check_target)
from atrader.tframe.language import text
from atrader.tframe.utils.datetimefunc import to_int_now_date
from atrader.tframe.utils.argchecker import apply_rule, verify_that, convert_targets
from . import convertor as history_cvt
from . import _history

__all__ = [
    'get_code_list',
    'get_code_list_set',
    'get_main_contract',
    'get_kdata',
    'get_kdata_n',
    'get_tick_data',
    'get_trading_days',
    'get_trading_time',
    'get_stock_info',
    'get_future_info',
    'get_future_contracts',
    'get_history_instruments',
    'get_strategy_id',
    'get_performance'
]


#################################

# 非策略结构使用函数

@apply_rule(verify_that('block').is_instance_of(str),
            verify_that('date').is_valid_date(allow_empty_str=True))
def get_code_list(block: 'str', date=''):
    blocks = block.strip().split(',')
    if isinstance(date, str) and date.strip() == '':
        new_date = to_int_now_date('%Y%m%d')
    else:
        new_date = convert_str_or_datetime_to_int_date(date)
    ls = _history.get_code_list(blocks, new_date)

    return history_cvt.convert_code_list_to_df(ls)


@apply_rule(verify_that('block').is_instance_of(str),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_code_list_set(block, begin_date, end_date):
    blocks = block.strip().split(',')
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)

    if isinstance(end_date, str) and end_date.strip() == '':
        new_end_date = to_int_now_date('%Y%m%d')
    else:
        new_end_date = convert_str_or_datetime_to_int_date(end_date)

    if 0 < new_end_date < new_begin_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    ls = _history.get_code_list_set(blocks, new_begin_date, new_end_date)

    return history_cvt.convert_code_list_set_to_df(ls)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('main_code').is_instance_of(str),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_main_contract(main_code: 'str',
                      begin_date,
                      end_date):
    begin_date = convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        end_date = to_int_now_date('%Y%m%d')
    else:
        end_date = convert_str_or_datetime_to_int_date(end_date)
    target_list = convert_targets([main_code])
    new_targets = todictmc(target_list)

    if begin_date > end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)
    data_dict = _history.get_main_contract(new_targets, begin_date, end_date)

    return history_cvt.convert_main_contract_to_df(data_dict)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('code').is_instance_of(str),
            verify_that('date').is_valid_date(),
            verify_that('fq').is_in((enums.FQ_NA,
                                     enums.FQ_FORWARD,
                                     enums.FQ_BACKWARD)),
            verify_that('df').is_in((False, True)))
def get_tick_data(code: 'str', date='', fq=enums.FQ_NA, df=False):
    today = to_int_now_date()
    if isinstance(date, str) and date.strip() == '':
        tick_day = to_int_now_date('%Y%m%d')
    else:
        tick_day = convert_str_or_datetime_to_int_date(date)
    if 0 < today < tick_day:
        raise ValueError(text.ARGCHECKER_INVALID_PARAM_FUTURE_DATE_ERROR.format(date))

    target = todictmc(convert_targets([code])[0])
    fq_type = convert_internal_fq_to_atcore(fq)
    info_dict = dict(_history.load_tick_data_from_pro(target['Market'], target['Code'], tick_day, fq_type, check_permission=True))

    if df:
        return history_cvt.convert_tick_data_to_df(info_dict)
    else:
        return history_cvt.convert_tick_data_to_order_list(info_dict)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(list, tuple, str),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min', 'year')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date(),
            verify_that('fq').is_in((enums.FQ_NA,
                                     enums.FQ_FORWARD,
                                     enums.FQ_BACKWARD)),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by_date').is_in((True, False)))
def get_kdata(target_list: 'list',
              frequency: 'str',
              fre_num: 'int',
              begin_date,
              end_date,
              fq=enums.FQ_NA,
              fill_up=False,
              df=False,
              sort_by_date=False):
    if isinstance(target_list, str):
        target_list = [target_list]

    if len(target_list) < 1:
        raise ValueError(text.ERROR_INPUT_EMPTY_PARAM.format(PARAMNAME='target_list'))

    begin_date = convert_str_or_datetime_to_int_date(begin_date)
    end_date = convert_str_or_datetime_to_int_date(end_date)
    new_targets = todictmc(convert_targets(target_list))
    fq = convert_internal_fq_to_atcore(fq)

    if 0 < end_date < begin_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    results = [None] * len(new_targets)
    target_infos = _history.get_target_info(new_targets)
    data_list = _history.get_k_data_independent_target(new_targets, frequency, fre_num, begin_date, end_date, fill_up, fq)
    for idx, data in enumerate(data_list):
        results[idx] = history_cvt.convert_k_data_to_df(data, target_list[idx], target_infos[idx]['Type'])
    if df:
        data_df = pd.concat(results, ignore_index=True)  # type: pd.DataFrame
        if sort_by_date:
            data_df = data_df.sort_values('time', ascending=True, na_position='first')  # type: pd.DataFrame
            data_df.index = range(data_df.shape[0])
        return data_df
    else:
        return {target: results[idx] for idx, target in enumerate(target_list)}


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(str, list, tuple),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('end_date').is_valid_date(allow_empty_str=True),
            verify_that('n').is_instance_of(int).is_greater_than(0).is_less_than(1000),
            verify_that('fq').is_in((enums.FQ_NA, enums.FQ_BACKWARD, enums.FQ_FORWARD)),
            verify_that('fill_up').is_in((True, False)),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by_date').is_in((True, False)))
def get_kdata_n(target_list: 'list',
                frequency: 'str',
                fre_num: 'int',
                n: 'int',
                end_date: 'str',
                fq=0,
                fill_up=False,
                df=False,
                sort_by_date=False):
    if isinstance(target_list, str):
        target_list = [target_list]

    if len(target_list) < 1:
        raise ValueError(text.ERROR_INPUT_EMPTY_PARAM.format(PARAMNAME='target_list'))

    if isinstance(end_date, str) and end_date.strip() == '':
        end_date = to_int_now_date('%Y%m%d')
    else:
        end_date = convert_str_or_datetime_to_int_date(end_date)

    new_targets = todictmc(convert_targets(target_list))
    fq = convert_internal_fq_to_atcore(fq)

    if frequency in ('day', 'week', 'month') and fre_num != 1:
        raise ValueError(text.ERROR_INPUT_FREQUENCY_FREQNUM)

    results = [None] * len(new_targets)
    target_infos = _history.get_target_info(new_targets)
    for idx, target in enumerate(new_targets):
        data = _history.get_k_data_n([target], frequency, fre_num, n, end_date, fill_up, fq)
        results[idx] = history_cvt.convert_k_data_n_to_df(data[0], target_list[idx], target_infos[idx]['Type'])
    if df:
        data_df = pd.concat(results, ignore_index=True)  # type: pd.DataFrame
        if sort_by_date:
            data_df = data_df.sort_values('time', ascending=True, na_position='first')  # type: pd.DataFrame
            data_df.index = range(data_df.shape[0])
        return data_df
    else:
        return {target: results[idx] for idx, target in enumerate(target_list)}


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('market').is_instance_of(str),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_trading_days(market: 'str',
                     begin_date,
                     end_date=''):
    # TODO market: 支持数字货币
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        new_end_date = to_int_now_date('%Y%m%d')
    else:
        new_end_date = convert_str_or_datetime_to_int_date(end_date)
    if new_begin_date > new_end_date:
        return None

    result = _history.get_trading_days_condition(market, new_begin_date, new_end_date)
    if result.size < 1:
        return None

    return history_cvt.convert_trading_days_to_np_datetime(result)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('frequency').is_in(('day', 'week', 'month', 'min')),
            verify_that('fre_num').is_instance_of(int),
            verify_that('begin_date').is_valid_date(allow_empty_str=False),
            verify_that('end_date').is_valid_date(allow_empty_str=True))
def get_trading_time(target_list: 'list',
                     frequency: 'str',
                     fre_num: 'int',
                     begin_date,
                     end_date=''):
    if isinstance(target_list, str):
        target_list = [target_list]

    new_targets = todictmc(convert_targets(target_list))
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)
    if isinstance(end_date, str) and end_date.strip() == '':
        new_end_date = to_int_now_date('%Y%m%d')
    else:
        new_end_date = convert_str_or_datetime_to_int_date(end_date)

    if frequency in ('day', 'week', 'month') and fre_num != 1:
        raise ValueError(text.ERROR_INPUT_FREQUENCY_FREQNUM)

    if 0 < new_end_date < new_begin_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    t, d = _history.get_trading_time(new_targets, frequency, new_begin_date, new_end_date, fre_num)

    if gv.frequency_to_int(frequency) >= gv.KFreq_Day:
        d = np.arange(0, t.size, 1, dtype=np.int)
    else:
        d -= 1

    return history_cvt.convert_trading_time_to_df(t, d)


#################################
# 标的查询接口
@smm.force_mode(gv.RUNMODE_CONSOLE, gv.RUNMODE_BEFORE_BACKTEST, gv.RUNMODE_BEFORE_REALTRADE)
@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(list))
def get_stock_info(target_list: 'list'):
    ls = _history.get_stock_info_ex(target_list)
    return history_cvt.convert_stock_info_to_df(ls)


@smm.force_mode(gv.RUNMODE_CONSOLE, gv.RUNMODE_BEFORE_BACKTEST, gv.RUNMODE_BEFORE_REALTRADE)
@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(str, list, tuple))
def get_future_info(target_list: 'list'):
    ls = _history.get_future_info_ex(convert_targets(target_list))
    return history_cvt.convert_future_info_to_df(ls)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('target_list').is_instance_of(list),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date(allow_empty_str=True),
            verify_that('df').is_in((True, False)),
            verify_that('sort_by_date').is_in((True, False)))
def get_history_instruments(target_list: 'list',
                            begin_date,
                            end_date='',
                            df=False,
                            sort_by_date=True):
    if isinstance(target_list, str):
        target_list = [target_list]

    targets = check_target(todictmc(convert_targets(target_list)))
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)
    new_end_date = to_int_now_date() if end_date == '' else convert_str_or_datetime_to_int_date(end_date)
    if begin_date != 0 and new_begin_date > new_end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)

    data_dict = _history.get_history_instruments(targets, new_begin_date, new_end_date)

    return history_cvt.convert_history_instrument_matrix_to_output(target_list, data_dict, df, sort_by_date)


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
def get_strategy_id():
    ids = _history.get_strategy_id()
    for ID in ids:
        ID.strategy_id = str(ID.strategy_id)
    return [todict(item) for item in ids]


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('strategy_id').is_instance_of(str))
def get_performance(strategy_id):
    results = _history.get_performance(int(strategy_id))
    return None if len(results) < 1 else history_cvt.convert_back_test_performance(results[0])


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('date').is_valid_date(),
            verify_that('market').is_instance_of(str),
            verify_that('varieties').is_instance_of(str))
def get_future_contracts(date, market='all', varieties='all'):
    int_date = convert_str_or_datetime_to_int_date(date)
    data_dict = _history.get_future_contracts(int_date, market, varieties)
    return [] if len(data_dict) < 1 else history_cvt.convert_future_contracts_info(data_dict)