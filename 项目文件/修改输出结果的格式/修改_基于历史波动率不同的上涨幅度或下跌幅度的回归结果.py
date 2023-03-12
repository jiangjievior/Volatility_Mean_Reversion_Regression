import pandas as pd
import numpy as np
import os

from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path


def reformat_regression_mean_reversion_different_volatility_change():
    results=pd.read_csv(data_real_path('数据文件/生成数据/均值回复回归/不同涨跌幅下的均值回复回归结果.csv'))
    results

    #CP:put》delta》days:30》col_past:rV_past_mean》days_past》days_future》date》down:up》node》params
    results_1=results[results['down']=='up']
    t_s=pd.pivot_table(results_1,columns=['delta'],index=['days_future','node'],values=['t'])['t'].round(3).astype(str)
    param_s=pd.pivot_table(results_1,columns=['delta'],index=['days_future','node'],values=['params'])['params'].round(3).astype(str)
    param_s=param_s+'('+t_s+')'
    param_s.to_excel(data_real_path('数据文件/生成数据/均值回复回归')+'/不同涨跌幅下的均值回复回归结果数据透视表1.xlsx')



    #不同时期的回归结果

    results_2 = results[(results['down'] == 'up')&(results['days_past'] ==30)]

    #切分不同的时间段
    def periods(date):
        if str(date)[:4]=='2008':
            return '2008'
        elif str(date)[:4]=='2012':
            return '2012'
        elif str(date)[:4]=='2015':
            return '2015'
        else:
            return 'other'

    results_2['periods']=results_2['date'].apply(lambda x:periods(x))










    t_s = pd.pivot_table(results_2, columns=['delta'], index=['periods', 'node'], values=['t'])['t'].round(
        3).astype(str)
    param_s = pd.pivot_table(results_2, columns=['delta'], index=['periods', 'node'], values=['params'])[
        'params'].round(3).astype(str)
    param_s = param_s + '(' + t_s + ')'
    param_s.to_excel(
        data_real_path('数据文件/生成数据/均值回复回归') + '/不同涨跌幅下的均值回复回归结果数据透视表2.xlsx')









    #绘图
    #CP: put》delta》days: 30》col_past: rV_past_mean》days_past:30》days_future:30》date》down: up》node》params

    results_2 = results[(results['down'] == 'up')&(results['days_past'] ==30)&(results['node'] ==0.3)]
    # t_s = pd.pivot_table(results_2, columns=['delta'], index=['days_future', 'node'], values=['t'])['t'].round(
    #     3).astype(str)
    param_s = pd.pivot_table(results_2, columns=['delta'], index=['date'], values=['params'])[
        'params']

















