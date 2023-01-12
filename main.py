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
#获取指定个股的财务数据
########################################################################################################################
from 项目文件.数据处理.获取指定个股的财务数据 import get_finance_compy
get_finance_compy()








option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=400000)
under=pd.read_csv(PATH_UNDER)

i=0
for data in option:
    #data=data[data['date']>20100101]
    # data['days'] = pd.to_datetime(data['exdate'], format='%Y%m%d') - pd.to_datetime(data['date'],
    #                                                                                           format='%Y%m%d')
    # data['days']
    i+=1



























