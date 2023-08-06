# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:31:39 2018

@author: kunlin.l
"""

from atrader.tframe.ufuncs import (todotmc, todictmc, convert_str_or_datetime_to_int_date, check_target)
from atrader.tframe.language import text
from atrader.tframe.utils.datetimefunc import to_int_now_date, check_begin_end_date
from atrader.tframe.utils.argchecker import apply_rule, verify_that, convert_targets
from atrader.tframe.sysclsbase import gv
from atrader.tframe.sysclsbase import smm
from . import _factors
from . import convertor as factor_cvt

__all__ = [
    'get_factor_by_factor',
    'get_factor_by_day',
    'get_factor_by_code',
]


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor').is_instance_of(str),
            verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date())
def get_factor_by_factor(factor: 'str',
                         target_list: 'list',
                         begin_date,
                         end_date):
    if isinstance(target_list, str):
        target_list = [target_list]

    targets = check_target(todictmc(convert_targets(target_list)))
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)
    new_end_date = convert_str_or_datetime_to_int_date(end_date)
    if begin_date != 0 and new_begin_date > new_end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)
    check_begin_end_date(new_begin_date, new_end_date)
    factor_dict = _factors.get_factor_by_factor(factor, targets, new_begin_date, new_end_date)
    result_df = factor_cvt.convert_factor_by_factor_to_df(factor_dict, todotmc(targets)) if factor_dict['date'].size > 0 else None
    return result_df


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor_list').is_instance_of(str, tuple, list),
            verify_that('target_list').is_instance_of(str, tuple, list),
            verify_that('date').is_valid_date(allow_empty_str=True))
def get_factor_by_day(factor_list: 'list',
                      target_list: 'list',
                      date=''):
    if isinstance(factor_list, str):
        factor_list = [factor_list]

    if isinstance(target_list, str):
        target_list = [target_list]

    targets = check_target(todictmc(convert_targets(target_list)))
    if date == '':
        new_date = to_int_now_date()
    else:
        new_date = convert_str_or_datetime_to_int_date(date)
    check_begin_end_date(new_date, new_date)
    factor_dict = _factors.get_factor_by_day(factor_list, targets, new_date)
    factor_df = factor_cvt.convert_factor_by_day_to_df(factor_dict) if factor_dict is not None else None

    return factor_df


@smm.force_phase(gv.RUMMODE_PHASE_USERINIT, gv.RUMMODE_PHASE_DEFAULT)
@apply_rule(verify_that('factor_list').is_instance_of(str, tuple, list),
            verify_that('target').is_instance_of(str),
            verify_that('begin_date').is_valid_date(),
            verify_that('end_date').is_valid_date())
def get_factor_by_code(factor_list: 'list',
                       target: 'str',
                       begin_date,
                       end_date):
    if isinstance(factor_list, str):
        factor_list = [factor_list]

    targets = check_target(todictmc([target]))
    new_begin_date = convert_str_or_datetime_to_int_date(begin_date)
    new_end_date = convert_str_or_datetime_to_int_date(end_date)
    if begin_date != 0 and new_begin_date > new_end_date:
        raise ValueError(text.ERROR_INPUT_BEGIN_GT_ENDDATE)
    check_begin_end_date(new_begin_date, new_end_date)
    factor_dict = _factors.get_factor_by_code(factor_list, targets, new_begin_date, new_end_date)
    factor_df = factor_cvt.convert_factor_by_code_to_df(factor_dict) if factor_dict is not None else None
    return factor_df
