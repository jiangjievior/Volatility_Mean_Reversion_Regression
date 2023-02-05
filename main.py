# -*- coding:utf-8 -*-
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


########################################################################################################################
#获取个股期权隐含波动率的截面数据或时间序列数据
########################################################################################################################
# from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
#
# #获取指定格式的截面数据
# vol_cross=get_cross_vol(path_vol=PATH_VOL_SAMPLE,num_date=757,)
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
# result_cross=CDAVC.run_OLS(past_Distance=['rV_past_mean','rV_past_mean'],
#               future_VolChange=['rV_future_mean','rV_future'],
#               )
#
# result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)


#-------------------------------------------------------
#在计算 波动率变化 与 波动率和均值的距离 的窗口长度时，使用不同的交易日数量
#-------------------------------------------------------
# from 项目文件.模型拟合.拟合距离与波动率变化的关系 import CrossDistanceAndVolatilityChangeDifferentWindows
# from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross
#
# CDAVCDW=CrossDistanceAndVolatilityChangeDifferentWindows(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
#                                                          num_date=757,
#                                                          days_past_windows=[30,60,100],
#                                                          days_future_windows=[30,60,100],
#                                                          )
# result_cross=CDAVCDW.run_OLS(models=[['rV_past_mean','dV_past_std'],
#                                     ['rV_future_mean','dV_future_std']],
#                             )
#
# result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)

#-------------------------------------------------------
#依据财务特征，或其他特征划分数据组，并进行OLS拟合
#-------------------------------------------------------
from 项目文件.数据处理.获取指定个股的财务数据 import finance_ratio_stock
from 项目文件.模型拟合.拟合距离与波动率变化的关系 import CrossDistanceAndVolatilityChangeDifferentCharacters
from 项目文件.修改输出结果的格式.修改_拟合距离与波动率变化的关系_输出结果格式 import reformat_OLS_Distance_and_VolChange_cross

CDAVCDW=CrossDistanceAndVolatilityChangeDifferentCharacters(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                                                         num_date=757,
                                                         days_past=30,
                                                         days_future=30
                                                         )

#生成特征数据，用于将数据划分为不同小组合
col_Characters='bm'#特征名称
finance_ratio=finance_ratio_stock(
    tickers=CDAVCDW.option.columns,
    name_fin=[col_Characters],
    dates=CDAVCDW.option.index,)
finance_ratio=pd.pivot_table(finance_ratio,index=['date'],columns=['ticker'],values=[col_Characters])[col_Characters].T

#依据特征数据的分组排序结果，对各个小组进行拟合
q=5
CDAVCDW.sort_characters_date(character=finance_ratio,q=q,col_character=col_Characters,q_labels=np.arange(1, q + 1))

result_cross=CDAVCDW.run_OLS(models=[['rV_past_mean','dV_past_std'],
                                    ['rV_future_mean','dV_future_std']],
                            )

result_cross=reformat_OLS_Distance_and_VolChange_cross(result_cross)


















########################################################################################################################
#从时间序列数据的角度，拟合 波动率变化 与 波动率和均值的距离 之间的关系
########################################################################################################################
from 项目文件.模型拟合.拟合距离与波动率变化的关系 import SeriesDistanceAndVolatilityChange

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



























