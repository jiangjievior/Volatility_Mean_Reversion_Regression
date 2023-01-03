from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

#获得过去n个交易日的分位数超出点
def value_over_quantitle(
        surface:pd.DataFrame,#波动率曲面数据
        windows_quantitle:int=200,#用于计算移动分位数的窗口长度
        quantitle_up:list=[0.9,0.95,0.99],#高于该分位数的视为超出点
        quantitle_down:list=[0.01,0.05,0.1],#低于该分位数的视为超出点

):

    #计算移动分位数
    value_quantitle_s={}
    value_quantitle_s['date']=[]
    for quantitle_ in quantitle_up:value_quantitle_s[f'up_{quantitle_}']=[]
    for quantitle_ in quantitle_down: value_quantitle_s[f'down_{quantitle_}'] = []

    for i in range(windows_quantitle,len(surface)):
        date=surface.loc[i,'date']
        value_quantitle_s['date'].append(date)
        for quantitle_ in quantitle_up:
            quantitle=np.quantile(surface.loc[i-windows_quantitle:i,'impl_volatility'],quantitle_)
            value_quantitle_s[f'up_{quantitle_}'].append(quantitle)
        for quantitle_ in quantitle_down:
            quantitle=np.quantile(surface.loc[i-windows_quantitle:i,'impl_volatility'],quantitle_)
            value_quantitle_s[f'down_{quantitle_}'].append(quantitle)
        print(f'计算移动分位数已经完成{date}')
    value_quantitle_s=pd.DataFrame(value_quantitle_s)
    surface=pd.merge(surface,value_quantitle_s,on=['date'])
    
    #寻找超过移动分位数的异常值
    for quantitle_ in quantitle_up:
        surface[f'value_up_{quantitle_}']=(surface['impl_volatility']>=surface[f'up_{quantitle_}'])
        surface[f'value_up_{quantitle_}']=surface[f'value_up_{quantitle_}'].apply(lambda x:1 if x else np.nan)*surface['impl_volatility']
    for quantitle_ in quantitle_down:
        surface[f'value_down_{quantitle_}']=(surface['impl_volatility']<=surface[f'down_{quantitle_}'])
        surface[f'value_down_{quantitle_}']=surface[f'value_down_{quantitle_}'].apply(lambda x:1 if x else np.nan)*surface['impl_volatility']

    return surface








if __name__=='__main__':
    surface=pd.read_csv(PATH_VOL_SURFACE_SPX)
    surface_days_delta=surface[(surface['days']==30)&(surface['delta']==50)]
    surface_days_delta.index=range(len(surface_days_delta))
    surface_days_delta=value_over_quantitle(surface_days_delta,
                                            windows_quantitle=20,
                                            quantitle_up=[0.9,0.95,0.99],
                                            quantitle_down= [0.01, 0.05, 0.1],
                                            )
    
    

    #绘图
    date_start=201604070
    date_end=20190809
    surface_days_delta_date=surface_days_delta[(surface_days_delta['date']>=date_start)&(surface_days_delta['date']<=date_end)]
    plt.figure(figsize=(24,8))
    #surface_days_delta_date.index=surface_days_delta_date['date'].astype(str)
    plt.plot(surface_days_delta_date['impl_volatility'])
    plt.scatter(x=surface_days_delta_date.index, y=surface_days_delta_date['value_up_0.95'], color='r',
                linewidths=0.5)
    plt.scatter(x=surface_days_delta_date.index,y=surface_days_delta_date['value_down_0.01'],color='g',linewidths=0.5)
    plt.xticks(np.array(surface_days_delta_date.index)[[int(x) for x in np.linspace(0,len(surface_days_delta_date)-1,15)]])
123












































