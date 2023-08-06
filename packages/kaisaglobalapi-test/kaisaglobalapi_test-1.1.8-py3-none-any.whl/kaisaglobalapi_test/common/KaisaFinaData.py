
# -*- coding: utf-8 -*-

# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# KaisaGlobal rights are reserved.
# FinanceData
# ===================================================================
import sys
from os.path import dirname, abspath
import requests, datetime
import pandas as pd
import numpy as np
import json
from com import *
from pub_cls_com import *
'''Date: 2021.03.15'''

################################财务数据##################################
###### 基础财务数据(主要财务数据、三大报表)
def _handle_req_ret(period, report_type, code, market):
    # 基础财务数据: 公共统一处理请求和返回数据
    body = {
        "reportType": report_type,
        "periodMark": period,
        "stockCode": code,
        "stockMarket": market
    }

    _df_ = total_handle_req(body=body, URL=BASIC_FIN_POST_URL)
    return _df_

def get_basic_fin_data(code='00700', market='hkg', period=12, report_type='1'):
    '''
    periodMark	integer($int32) null-全部 3-一季度，6-半年度，9-三季度，12-年度
    reportType	string 1：主要指标
    stockCode	string 股票代码
    stockMarket	string 港股：hkg，美股：usa,a股：chn
    Returns:
        df:
        主要财务指标  季度/年度的财务数据
    '''
    basic_fin_df = _handle_req_ret(period, report_type, code, market)

    return basic_fin_df

def get_income_fin_data(code='00700', market='hkg', period=12, report_type='2'):
    '''
    Args:
        code: string 股票代码
        market: string 港股：hkg，美股：usa,a股：chn
        period: integer($int32) null-全部 3-一季度，6-半年度，9-三季度，12-年度
        report_type: string 2：利润表
    Returns:
        df:
        income 季度/年度的财务数据
    '''
    income_fin_df = _handle_req_ret(period, report_type, code, market)

    return income_fin_df

def get_balance_fin_data(code='00700', market='hkg', period=12, report_type='3'):
    '''
    Args:
        code: string 股票代码
        market: string 港股：hkg，美股：usa,a股：chn
        period: integer($int32) null-全部 3-一季度，6-半年度，9-三季度，12-年度
        report_type: string 3：资产负债表
    Returns:
        df:
        balance 季度/年度的财务数据
    '''
    balance_fin_df = _handle_req_ret(period, report_type, code, market)

    return balance_fin_df

def get_cashflow_fin_data(code='00700', market='hkg', period=12, report_type='4'):
    '''
    Args:
        code: string 股票代码
        market: string 港股：hkg，美股：usa,a股：chn
        period: integer($int32) null-全部 3-一季度，6-半年度，9-三季度，12-年度
        report_type: string 4：现金流量表
    Returns:
        df
        cashflow  季度/年度的财务数据
    '''
    cashflow_fin_df = _handle_req_ret(period, report_type, code, market)

    return cashflow_fin_df

###### 衍生财务数据(财务因子)

def _handle_ex_ret(code_list=['00700'], queryType='profit', start_date='2018-12-31', end_date='2020-12-31', market=2, period=12, page=1):
    if queryType == 'baseFace':
        body = {
            "codeList": code_list,
            "market": market,
            "queryType": queryType,
            "startDate": start_date,
            "endDate": end_date,
            "periodMark": period,
            "current": page
        }
    else:
        body = {
            "codeList": code_list,
            "market": market,
            "queryType": queryType,
            "periodMark": period,
            "current": page
        }
    
    df_ = total_handle_req(body=body, URL=EX_FIN_POST_URL)

    return df_

def _handle_get_fina_data_cls(_data_, data_type, code_list, start_date, end_date, market, period):
    # 统一get财务数据
    info_date = 'InfoPublDate'
    date_type_dic = {'baseFace': 'Trading_Day', 'profit': info_date, 'cashFlow': info_date, 'operation': info_date, 'debtPay': info_date, 'growth': info_date}
    dt_filter_field = date_type_dic[data_type]

    pageSize = _data_['totalPage']
    page1_data = _data_['result']
    df1_ = pd.DataFrame(page1_data)
    for pageC in range(2, pageSize + 1):
        profit_data_next = _handle_ex_ret(code_list, 'profit', start_date, end_date, market, period, pageC)
        page_n_data = profit_data_next['result']
        df1_ = pd.concat([df1_, pd.DataFrame(page_n_data)], axis=0)

    if (start_date is None and end_date is not None) or (start_date is not None and end_date is None):
        cur_dt = end_date if start_date is None else start_date
        df1_ = df1_[df1_[dt_filter_field] <= cur_dt]
        dt_type = 1

    elif start_date is not None and end_date is not None:
        df1_ = df1_[(df1_[dt_filter_field] >= start_date) & (df1_[dt_filter_field] <= end_date)]
        dt_type = 2
    else:
        df1_ = df1_[df1_[dt_filter_field] <= datetime.datetime.now().strftime('%Y-%m-%d')]
        dt_type = 1
    __ = _get___(df1_, dt_type, dt_filter_field)

    return __

