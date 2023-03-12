# -*- coding:utf-8 -*-
from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

from 项目文件.修改输出结果的格式.修改_基于历史波动率不同的上涨幅度或下跌幅度的回归结果 import \
    reformat_regression_mean_reversion_different_volatility_change
from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复的概率_之间关系 import \
    volatility_multiple_dimension_probability_mean_reversion, describe_probability_volatility_MeanReversion
from 项目文件.绘图.绘制波动率均值回复概率图 import plot_probability_MeanReversion

########################################################################################################################
#临时修改代码，事后务必修改规正
########################################################################################################################
#from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol
#data = pd.read_csv(path_vol,usecols=usecols,skiprows=12490950) 额外增加 ,skiprows=12490950



########################################################################################################################
#描述性统计分析
########################################################################################################################

#-------------------------------------------------------
#对期权样本的描述性统计分析
#-------------------------------------------------------
# from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
#
# for path_vol in PATH_VOL_S:
#     vol_cross = get_cross_vol(path_vol=PATH_VOL_S[path_vol])
#     vol_cross
#     # #
#     # vol = pd.read_csv(PATH_VOL_S[path_vol])
#
#     #统计历年可交易股票个数
#     vol_cross


########################################################################################################################
#获取个股期权隐含波动率的截面数据或时间序列数据
########################################################################################################################
# from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
#
# #获取指定格式的截面数据
# vol_cross=get_cross_vol(path_vol=PATH_VOL_S['put&delta50&days30'])
#
# #获得指定个股的时间序列数据
# vol_series=get_series_vol(path_vol=PATH_VOL_SAMPLE,ticker='SPX',)


########################################################################################################################
#计算过去波动率涨跌幅度
########################################################################################################################
# # 计算过去的波动率涨跌幅
# from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
# from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
#
#
# # 获取指定格式的截面数据
# vol_cross = get_cross_vol(path_vol=PATH_VOL_SAMPLE, num_date=757, )
# DVCP = DefinitionVolatilityChangePast(option=vol_cross, col_iv=['AAPL', 'SPX'])
# DVCP.dV_past()
# DVCP.rV_past()
# DVCP.dV_past_mean()
# DVCP.rV_past_mean()
# DVCP.dV_past_std()
# DVCP.dV_past_min()
# DVCP.dV_past_max()
# DVCP.rV_past_min()
# DVCP.rV_past_max()
# DVCP.dummy_past_diff_higher_std(K=1)
# DVCP.dummy_past_diff_lower_std(K=1)
#
# # 获得指定个股的时间序列数据
# vol_series = get_series_vol(path_vol=PATH_VOL_SAMPLE, ticker='SPX', )
# DVCP = DefinitionVolatilityChangePast(option=vol_series)
# DVCP.dV_past()
# rV_past=DVCP.rV_past()
# DVCP.dV_past_mean()
# DVCP.rV_past_mean()
# DVCP.dV_past_std()
# DVCP.dV_past_min()
# DVCP.dV_past_max()
# DVCP.rV_past_min()
# DVCP.rV_past_max()
# DVCP.dummy_past_diff_higher_std(K=1)
# DVCP.dummy_past_diff_lower_std(K=1)


########################################################################################################################
#计算未来波动率涨跌幅度
########################################################################################################################
# # 计算未来的波动率涨跌幅
# from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
# from 项目文件.定义公用变量.计算未来波动率涨跌幅度 import DefinitionVolatilityChangeFuture
#
# # 获取指定格式的截面数据
# vol_cross = get_cross_vol(path_vol=PATH_VOL_SAMPLE, num_date=757, )
# DVCP = DefinitionVolatilityChangeFuture(option=vol_cross, col_iv=['AAPL', 'SPX'])
# DVCP.dV_future()
# DVCP.rV_future()
# DVCP.dV_future_mean()
# DVCP.rV_future_mean()
# DVCP.dV_future_std()
# DVCP.dV_future_min()
# DVCP.dV_future_max()
# DVCP.rV_future_min()
# DVCP.rV_future_max()
# DVCP.dummy_future_diff_higher_std(K=1)
# DVCP.dummy_future_diff_lower_std(K=1)
#
# # 获得指定个股的时间序列数据
# vol_series = get_series_vol(path_vol=PATH_VOL_SAMPLE, ticker='SPX', )
# DVCP = DefinitionVolatilityChangeFuture(option=vol_series)
# DVCP.dV_future()
# DVCP.rV_future()
# DVCP.dV_future_mean()
# DVCP.rV_future_mean()
# DVCP.dV_future_std()
# DVCP.dV_future_min()
# DVCP.dV_future_max()
# DVCP.rV_future_min()
# DVCP.rV_future_max()
# DVCP.dummy_future_diff_higher_std(K=1)
# DVCP.dummy_future_diff_lower_std(K=1)

