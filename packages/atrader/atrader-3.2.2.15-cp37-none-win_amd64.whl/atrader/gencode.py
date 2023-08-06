# -*- coding: utf-8 -*-
# @Time     : 2019/3/6 11:41
# @Author   : kunlin.l@bitpower.com.cn
# @SoftWare : PyCharm 
# @FileName : gencode.py
# @Detail   : 生成各种运行模式的代码

import os
from atrader.tframe.utils.datetimefunc import to_int_now_date, next_n_day

__all__ = [
    'gen_template'
]


def _gen_run_real_trade_code_template(strategy_name, file_path=None):
    _code_template = """
    # -*- coding: utf-8 -*-
    from atrader import *
    
    
    def double_mean(context: 'Context'):
        len1 = context.len1
        len2 = context.len2
        max_len = max(len1, len2)
    
        target_num = len(context.target_list)
        value = np.full((target_num, 1), np.nan)
        df_data = get_reg_kdata(context.reg_kdata[0], target_indices=list(range(target_num)), length=max_len, fill_up=True, df=True)  # type: pd.DataFrame
    
        close_s = df_data['close']  # type: pd.Series
        for i in range(target_num):
            close_item = close_s.iloc[(i * max_len):(i + 1) * max_len]
            if close_item.shape[0] >= max(len1, len2):
                mean1 = np.nanmean(close_item.iloc[-len1:], dtype=np.float64)
                mean2 = np.nanmean(close_item.iloc[-len2:], dtype=np.float64)
                if mean1 - mean2 > 0.000001:
                    value[i] = 1
                if mean2 - mean1 > 0.000001:
                    value[i] = 2
        return value
    
    
    def init(context: 'Context'):
        context.len1 = 5
        context.len2 = 20
        reg_kdata('min', 1)
        reg_userindi(double_mean)
        
        
    def on_data(context: 'Context'):
        positions = context.account(0).positions
        volume_sub = positions['volume_long'] - positions['volume_short']  # type: pd.Series
        value = get_reg_userindi(context.reg_userindi[0], 1)  # type: pd.DataFrame
        for idx, _ in enumerate(context.target_list):
            if volume_sub[idx] <= 0 and value.loc[0, 'value'][idx] == 1:
                order_volume(0, idx, 100, enums.ORDERSIDE_BUY, enums.ORDERPOSITIONEFFECT_OPEN, enums.ORDERTYPE_MARKET, 0)
            elif volume_sub[idx] >= 0 and value.loc[0, 'value'][idx] == 2:
                order_volume(0, idx, 100, enums.ORDERSIDE_SELL, enums.ORDERPOSITIONEFFECT_CLOSE, enums.ORDERTYPE_MARKET, 0)

    
    if __name__ == '__main__':
        targets = ['szse.000001', 'sse.600000', 'dce.a0000', 'shfe.RB0000', 'cffex.if0000']
        run_realtrade(strategy_name='{STRATEGY_NAME}',
                      file_path='.',
                      account_list=('sim',),
                      target_list=targets,
                      frequency='min',
                      fre_num=1,
                      begin_date='{BEGIN_DATE}',
                      fq=enums.FQ_NA) 
    """

    ls = _code_template.format(STRATEGY_NAME=strategy_name,
                               BEGIN_DATE=next_n_day(to_int_now_date(), -10, out_fmt='%Y-%m-%d')).splitlines(keepends=False)[1:]
    context = '\n'.join([line[4:] for line in ls])

    if file_path is not None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(context)

    return context


