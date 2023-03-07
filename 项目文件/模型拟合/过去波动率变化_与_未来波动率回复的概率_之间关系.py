# -*- coding:utf-8 -*-
import os.path
import os
import pandas as pd
import numpy as np
import copy

from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path


from pandas import DataFrame

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 数据文件.基本参数 import *
from 项目文件.数据处理.获取指定个股的财务数据 import finance_ratio_stock
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
from 项目文件.定义公用变量.计算未来波动率涨跌幅度 import DefinitionVolatilityChangeFuture


#在值程度的数据《过去窗口《过去变量《过去涨幅(%)《未来窗口《未来变量《未来跌幅(%)《交易日《均值回复概率
# windows_past=[15,30,60,90]
# windows_future=[15,30,60,90]
#
# cols_past=['rV_past_mean','dV_past_mean']
# cols_future=['rV_future','dV_future']
#
# volatility_change_past=[0.1,0.3,0.5]
# volatility_change_future=[-0.1,-0.3,-0.5]
#
# results=[]
# results_dates= {}
# path_save=os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\均值回复概率','多维均值回复概率表.csv')
#

#波动率均值回复多维概率统计表
#在值程度的数据《过去窗口《过去变量《过去涨幅(%)《未来窗口《未来变量《未来跌幅(%)《交易日《均值回复概率
def volatility_multiple_dimension_probability_mean_reversion(
        PATH_VOL_S=PATH_VOL_S,#文件路径

        windows_past=[15,30,60,90],#过去窗口
        windows_future=[15,30,60,90],#未来窗口

        cols_past=['rV_past_mean','dV_past_mean'],#过去变量
        cols_future=['rV_future','dV_future'],#未来变量

        volatility_change_past=[0.1,0.3,0.5],#过去涨幅(%)
        volatility_change_future=[-0.1,-0.3,-0.5],#未来跌幅(%)

        path_save=os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\均值回复概率','多维均值回复概率表.csv'),

        ):
    results = []
    results_dates = {}

    i=1#组合序号
    for key in PATH_VOL_S.keys():
        put_call = key.split('&')[0]
        delta = int(key.split('&')[1][-2:])
        days_to_maturity = int(key.split('&')[2][-2:])


        vol=get_cross_vol(PATH_VOL_S[key])
        #vol = get_cross_vol(PATH_VOL_SAMPLE)
        for window_past in windows_past:
            window_past

            DVCP= DefinitionVolatilityChangePast(option=vol, col_iv=vol.columns,
                                                                       days_past=window_past)
            for col_past in cols_past:
                rV_past_mean=DVCP.varibles_type(cols_varible_type=[col_past])[col_past]

                for volatility_change_past_ in volatility_change_past:

                    for window_future in windows_future:
                        DVCF = DefinitionVolatilityChangeFuture(option=vol, col_iv=vol.columns,
                                                              days_future=window_future)

                        for col_future in cols_future:
                            rV_future = DVCF.varibles_type(cols_varible_type=[col_future])[col_future]

                            for volatility_change_future_ in volatility_change_future:

                                #过去波动率涨幅高于某个值的样本
                                past=(rV_past_mean>volatility_change_past_)
                                #未来波动率高于某个值的样本
                                future=(rV_future<volatility_change_future_)
                                #在过去波动率涨幅高于某个值的前提下，未来波动率高于某个值的样本
                                results_condition=past*future
                                #统计每个交易日发生概率
                                probability_date=results_condition.sum(axis=1)/past.sum(axis=1)
                                #统计总共发生概率
                                probability_total=sum(sum(results_condition.values))/sum(sum(past.values))

                                results.append([i,put_call,delta,days_to_maturity,window_past,col_past,volatility_change_past_,
                                                window_future,col_future,volatility_change_future_,probability_total
                                                ])
                                print([i,put_call,delta,days_to_maturity,window_past,col_past,volatility_change_past_,
                                                window_future,col_future,volatility_change_future_,probability_total
                                                ])
                                results_dates[i]=probability_date

                                i+=1


    result=pd.DataFrame(results,
                         columns=['i','pc','delta','days','window_past','col_past','volatility_change_past',
                                                'window_future','col_future','volatility_change_future','probability']
                         )
    result.to_csv(path_save,encoding='utf_8_sig',index=False)


#对上述生成的多维统计表进行整理分析
def describe_probability_volatility_MeanReversion(
        path_results=data_real_path('数据文件/生成数据/均值回复概率/多维均值回复概率表.csv'),
        path_save=data_real_path('数据文件/生成数据/均值回复概率')+'/多维均值回复概率表数据透视.xlsx',
):
    result=pd.read_csv(path_results)
    result=result[(result['col_future']=='rV_future')&(result['window_past']==60)]



    result=pd.pivot_table(result,index=['window_future','volatility_change_past'],columns=['delta','volatility_change_future'],values=['probability'])['probability']
    result=result.loc[pd.IndexSlice[:,:],pd.IndexSlice[[10,50,90],:]].round(3)
    result.to_excel(path_save)










pass






















































































