# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
from atrader import enums
from atrader.tframe.uclass import MinListWrapper
from atrader.tframe.utils.argchecker import apply_rule, verify_that
from atrader.tframe.udefs import INTEGERS_TYPE
from atrader.tframe.utils.utilcls import OrderedDotDict


class AccountSnapshot:
    """
        账户信息快照，提供调用时刻的实时账户信息
        公有属性:
        ::
            name: str: 账户名称
            account_idx: int 账户索引
            type: int 账户类型
        ..
        公有方法:
        ::
            position:获取指定标的和方向的仓位信息
            positions: 获得所有仓位的双向仓位信息
            cash: 获得账户的资金信息
        ..
    """

    def __init__(self, account_idx, acc_type, name, env):
        self.name = name
        self.account_idx = account_idx
        self.account_type = acc_type
        self._env = env

    @property
    def positions(self) -> 'pd.DataFrame':
        """ 账户的双向仓位信息

        :return: pandas.df or OrderDict 双向持仓信息
        """
        return self._env.snap.positions(self.account_idx, True)

    @property
    def cash(self) -> 'pd.DataFrame':
        """ 账户的资金信息

        :return: pandas.df or OrderDict 账户资金信息
        """
        return self._env.snap.cash(self.account_idx, True)

    @apply_rule(verify_that('target_idx').is_instance_of(*INTEGERS_TYPE, list, tuple))
    def position(self, target_idx=(), side=enums.POSITIONSIDE_UNKNOWN, df=True) -> 'pd.DataFrame':
        """
        从positions中构建position
        :param target_idx: 标的索引
        :param side: 持仓方向
        :param df: 是否生成dataframe对象
        :return: df or OrderDict position对象
        """
        if isinstance(target_idx, INTEGERS_TYPE):
            target_idx = [target_idx]
        if len(target_idx) < 1:
            target_idx = list(range(self._env.target_idx_count))
        else:
            _, target_idx = self._env.check_idx('position', None, target_idx, False)
        return self._env.snap.position(self.account_idx, target_idx, side, df)


class OrderSnapshot(OrderedDotDict):
    # __slots__ = ['account_name', 'account_idx', 'order_id', 'order_id_broker', 'order_type', 'status', 'value',
    #              'code', 'target_idx', 'position_effect', 'side', 'source', 'price', 'volume', 'rej_reason', 'created',
    #              'filled_volume', 'filled_average', 'filled_amount', 'updated']

    def __init__(self):
        super(OrderedDotDict, self).__init__()
        self.account_name = None
        self.account_idx = None
        self.order_id = None
        self.order_id_broker = None
        self.code = None
        self.target_idx = None
        self.side = None
        self.position_effect = None
        self.order_type = None
        self.source = None
        self.status = None
        self.rej_reason = float('nan')
        self.price = None
        self.volume = None
        self.value = None
        self.filled_volume = None
        self.filled_average = None
        self.filled_amount = None
        self.created = None
        self.updated = None


class ExecutionSnapshot(OrderedDotDict):
    # __slots__ = ['account_name', 'account_idx', 'order_id', 'order_id_broker', 'trade_id', 'code',
    #              'target_idx', 'position_effect', 'side', 'price', 'volume', 'amount', 'created']

    def __init__(self):
        super(OrderedDotDict, self).__init__()
        self.account_name = None
        self.account_idx = None
        self.order_id = None
        self.order_id_broker = None
        self.trade_id = None
        self.code = None
        self.target_idx = None
        self.position_effect = None
        self.side = None
        self.price = None
        self.volume = None
        self.amount = None
        self.created = None


class _ContextBase:
    def __init__(self):
        self.target_list = []
        self.reg_kdata = MinListWrapper()
        self.reg_factor = MinListWrapper()
        self.reg_userindi = MinListWrapper()
        self.reg_userdata = MinListWrapper()
        self.now = datetime(1990, 1, 1)


class ContextBackReal(_ContextBase):
    def __init__(self):
        super(ContextBackReal, self).__init__()
        self.day_begin = False
        self.account_list = []
        self.backtest_setting = {}
        # 生成 account 列表
        self._acc_snapshot_list = []

    def init_acc_snapshot(self, env, accounts):
        """ 生成Account对象列表

        """
        self.account_list = accounts.copy()
        self._acc_snapshot_list = [AccountSnapshot(account.handle_idx, account.type, account.name, env) for account in self.account_list]

    def account(self, account_idx=0) -> 'AccountSnapshot':
        """根据账户索引获取账户信息

        :param account_idx: 账户索引，默认为0 也就是第一个账户的信息
        :return: Account对象
        """

        return self._acc_snapshot_list[account_idx]


class ContextFactor(_ContextBase):
    def __init__(self):
        super(ContextFactor, self).__init__()