def _gen_run_back_test_code_template(strategy_name, file_path=None):
    _code_template = """
    # -*- coding: utf-8 -*-
    from atrader import *


    def double_mean(context: 'Context'):
        len1 = context.len1
        len2 = context.len2
        max_len = max(len1, len2)

        target_num = len(context.target_list)
        value = np.full((target_num, 1), np.nan)
        df_data = get_reg_kdata(context.reg_kdata[0], target_indices=list(range(target_num)), 
                                length=max_len, fill_up=True, df=True)  # type: pd.DataFrame

        close_s = df_data['close']  # type: pd.Series
        for i in range(target_num):
            close_item = close_s.iloc[(i * max_len):(i + 1) * max_len]
            if close_item.shape[0] >= max(len1, len2):
                mean1 = np.nanmean(close_item.iloc[-len1:], dtype=np.float64)
                mean2 = np.nanmean(close_item.iloc[-len2:], dtype=np.float64)
                if mean1 - mean2 > 0.000001:
                    value[i] = 1
                if mean2 - mean1 > 0.000001:
                    value[i] = 2
        return value


    def init(context: 'Context'):
        context.len1 = 5
        context.len2 = 20
        reg_kdata('min', 1)
        reg_userindi(double_mean)


    def on_data(context: 'Context'):
        positions = context.account(0).positions
        volume_sub = positions['volume_long'] - positions['volume_short']  # type: pd.Series
        value = get_reg_userindi(context.reg_userindi[0], 1)  # type: pd.DataFrame
        for idx, _ in enumerate(context.target_list):
            if volume_sub[idx] <= 0 and value.loc[0, 'value'][idx] == 1:
                order_volume(0, idx, 100, enums.ORDERSIDE_BUY, enums.ORDERPOSITIONEFFECT_OPEN, enums.ORDERTYPE_MARKET, 0)
            elif volume_sub[idx] >= 0 and value.loc[0, 'value'][idx] == 2:
                order_volume(0, idx, 100, enums.ORDERSIDE_SELL, enums.ORDERPOSITIONEFFECT_CLOSE, enums.ORDERTYPE_MARKET, 0)


    if __name__ == '__main__':
        targets = ['szse.000001', 'sse.600000', 'dce.a0000', 'shfe.RB0000', 'cffex.if0000']
        run_backtest(strategy_name='{STRATEGY_NAME}',
                     file_path='.',
                     target_list=targets,
                     frequency='min',
                     fre_num=1,
                     begin_date='{BEGIN_DATE}',
                     end_date='{END_DATE}',
                     fq=enums.FQ_NA)
    """

    ls = _code_template.format(STRATEGY_NAME=strategy_name,
                               BEGIN_DATE=next_n_day(to_int_now_date(), -10, out_fmt='%Y-%m-%d'),
                               END_DATE=to_int_now_date(fmt='%Y-%m-%d')).splitlines(keepends=False)[1:]

    context = '\n'.join([line[4:] for line in ls])

    if file_path is not None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(context)

    return context


def _gen_run_factor_code_template(strategy_name, file_path=None):
    _code_template = """
    # -*- coding: utf-8 -*-
    from atrader.calcfactor import *
    import numpy as np
    import random


    def init(context: 'ContextFactor'):
        reg_kdata('day', 1)


    def calc_factor(context: 'ContextFactor'):
        return np.array([random.gauss(0, 1) for _ in range(len(context.target_list))]).T


    if __name__ == '__main__':
        run_factor(factor_name='{STRATEGY_NAME}', 
                   file_path='.', 
                   targets='SZ50', 
                   begin_date='{BEGIN_DATE}', 
                   end_date='{END_DATE}', 
                   fq=enums.FQ_FORWARD)
    """

    ls = _code_template.format(STRATEGY_NAME=strategy_name,
                               BEGIN_DATE=next_n_day(to_int_now_date(), -10, out_fmt='%Y-%m-%d'),
                               END_DATE=to_int_now_date(fmt='%Y-%m-%d')).splitlines(keepends=False)[1:]
    context = '\n'.join([line[4:] for line in ls])

    if file_path is not None:
        with open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(context)

    return context


def gen_template(code_type: 'str', dir_path=None, strategy_name=None):
    """ 生成代码模板

    :param code_type: 支持：’r‘,’b‘,’c‘, 'a', 分别代表: run_realtrade, run_backtest, run_factor, 前面所有
    :param dir_path: 生成文件路径
    :param strategy_name: 策略名称
    """

    code_type = str.lower(code_type)
    strategy_name = 'Untitle' if strategy_name is None else strategy_name
    dir_path = os.path.normpath(os.path.abspath('.') if dir_path is None or not os.path.exists(dir_path) else dir_path)

    if code_type == 'r':
        file_path = os.path.join(dir_path, strategy_name + '_realtrade.py')
        return _gen_run_real_trade_code_template(strategy_name, file_path)
    elif code_type == 'b':
        file_path = os.path.join(dir_path, strategy_name + '_backtest.py')
        return _gen_run_back_test_code_template(strategy_name, file_path)
    elif code_type == 'c':
        file_path = os.path.join(dir_path, strategy_name + '_runfactor.py')
        return _gen_run_factor_code_template(strategy_name, file_path)
    elif code_type == 'a':
        ls = []
        ls.append(gen_template('r', dir_path, strategy_name))
        ls.append(gen_template('b', dir_path, strategy_name))
        ls.append(gen_template('c', dir_path, strategy_name))
        return ls
    else:
        print("code_type 支持: 'r','b', 'c', 'a'")
    return None
