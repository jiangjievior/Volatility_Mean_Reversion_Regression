import numpy as np
import pandas as pd
import os
import copy
from 数据文件.基本参数 import *



#定义过去波动率涨跌幅度：时间序列数据
class DefinitionVolatilityChangePast():

    def __init__(self,
                 option,
                 col_iv='impl_volatility',#所计算数据格式为时间序列格式还是截面数据格式？
                                         # 'impl_volatility':时间序列格式
                                         # ['AAPL','SPX']:截面数据格式，且列表长度需大于1

                 days_past=30,#过去的n个交易日
                 col_date='date',
                 ):
        self.option = option  # 期权数据
        self.col_iv=col_iv
        
        #根据列标题判断所用数据格式:所计算数据格式为时间序列格式还是截面数据格式？
        self.type_data='series' if type(col_iv) is str else 'cross'
        
        self.days_past=days_past
        self.col_date=col_date
        
    def format_output(self,output):
        if self.type_data=='series':
            return output
        elif self.type_data=='cross':
            return output[self.col_iv]


    #当前交易日的波动率相比于第t-n个交易日的涨跌额
    def dV_past(self):
        option_dV_past=copy.deepcopy(self.option)
        option_dV_past[self.col_iv]=self.option[self.col_iv].diff(self.days_past)
        return self.format_output(option_dV_past)


    #当前交易日的波动率相比于第t-n个交易日的涨跌幅（%）
    def rV_past(self):
        option_rV_past=copy.deepcopy(self.option)
        option_rV_past[self.col_iv]=np.log(self.option[self.col_iv]/self.option[self.col_iv].shift(self.days_past))
        return self.format_output(option_rV_past)


    #当前交易日的波动率相比于过去n个交易日移动均值的差值
    def dV_past_mean(self):
        option_dV_past_mean = copy.deepcopy(self.option)
        option_dV_past_mean[self.col_iv] = self.option[self.col_iv]-self.option[self.col_iv].rolling(self.days_past).mean()
        return self.format_output(option_dV_past_mean)


    #当前交易日的波动率相比于过去n个交易日移动均值的差值百分比（%）
    def rV_past_mean(self):
        option_rV_past_mean = copy.deepcopy(self.option)
        option_rV_past_mean[self.col_iv] = np.log(self.option[self.col_iv]/self.option[self.col_iv].rolling(self.days_past).mean())
        return self.format_output(option_rV_past_mean)


    #当前交易日的波动率相比于过去n个交易日移动均值的差值（移动标准差个数）
    def dV_past_std(self):
        option_rV_past_mean = copy.deepcopy(self.option)
        option_rV_past_mean[self.col_iv] = (self.option[self.col_iv]-self.option[self.col_iv].rolling(self.days_past).mean())/self.option[self.col_iv].rolling(self.days_past).std()
        return self.format_output(option_rV_past_mean)


    #当前交易日的波动率相比于过去n个交易日移动最小值的差值
    def dV_past_min(self):
        option_dV_past_min = copy.deepcopy(self.option)
        option_dV_past_min[self.col_iv] = self.option[self.col_iv]-self.option[self.col_iv].rolling(self.days_past).min()
        return self.format_output(option_dV_past_min)


    #当前交易日的波动率相比于过去n个交易日移动最大值的差值
    def dV_past_max(self):
        option_dV_past_max = copy.deepcopy(self.option)
        option_dV_past_max[self.col_iv] = self.option[self.col_iv]-self.option[self.col_iv].rolling(self.days_past).max()
        return self.format_output(option_dV_past_max)


    #当前交易日的波动率相比于过去n个交易日移动最小值的差值百分比（%）
    def rV_past_min(self):
        option_rV_past_min = copy.deepcopy(self.option)
        option_rV_past_min[self.col_iv] = np.log(self.option[self.col_iv]/self.option[self.col_iv].rolling(self.days_past).min())
        return self.format_output(option_rV_past_min)


    #当前交易日的波动率相比于过去n个交易日移动最大值的差值百分比（%）
    def rV_past_max(self):
        option_rV_past_max = copy.deepcopy(self.option)
        option_rV_past_max[self.col_iv] = np.log(self.option[self.col_iv]/self.option[self.col_iv].rolling(self.days_past).max())
        return self.format_output(option_rV_past_max)


    #当前交易日的波动率超过过去n个交易日移动均值的k个移动标准差（哑元变量）
    def dummy_past_diff_higher_std(self,K=2):
        option_dummy_past_diff_higher_std = copy.deepcopy(self.option)
        std_roll=self.option[self.col_iv].rolling(self.days_past).std()
        mean_roll=self.option[self.col_iv].rolling(self.days_past).mean()
        option_dummy_past_diff_higher_std[self.col_iv] =(self.option[self.col_iv]-mean_roll>=K*std_roll)*1
        return self.format_output(option_dummy_past_diff_higher_std)


    #当前交易日的波动率低于过去n个交易日移动均值的k个移动标准差（哑元变量）
    def dummy_past_diff_lower_std(self,K=2):
        option_dummy_past_diff_lower_std = copy.deepcopy(self.option)
        std_roll=self.option[self.col_iv].rolling(self.days_past).std()
        mean_roll=self.option[self.col_iv].rolling(self.days_past).mean()
        option_dummy_past_diff_lower_std[self.col_iv] =(mean_roll-self.option[self.col_iv]>=K*std_roll)*1
        return self.format_output(option_dummy_past_diff_lower_std)
    
    
    #通过在列表中填入将使用的变量类型，计算相应的变量
    def varibles_type(self,
                      cols_varible_type=[],#所使用变量的类型
                                            #可选择范围  ['dV_past','rV_past','dV_past_mean','rV_past_mean','dV_past_std','dV_past_min','dV_past_max','rV_past_min','rV_past_max','dummy_past_diff_higher_std','dummy_past_diff_lower_std',]
                      
                      K=1,
                      ):
        
        VolatilityChange_s={}
        
        if 'dV_past' in cols_varible_type:
            VolatilityChange_s['dV_past']=self.dV_past()
        if 'rV_past' in cols_varible_type:
            VolatilityChange_s['rV_past'] = self.rV_past()
        if 'dV_past_mean' in cols_varible_type:
            VolatilityChange_s['dV_past_mean'] = self.dV_past_mean()
        if 'rV_past_mean' in cols_varible_type:
            VolatilityChange_s['rV_past_mean'] = self.rV_past_mean()
        if 'dV_past_std' in cols_varible_type:
            VolatilityChange_s['dV_past_std'] = self.dV_past_std()
        if 'dV_past_min' in cols_varible_type:
            VolatilityChange_s['dV_past_min'] = self.dV_past_min()
        if 'dV_past_max' in cols_varible_type:
            VolatilityChange_s['dV_past_max'] = self.dV_past_max()
        if 'rV_past_min' in cols_varible_type:
            VolatilityChange_s['rV_past_min'] = self.rV_past_min()
        if 'rV_past_max' in cols_varible_type:
            VolatilityChange_s['rV_past_max'] = self.rV_past_max()
        if 'dummy_past_diff_higher_std' in cols_varible_type:
            VolatilityChange_s['dummy_past_diff_higher_std'] = self.dummy_past_diff_higher_std(K=K)
        if 'dummy_past_diff_lower_std' in cols_varible_type:
            VolatilityChange_s['dummy_past_diff_lower_std'] = self.dummy_past_diff_lower_std(K=K)
            
        return VolatilityChange_s
    


    




