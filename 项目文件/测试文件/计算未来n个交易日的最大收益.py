from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def compute_max_gains(
        surface:pd.DataFrame,
        windows:int=30,#移动窗口长度，交易日天数

        ):

    #计算未来n个交易日的波动率移动最值
    surface.sort_values('date',ascending=False,inplace=True)
    surface['min_windows']=surface['impl_volatility'].rolling(windows).min()
    surface['max_windows'] = surface['impl_volatility'].rolling(windows).max()
    surface.sort_values('date', ascending=True, inplace=True)

    surface
    #计算该日波动率与波动率移动最值之间差值和收益率
    surface['diff_min_windows']=surface['min_windows']-surface['impl_volatility']#该日波动率与波动率移动最小值之间差值
    surface['diff_max_windows']=surface['max_windows']-surface['impl_volatility']#波动率移动最大值与该日波动率之间差值
    surface['rate_min_windows']=surface['diff_min_windows']/surface['impl_volatility']#该日波动率与波动率移动最小值之间差值
    surface['rate_max_windows']=surface['diff_max_windows']/surface['impl_volatility']#波动率移动最大值与该日波动率之间差值






















if __name__=='__main__':
    surface = pd.read_csv(PATH_VOL_SURFACE_SPX)
    surface_days_delta = surface[(surface['days'] == 30) & (surface['delta'] == 50)]
    surface_days_delta.index = range(len(surface_days_delta))
    surface_days_delta = compute_max_gains(surface_days_delta,
                                              )










