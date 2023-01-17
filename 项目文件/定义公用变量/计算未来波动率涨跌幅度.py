import numpy as np
import pandas as pd
import os
import copy
from 数据文件.基本参数 import *



#定义未来波动率涨跌幅度：时间序列数据
class DefinitionVolatilityChangeFuture():

    def __init__(self,
                 option,
                 col_iv='impl_volatility',#所计算数据格式为时间序列格式还是截面数据格式？
                                         # 'impl_volatility':时间序列格式
                                         # ['AAPL','SPX']:截面数据格式，且列表长度需大于1

                 days_future=30,#未来的n个交易日
                 col_date='date',
                 ):
        self.option = option  # 期权数据
        self.col_iv=col_iv
        
        #根据列标题判断所用数据格式:所计算数据格式为时间序列格式还是截面数据格式？
        self.type_data='series' if type(col_iv) is str else 'cross'
        
        self.days_future=days_future
        self.col_date=col_date
        
    def format_output(self,output):
        if self.type_data=='series':
            return output
        elif self.type_data=='cross':
            return output[self.col_iv]


    #未来第t+m个交易日的波动率相比于当前交易日t的涨跌额
    def dV_future(self):
        option_dV_future=copy.deepcopy(self.option)
        option_dV_future[self.col_iv]=self.option[self.col_iv].diff(-self.days_future)
        return self.format_output(option_dV_future)


    #未来第t+m个交易日的波动率相比于当前交易日t的涨跌幅(%)
    def rV_future(self):
        option_rV_future=copy.deepcopy(self.option)
        option_rV_future[self.col_iv]=np.log(self.option[self.col_iv].shift(-self.days_future)/self.option[self.col_iv])
        return self.format_output(option_rV_future)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动均值的差值
    def dV_future_mean(self):
        option_dV_future_mean = copy.deepcopy(self.option).sort_index(ascending=False)
        option_dV_future_mean[self.col_iv] = option_dV_future_mean[self.col_iv].shift(self.days_future)-option_dV_future_mean[self.col_iv].rolling(self.days_future).mean()
        option_dV_future_mean.sort_index(ascending=True,inplace=True)
        return self.format_output(option_dV_future_mean)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动均值的差值百分比（%）
    def rV_future_mean(self):
        option_rV_future_mean = copy.deepcopy(self.option).sort_index(ascending=False)
        option_rV_future_mean[self.col_iv] = np.log(option_rV_future_mean[self.col_iv].shift(self.days_future) /
                                             option_rV_future_mean[self.col_iv].rolling(self.days_future).mean())
        option_rV_future_mean.sort_index(ascending=True, inplace=True)
        return self.format_output(option_rV_future_mean)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动均值的差值（移动标准差个数）
    def dV_future_std(self):
        option_rV_future_std = copy.deepcopy(self.option).sort_index(ascending=False)
        option_rV_future_std[self.col_iv] = (option_rV_future_std[self.col_iv].shift(self.days_future)-option_rV_future_std[self.col_iv].rolling(self.days_future).mean())/option_rV_future_std[self.col_iv].rolling(self.days_future).std()
        option_rV_future_std.sort_index(ascending=True, inplace=True)
        return self.format_output(option_rV_future_std)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动最小值的差值
    def dV_future_min(self):
        option_dV_future_min = copy.deepcopy(self.option).sort_index(ascending=False)
        option_dV_future_min[self.col_iv] = option_dV_future_min[self.col_iv].shift(self.days_future)-option_dV_future_min[self.col_iv].rolling(self.days_future).min()
        option_dV_future_min.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dV_future_min)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动最大值的差值
    def dV_future_max(self):
        option_dV_future_max = copy.deepcopy(self.option).sort_index(ascending=False)
        option_dV_future_max[self.col_iv] = option_dV_future_max[self.col_iv].shift(self.days_future)-option_dV_future_max[self.col_iv].rolling(self.days_future).max()
        option_dV_future_max.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dV_future_max)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动最小值的差值百分比（%）
    def rV_future_min(self):
        option_dV_future_min = copy.deepcopy(self.option).sort_index(ascending=False)
        option_dV_future_min[self.col_iv] = np.log(option_dV_future_min[self.col_iv].shift(self.days_future)/option_dV_future_min[self.col_iv].rolling(self.days_future).min())
        option_dV_future_min.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dV_future_min)


    #未来第t+m个交易日的波动率相比于未来m个交易日移动最大值的差值百分比（%）
    def rV_future_max(self):
        option_dV_future_max = copy.deepcopy(self.option).sort_index(ascending=False)
        option_dV_future_max[self.col_iv] = np.log(option_dV_future_max[self.col_iv].shift(self.days_future)/option_dV_future_max[self.col_iv].rolling(self.days_future).max())
        option_dV_future_max.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dV_future_max)


    #未来第t+m个交易日的波动率高于未来m个交易日移动均值的k个移动标准差（哑元变量）
    def dummy_future_diff_higher_std(self,K=2):
        option_dummy_future_diff_higher_std = copy.deepcopy(self.option).sort_index(ascending=False)
        std_roll=option_dummy_future_diff_higher_std[self.col_iv].rolling(self.days_future).std()
        mean_roll=option_dummy_future_diff_higher_std[self.col_iv].rolling(self.days_future).mean()
        option_dummy_future_diff_higher_std[self.col_iv] =(option_dummy_future_diff_higher_std[self.col_iv]-mean_roll>=K*std_roll)*1
        option_dummy_future_diff_higher_std.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dummy_future_diff_higher_std)


    #未来第t+m个交易日的波动率低于未来m个交易日移动均值的K个移动标准差（哑元变量）
    def dummy_future_diff_lower_std(self,K=2):
        option_dummy_future_diff_lower_std = copy.deepcopy(self.option).sort_index(ascending=False)
        std_roll=option_dummy_future_diff_lower_std[self.col_iv].rolling(self.days_future).std()
        mean_roll=option_dummy_future_diff_lower_std[self.col_iv].rolling(self.days_future).mean()
        option_dummy_future_diff_lower_std[self.col_iv] =(mean_roll-option_dummy_future_diff_lower_std[self.col_iv]>=K*std_roll)*1
        option_dummy_future_diff_lower_std.sort_index(ascending=True, inplace=True)
        return self.format_output(option_dummy_future_diff_lower_std)


    # 通过在列表中填入将使用的变量类型，计算相应的变量
    def varibles_type(self,
                      cols_varible_type=[],  # 所使用变量的类型
                      # 可选择范围  ['dV_future','rV_future','dV_future_mean','rV_future_mean','dV_future_std','dV_future_min','dV_future_max','rV_future_min','rV_future_max','dummy_future_diff_higher_std','dummy_future_diff_lower_std',]

                      K=1,
                      ):

        VolatilityChange_s = {}

        if 'dV_future' in cols_varible_type:
            VolatilityChange_s['dV_future'] = self.dV_future()
        if 'rV_future' in cols_varible_type:
            VolatilityChange_s['rV_future'] = self.rV_future()
        if 'dV_future_mean' in cols_varible_type:
            VolatilityChange_s['dV_future_mean'] = self.dV_future_mean()
        if 'rV_future_mean' in cols_varible_type:
            VolatilityChange_s['rV_future_mean'] = self.rV_future_mean()
        if 'dV_future_std' in cols_varible_type:
            VolatilityChange_s['dV_future_std'] = self.dV_future_std()
        if 'dV_future_min' in cols_varible_type:
            VolatilityChange_s['dV_future_min'] = self.dV_future_min()
        if 'dV_future_max' in cols_varible_type:
            VolatilityChange_s['dV_future_max'] = self.dV_future_max()
        if 'rV_future_min' in cols_varible_type:
            VolatilityChange_s['rV_future_min'] = self.rV_future_min()
        if 'rV_future_max' in cols_varible_type:
            VolatilityChange_s['rV_future_max'] = self.rV_future_max()
        if 'dummy_future_diff_higher_std' in cols_varible_type:
            VolatilityChange_s['dummy_future_diff_higher_std'] = self.dummy_future_diff_higher_std(K=K)
        if 'dummy_future_diff_lower_std' in cols_varible_type:
            VolatilityChange_s['dummy_future_diff_lower_std'] = self.dummy_future_diff_lower_std(K=K)

        return VolatilityChange_s












