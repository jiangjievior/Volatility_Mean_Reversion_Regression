from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


class RelationFutureAndPast():
    def __init__(self,
                 surface:pd.DataFrame,

                 ):
        self.surface=surface

    #计算未来n个交易日的波动率最值变化：当前波动率-波动率未来移动最值
    def change_future(self,
                      num_future:int,
                      category_future:int=1,
                      ):
        #类型1：计算该日波动率与波动率未来移动最值之间差值和收益率
        if category_future==1:
            # 计算未来n个交易日的波动率移动最值
            self.surface.sort_values('date', ascending=False, inplace=True)
            self.surface['min_windows_future'] = self.surface['impl_volatility'].rolling(num_future).min()
            self.surface['max_windows_future'] = self.surface['impl_volatility'].rolling(num_future).max()
            self.surface.sort_values('date', ascending=True, inplace=True)

            # 计算该日波动率与波动率移动最值之间差值和收益率
            self.surface['diff_min_windows_future'] = self.surface['min_windows_future'] - self.surface['impl_volatility']  # 该日波动率与波动率移动最小值之间差值
            self.surface['diff_max_windows_future'] = self.surface['max_windows_future'] - self.surface['impl_volatility']  # 波动率移动最大值与该日波动率之间差值
            self.surface['rate_min_windows_future'] = self.surface['diff_min_windows_future'] / self.surface['impl_volatility']  # 该日波动率与波动率移动最小值之间差值
            self.surface['rate_max_windows_future'] = self.surface['diff_max_windows_future'] / self.surface['impl_volatility']  # 波动率移动最大值与该日波动率之间差值



        pass

    #计算过去m个交易日的波动率最值变化：当前波动率-波动率未来移动最值
    def change_past(self,
                    num_past:int,
                    category_past:int=1,
                    ):
        # 类型1：计算该日波动率与波动率过去移动最值之间差值和收益率
        if category_past == 1:
            # 计算未来n个交易日的波动率移动最值
            self.surface['min_windows_past'] = self.surface['impl_volatility'].rolling(num_past).min()
            self.surface['max_windows_past'] = self.surface['impl_volatility'].rolling(num_past).max()

            # 计算该日波动率与波动率移动最值之间差值和收益率
            self.surface['diff_min_windows_past'] = self.surface['impl_volatility']-self.surface['min_windows_past']  # 该日波动率与波动率移动最小值之间差值
            self.surface['diff_max_windows_past'] = self.surface['impl_volatility']-self.surface['max_windows_past']  # 波动率移动最大值与该日波动率之间差值
            self.surface['rate_min_windows_past'] = self.surface['diff_min_windows_past'] / self.surface['min_windows_past']  # 该日波动率与波动率移动最小值之间差值
            self.surface['rate_max_windows_past'] = self.surface['diff_max_windows_past'] / self.surface['max_windows_past']  # 波动率移动最大值与该日波动率之间差值

        pass

    #用分组排序的方式研究组合值的差异
    def protfolios_sort(self,col_X,col_Y):
        self.surface[f'bin_{col_X}']=pd.qcut(self.surface[col_X],6)
        return pd.pivot_table(self.surface,index=[f'bin_{col_X}'],values=[col_Y])[col_Y]









    def run(self,
            num_past:int,
            num_future:int,
            category_future:int,
            category_past:int,
            ):
        self.surface.dropna(inplace=True)
        self.change_future(num_future=num_future, category_future=category_future)
        self.change_past(num_past=num_past, category_past=category_past)








if __name__=='__main__':
    #2.波动率的暴涨暴跌引起未来暴跌暴涨的概率
    #哑元回归：当波动率跌幅超过过去n个交易日的K倍移动标准差，波动率
    surface = pd.read_csv(PATH_VOL_SURFACE_SPX)
    surface_days_delta = surface[(surface['days'] == 30) & (surface['delta'] == -50)]
    surface_days_delta.index = range(len(surface_days_delta))
    RFAP = RelationFutureAndPast(surface=surface_days_delta, )
    RFAP.run(num_past=30, num_future=30,category_past=1,category_future=1)



















    #1.波动率的暴涨暴跌是否会引起未来暴跌暴涨
    surface = pd.read_csv(PATH_VOL_SURFACE_SPX)
    surface_days_delta = surface[(surface['days'] == 30) & (surface['delta'] == -50)]
    surface_days_delta.index = range(len(surface_days_delta))
    RFAP=RelationFutureAndPast(surface=surface_days_delta,)
    RFAP.run(num_past=30, num_future=30)
    # 波动率暴涨之后，未来是否有可能跌得更狠
    results_up = RFAP.protfolios_sort(col_X='rate_min_windows_past', col_Y='rate_min_windows_future')
    # 波动率暴跌之后，未来是否有可能涨得更狠
    results_down = RFAP.protfolios_sort(col_X='rate_max_windows_past', col_Y='rate_max_windows_future')

























