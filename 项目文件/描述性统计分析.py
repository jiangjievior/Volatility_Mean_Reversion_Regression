import pandas as pd
import numpy as np
import os

from 数据文件.基本参数 import PATH_VOL_main




results=pd.read_excel("H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\均值回复基本回归结果.xlsx")
results
results.rename(columns={'X':'Y','Y':'X','windows_X':'windows_Y','windows_Y':'windows_X'},inplace=True)



results_dV_future=pd.pivot_table(results[(results['term']=='mean')&(results['Y']=='dV_future')],
               columns=['delta'],
               index=['windows_X','windows_Y'],
               values=['系数','系数t值']
               ).round(4)
results_dV_future=results_dV_future.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数',:]].round(4).astype(str)+'('+results_dV_future.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数t值',:]].round(4).astype(str).values+')'
results_dV_future=results_dV_future.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数',:]]
results_dV_future.to_excel("H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\dV_future基本回归结果.xlsx")

results_dV_future.to_excel("H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\dV_future基本回归结果.xlsx")


results_dV_future_min=pd.pivot_table(results[(results['term']=='mean')&(results['Y']=='dV_future_min')],
               columns=['delta'],
               index=['windows_X','windows_Y'],
               values=['系数','系数t值']
               ).round(4)
results_dV_future_min=results_dV_future_min.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数',:]].round(4).astype(str)+'('+results_dV_future_min.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数t值',:]].round(4).astype(str).values+')'
results_dV_future_min=results_dV_future_min.loc[pd.IndexSlice[:,:],pd.IndexSlice['系数',:]]
results_dV_future_min.to_excel("H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\dV_future_min基本回归结果.xlsx")

k=4














data=pd.read_csv(PATH_VOL_main,usecols=['date', 'days', 'delta', 'impl_volatility','cusip','ticker'])
data=data.loc[data['cusip']!='99999999',:]
# data=data.loc[data['cusip']!='99999999',:]





#
# data=data.loc[data['date']>=20170101,:]


# 每个股期权的交易个数,并筛选出符合适合数量的样本
size_individual = pd.pivot_table(data, index='cusip', values='date', aggfunc=np.size)
size_individual.sort_values(by='date', inplace=True, ascending=False)
size_individual=size_individual[size_individual>=360]
size_individual.dropna(inplace=True)

data = data[data['cusip'].astype(str).apply(lambda x: x in size_individual.index)]
vol_individual_pivot = pd.pivot_table(data, index=['date'], columns=['cusip'], values=['impl_volatility'],dropna=False)[
    'impl_volatility']
vol_individual_pivot = vol_individual_pivot.T.dropna().T


#逐年遍历每年的期权数据
data_last_year=None
year_start=1996
year_last=2021
for volatility_ in volatility:
    volatility_.columns

    if data_last_year is not None:
        volatility_=data_last_year.append(volatility_)
        volatility_.reset_index(inplace=True)

    year_end=str(volatility_.loc[len(volatility_)-1,'date'])[:4]
    years=np.arange(int(year_start),int(year_end))
    year_start=year_end
    data_last_year=volatility_.loc[volatility_['date'].astype(str).str[:4]==year_end,:]






















