if __name__=='__main__':
    #计算未来的波动率涨跌幅
    from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol

    # 获取指定格式的截面数据
    vol_cross = get_cross_vol(path_vol=PATH_VOL_SAMPLE, num_date=757, )
    DVCP = DefinitionVolatilityChangeFuture(option=vol_cross,col_iv=['AAPL','SPX'])
    DVCP.dV_future()
    DVCP.rV_future()
    DVCP.dV_future_mean()
    DVCP.rV_future_mean()
    DVCP.dV_future_std()
    DVCP.dV_future_min()
    DVCP.dV_future_max()
    DVCP.rV_future_min()
    DVCP.rV_future_max()
    DVCP.dummy_future_diff_higher_std(K=1)
    DVCP.dummy_future_diff_lower_std(K=1)

    # 获得指定个股的时间序列数据
    vol_series = get_series_vol(path_vol=PATH_VOL_SAMPLE, ticker='SPX', )
    DVCP=DefinitionVolatilityChangeFuture(option=vol_series)
    DVCP.dV_future()
    DVCP.rV_future()
    DVCP.dV_future_mean()
    DVCP.rV_future_mean()
    DVCP.dV_future_std()
    DVCP.dV_future_min()
    DVCP.dV_future_max()
    DVCP.rV_future_min()
    DVCP.rV_future_max()
    DVCP.dummy_future_diff_higher_std(K=1)
    DVCP.dummy_future_diff_lower_std(K=1)
