########################################################################################################################
#从截面数据的角度，拟合 波动率变化 与 波动率和均值的距离 之间的关系，并返回 每个交易日的拟合结果 及 总体结果的描述性统计分析
########################################################################################################################
# from 项目文件.模型拟合.拟合距离与波动率变化的关系 import CrossDistanceAndVolatilityChange
# from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross
#
# CDAVC=CrossDistanceAndVolatilityChange(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE, num_date=757)
# result_cross=CDAVC.run_OLS(models=[['rV_past_mean','dV_past_std'],
#                         ['rV_future_mean','dV_future_std']]
#               )
#
# result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)


#-------------------------------------------------------
#在计算 波动率变化 与 波动率和均值的距离 的窗口长度时，使用不同的交易日数量
#-------------------------------------------------------
# from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复_的关系 import CrossDistanceAndVolatilityChangeDifferentWindows
# from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross
#
# CDAVCDW=CrossDistanceAndVolatilityChangeDifferentWindows(PATH_VOL_SAMPLE=PATH_VOL_S['put&delta50&days30'],
#                                                          days_past_windows=[30,60,100,30,60,100,30,60,100],
#                                                          days_future_windows=[5,5,5,30,30,30,60,60,60],
#                                                          )
#
# result_s,result_cross=CDAVCDW.run_OLS(models=[['rV_past_mean'],
#                                     ['dV_future_min']],
#                             )
#
# result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)

#-------------------------------------------------------
#在计算 波动率变化 与 波动率和均值的距离 的窗口长度时，使用不同的交易日数量
#-------------------------------------------------------
# from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复_的关系 import CrossDistanceAndVolatilityChangeDifferentWindows
# from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross
#
# result_s_s={}
# result_cross_s={}
# for path_vol in PATH_VOL_S.keys():
#     try:
#         CDAVCDW=CrossDistanceAndVolatilityChangeDifferentWindows(PATH_VOL_SAMPLE=PATH_VOL_S[path_vol],
#                                                                  days_past_windows=[30,60,100,30,60,100,30,60,100],
#                                                                  days_future_windows=[5,5,5,30,30,30,60,60,60],
#                                                                  )
#
#         result_s,result_cross=CDAVCDW.run_OLS(models=[['rV_past_mean','rV_past_mean'],
#                                             ['dV_future_min','dV_future']],
#                                     )
#
#         result_s_s[path_vol]=result_s
#         result_cross_s[path_vol]=result_cross
#     except:
#         continue
#
# result_cross_s
# result_s_s

#-------------------------------------------------------
#基于历史波动率不同的上涨幅度或下跌幅度，在不同的过去未来窗口上，波动率均值回复特征回归结果
#-------------------------------------------------------
from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复_的关系 import MeanReversionRegressionDifferentWindowsDifferentVolatilityChange
from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复的概率_之间关系 import \
    volatility_multiple_dimension_probability_mean_reversion, describe_probability_volatility_MeanReversion
from 项目文件.绘图.绘制波动率均值回复概率图 import plot_probability_MeanReversion

MRRDWD=MeanReversionRegressionDifferentWindowsDifferentVolatilityChange(
                 PATH_VOL_S,
                 models=[['rV_past_mean'],
                         ['rV_future']],
                 days_past_windows=[30,60,100],#各种过去变量的滑动窗口长度
                 days_future_windows=[30,60,100],#各种未来变量的滑动窗口长度
                 )

MRRDWD.node(data=np.random.random(size=2000),
            type='quant_q',
            num=5
            )


MRRDWD.run_OLS(path_save='数据文件\生成数据\均值回复回归'+'\不同涨跌幅下的均值回复回归结果.csv')

#CP:put》delta》days:30》col_past:rV_past_mean》days_past》days_future》date》down:up》node》params
reformat_regression_mean_reversion_different_volatility_change()