def _get___(df, dt_type=1, dt_filter_field='InfoPublDate'):
    '''
    Args:
        df: 原始数据
        dt_type: 时间类型【start_date/end_date】
    Returns:
    返回所需的衍生财务/基本面因子数据
    '''
    # 统一过滤得到最后需要的财务数据-df
    __ = pd.DataFrame()
    for code in list(set(list(df['SecuCode']))):
        df1_this = df[df['SecuCode'] == code]
        df1_this.sort_values(by=[dt_filter_field], inplace=True, ascending=False)
        if dt_type == 1:
            df1_this = df1_this.head(1)
            df1_this.set_index('InfoPublDate', inplace=True)
        if dt_type == 2:
            #df1_this.set_index('Trading_Day', inplace=True)
            pass
        df1_this = df1_this.T
        if __.empty:
            __ = df1_this.copy()
        else:
            __ = pd.concat([__, df1_this], axis=1)
    return __


def get_profit_factor_fin_data(code_list=['00700'], start_date='2018-12-31', end_date='2020-12-31', market=2, period=12):
    '''
        获取盈利能力因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是上市公司公布财报的日期)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    __ = _all_fina_factor_handle_method(code_list, 'profit', start_date, end_date, market, period)
    return __

def get_cash_flow_factor_fin_data(code_list=['00700'], start_date=None, end_date='2018-12-31', market=2, period=12):
    '''
        获取现金流因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是上市公司公布财报的日期)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    data_type = 'cashFlow'
    __ = _all_fina_factor_handle_method(code_list, data_type, start_date, end_date, market, period)
    return __

def get_operation_factor_fin_data(code_list=['00700'], start_date=None, end_date='2018-12-31', market=2, period=12):
    '''
        获取运营能力因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是上市公司公布财报的日期)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    data_type = 'operation'
    __ = _all_fina_factor_handle_method(code_list, data_type, start_date, end_date, market, period)
    return __

def get_growth_factor_fin_data(code_list=['00700'], start_date=None, end_date='2018-12-31', market=2, period=12):
    '''
        获取成长能力因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是上市公司公布财报的日期)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    data_type = 'growth'
    __ = _all_fina_factor_handle_method(code_list, data_type, start_date, end_date, market, period)
    return __

def get_debtPay_factor_fin_data(code_list=['00700'], start_date=None, end_date='2018-12-31', market=2, period=12):
    '''
        获取偿债能力因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是上市公司公布财报的日期)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    data_type = 'debtPay'
    __ = _all_fina_factor_handle_method(code_list, data_type, start_date, end_date, market, period)
    return __

def _all_fina_factor_handle_method(code_list=['00700'], data_type='profit', start_date='2018-12-31', end_date=None, market=2, period=12):
    # 集中处理_handle_ex_ret/_handle_get_fina_data_cls
    if _t_typeof(code_list) != 'list':return pd.DataFrame()
    profit_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, period)
    __ = _handle_get_fina_data_cls(profit_data_, data_type, code_list, start_date, end_date, market, period)
    return __


def _t_typeof(variate):
    '''返回变量的类型'''
    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type

def get_baseFace_factor_fin_data(code_list=['00700'], start_date=None, end_date='2018-12-28', market=2, period=12):
    '''
        获取一般基本面因子数据
        Args:
            code_list: 股票篮子 ['00700']/['00700','06969']
            start_date: 开始日期 如 ‘2016-12-31’
            end_date: 结束日期 如 ‘2018-12-31’
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            period: 报表类型：0全部, 3一季报,6中报,9三季报,12年报
        Returns:
        PS： 1.如果指定了start_date和end_date那返回的是这个区间的财务因子数据,(时间对应的是每日行情数据更新后的交易日)
            2.如果只指定了开始日期或者结束日期则取这个日期的最近一期的财务因子数据
            3.如果两个日期都没指定，则取最近一期的财务因子数据
        对应股票篮子的历史财务数据
    '''
    data_type = 'baseFace'
    if end_date is None and start_date is None:
        print('必须指定start_date或end_date字段')
        return pd.DataFrame()
    if end_date is None and start_date is not None:
        end_date = start_date
    if end_date is not None and start_date is None:
        start_date = end_date
    profit_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, period)
    __ = _handle_get_fina_data_cls(profit_data_, data_type, code_list, start_date, end_date, market, period)

    return __
################################财务数据##################################