if __name__=='__main__':
    #计算过去的波动率涨跌幅
    from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol

    # 获取指定格式的截面数据
    vol_cross = get_cross_vol(path_vol=PATH_VOL_SAMPLE, num_date=757, )
    DVCP = DefinitionVolatilityChangePast(option=vol_cross,col_iv=['AAPL','SPX'])
    DVCP.dV_past()
    DVCP.rV_past()
    DVCP.dV_past_mean()
    DVCP.rV_past_mean()
    DVCP.dV_past_std()
    DVCP.dV_past_min()
    DVCP.dV_past_max()
    DVCP.rV_past_min()
    DVCP.rV_past_max()
    DVCP.dummy_past_diff_higher_std(K=1)
    DVCP.dummy_past_diff_lower_std(K=1)

    # 获得指定个股的时间序列数据
    vol_series = get_series_vol(path_vol=PATH_VOL_SAMPLE, ticker='SPX', )
    DVCP=DefinitionVolatilityChangePast(option=vol_series)
    DVCP.dV_past()
    DVCP.rV_past()
    DVCP.dV_past_mean()
    DVCP.rV_past_mean()
    DVCP.dV_past_std()
    DVCP.dV_past_min()
    DVCP.dV_past_max()
    DVCP.rV_past_min()
    DVCP.rV_past_max()
    DVCP.dummy_past_diff_higher_std(K=1)
    DVCP.dummy_past_diff_lower_std(K=1)
