#-------------------------------------------------------
#依据财务特征，或其他特征划分数据组，并进行OLS拟合
#-------------------------------------------------------
# from 项目文件.数据处理.获取指定个股的财务数据 import finance_ratio_stock
# from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复_的关系 import CrossDistanceAndVolatilityChangeDifferentCharacters
# from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross
#
#
# CDAVCDW=CrossDistanceAndVolatilityChangeDifferentCharacters(PATH_VOL_SAMPLE=PATH_VOL_main,
#                                                          days_past=30,
#                                                          days_future=3
#                                                          )
# #生成特征数据，用于将数据划分为不同小组合
# #依据特征数据的分组排序结果，对各个小组进行拟合
# CDAVCDW.sort_options_according_charactes(col_Characters='roe',#特征名称
#                              q=5#分组数
#                              )
# result_cross=CDAVCDW.run_OLS(models=[['rV_past_mean'],
#                                     ['rV_future']],
#                             )
#
# result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)


########################################################################################################################
#从截面数据的角度，拟合 过去波动率变化 与 未来波动率回复的概率 之间的关系，并返回 每个交易日的拟合结果 及 总体结果的描述性统计分析
########################################################################################################################

#-------------------------------------------------------
# 波动率均值回复多维概率统计表
# 在值程度的数据《过去窗口《过去变量《过去涨幅(%)《未来窗口《未来变量《未来跌幅(%)《交易日《均值回复概率
#-------------------------------------------------------

# volatility_multiple_dimension_probability_mean_reversion(
#         PATH_VOL_S=PATH_VOL_S,  # 文件路径
#
#         windows_past=[15, 30, 60, 90],  # 过去窗口
#         windows_future=[15, 30, 60, 90],  # 未来窗口
#
#         cols_past=['rV_past_mean', 'dV_past_mean'],  # 过去变量
#         cols_future=['rV_future', 'dV_future'],  # 未来变量
#
#         volatility_change_past=[0.1, 0.3, 0.5],  # 过去涨幅(%)
#         volatility_change_future=[-0.1, -0.3, -0.5],  # 未来跌幅(%)
#
#         path_save=os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\均值回复概率',
#                                '多维均值回复概率表.csv')
# )
#
describe_probability_volatility_MeanReversion(
    path_results=data_real_path('数据文件/生成数据/均值回复概率/多维均值回复概率表.csv'),
    path_save=data_real_path('数据文件/生成数据/均值回复概率')+'/多维均值回复概率表数据透视.xlsx'
)

#-------------------------------------------------------
#绘制波动率均值回复概率分布图
#30天的delta50看跌期权波动率》过去变量'rV_past_mean'》过去窗口60天》过去波动率涨幅（5%~60%）》未来变量'dV_future'》
#未来窗口（15天、30天、60天）》未来波动率跌幅（-5%~-60%）
#-------------------------------------------------------
volatility_multiple_dimension_probability_mean_reversion(
        PATH_VOL_S={'put&delta50&days30':'H:\\美国个股期权隐含波动率曲面\\put&delta50&days30.csv'},  # 文件路径

        windows_past=[15, 30, 60, 90],  # 过去窗口
        windows_future=[15, 30, 60, 90],  # 未来窗口

        cols_past=['rV_past_mean', 'dV_past_mean'],  # 过去变量
        cols_future=['rV_future', 'dV_future'],  # 未来变量

        volatility_change_past=np.arange(0.05,0.6,0.05),  # 过去涨幅(%)
        volatility_change_future=-np.arange(0.05,0.3,0.05),  # 未来跌幅(%)

        path_save=os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\均值回复概率',
                               '多维均值回复概率表绘图版2.csv')
)

plot_probability_MeanReversion(
        results=pd.read_csv('数据文件/生成数据/均值回复概率/多维均值回复概率表绘图版2.csv'),
        volatility_change_past=np.arange(0.05,0.6,0.05),  # 过去涨幅(%)
        volatility_change_future=-np.arange(0.05,0.3,0.05),  # 未来跌幅(%)
        pig_save=f'数据文件/生成数据/均值回复概率/多维均值回复概率表.png',
        )

pass









########################################################################################################################
#从时间序列数据的角度，拟合 波动率变化 与 波动率和均值的距离 之间的关系
########################################################################################################################
# from 项目文件.模型拟合.拟合距离与波动率变化的关系 import SeriesDistanceAndVolatilityChange
#
#SDAVC=SeriesDistanceAndVolatilityChange()




########################################################################################################################
#获取指定个股的财务数据
########################################################################################################################
from 项目文件.数据处理.获取指定个股的财务数据 import finance_ratio_stock
finance_ratio_stock()








option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=400000)
under=pd.read_csv(PATH_UNDER)

i=0
for data in option:
    #data=data[data['date']>20100101]
    # data['days'] = pd.to_datetime(data['exdate'], format='%Y%m%d') - pd.to_datetime(data['date'],
    #                                                                                           format='%Y%m%d')
    # data['days']
    i+=1



























