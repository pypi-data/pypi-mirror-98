
# -*- coding: utf-8 -*-

# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# KaisaGlobal rights are reserved.
# Technical index data
# ===================================================================
import sys
from os.path import dirname, abspath
import requests, datetime
import pandas as pd
import numpy as np
import json
from com import *
from pub_cls_com import *
'''Date: 2021.03.16'''

def _handle_ex_ret(code_list=['00700'], queryType='tradition', start_date='2021-03-11', end_date='2021-03-12', market=2, unit='1d', page=1, fre=2):

    body = {
        "codeList": code_list,
        "market": market,
        "queryType": queryType,
        "startDate": start_date,
        "endDate": end_date,
        "unit": unit,
        "ifRehabili": fre,
        "current": page
    }

    df_ = total_handle_req(body=body, URL=BE_TECH_POST_URL)

    return df_

###### 基础类技术面指标
def get_sar_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取SAR技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'Trend', 'WhetherTurn', 'AF', 'SAR1', 'SAR2', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_obv_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取OBV技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'OBV', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_boll_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取BOLL技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'MID', 'MD', 'UPPERValue', 'LOWERValue', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_wr_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取WR技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'WR6', 'WR10', 'WR13', 'WR34', 'WR89', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_rsi_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取RSI技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'RSI', 'RS', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_kdj_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
        获取kdj技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权  1 不复权/2 前复权/3 后复权
        Returns: 返回macd的因子数据
        '''
    factor_names = ['SecuCode', 'HighestInNine', 'LowestInNine', 'RSV', 'Kvalue', 'Dvalue', 'Jvalue', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_macd_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-22', end_date='2018-12-27', fre=2):
    '''
    获取macd技术指标数据
    Args:
        code_list: 合约列表
        queryType:数据类型
        market: 市场类型：1 CH/ 2 HK/ 3 USA
        unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
        start_date: 开始日期
        end_date: 结束日期
        fre:是否复权  1 不复权/2 前复权/3 后复权
    Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'EMA12', 'EMA26', 'DIF', 'DEA', 'MACD', 'TradingDay']
    data_type = 'tradition'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)

    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre):
    '''
    Args:
        factor_names:  所选因子字段
        f_data_: 后台api返回的数据
        data_type: 技术指标类型 tradition 传统技术指标；derived 衍生技术指标
        code_list: 合约列表
        start_date: 开始日期
        end_date: 结束日期
        market: 市场类型 1 CH/ 2 HK/ 3 USA
        unit: 频率 默认 '1d' 日级别数据
        fre: 是否复权  1 不复权/2 前复权/3 后复权

    Returns:
    '''
    pageSize = f_data_['totalPage']
    page1_data = f_data_['result']
    res_df = pd.DataFrame(page1_data)

    if pageSize > 1:
        res_df = _get_other_data(res_df, pageSize, data_type, code_list, start_date, end_date, market, unit, fre)

    __ = res_df[factor_names]
    __ = __
    return __

def _get_other_data(page1_data, page_size, data_type, code_list, start_date, end_date, market, unit, fre=2):
    # 获取剩下页码的数据
    df1_ = page1_data.copy()    #pd.DataFrame(page1_data)
    for pageC in range(2, page_size + 1):
        profit_data_next = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, pageC, fre)

        page_n_data = profit_data_next['result']
        df1_ = pd.concat([df1_, pd.DataFrame(page_n_data)], axis=0)
    return df1_

##### 衍生类技术面指标
def get_hbeta_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Hbeta技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Hbeta', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_halpha_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Halpha技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Halpha', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_hsigma_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Hsigma技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Hsigma', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_hmsens_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Dmsens技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Dmsens', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_oilsen_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Oilsen技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Oilsen', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_dsbeta_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Dsbeta技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Dsbeta', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_cmra_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Cmra技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Cmra', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_stom_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Stom技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Stom', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_stoq_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Stoq技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Stoq', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_stoa_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Stoa技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Stoa', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_dastd_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Dastd技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Dastd', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_season_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Season技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Season', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_rstr_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-20', end_date='2018-12-27', fre=2):
    '''
        获取Rstr技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Rstr', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

def get_strev_factor_data(code_list=['00700'], market=2, unit='1d', start_date='2018-12-27', end_date='2018-12-27', fre=2):
    '''
        获取strev技术指标数据
        Args:
            code_list: 合约列表
            queryType:数据类型
            market: 市场类型：1 CH/ 2 HK/ 3 USA
            unit: 频率 默认为 '1d', 将支持如下周期: '5m', '15m', '30m', '1d', '1w', '1M'. '1w' 表示一周, '1M' 表示一月
            start_date: 开始日期
            end_date: 结束日期
            fre:是否复权 默认不复权
        Returns: 返回macd的因子数据
    '''
    factor_names = ['SecuCode', 'Strev', 'Trading_Day']
    data_type = 'derived'
    f_data_ = _handle_ex_ret(code_list, data_type, start_date, end_date, market, unit, 1, fre)
    __ = _get__(f_data_, factor_names, data_type, code_list, start_date, end_date, market, unit, fre)

    return __

if __name__ == '__main__':
    pass
