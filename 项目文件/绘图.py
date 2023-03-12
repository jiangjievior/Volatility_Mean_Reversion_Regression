import os.path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import PATH_VOL_SAMPLE, PATH_VOL_S
from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复_的关系 import CrossDistanceAndVolatilityChangeDifferentCharacters


plt.rcParams['font.sans-serif']=['simhei']#用于正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用于正常显示负号


#绘制概率密度图
def plt_dist(
            data = np.random.chisquare(14, 8000),#构造服从卡方分布的随机数据
            path_save='H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\生成图片\波动率变化的概率密度图.png',
            xlabel='Change of Volatility',
            ylabel='Frequency',

):
    plt.figure(figsize=(10,8))
    ax=sns.distplot(data, bins=100, kde=True, color='b', hist_kws={"linewidth": 15, 'alpha': 0.2})#将数据分为100组，绘制概率分布图，kde=True可以绘制出概率密度曲线
    ax.set(xlabel=ylabel, ylabel=xlabel)
    plt.text(1.5,1.5,
             f'skew:{pd.DataFrame(data).skew().round(3).values[0]}\nkurt:{pd.DataFrame(data).kurt().round(3).values[0]}',
             fontsize=15
             )

    #plt.legend(loc='upper right', fontsize='small')
    plt.savefig(path_save)



#绘制波动率上涨后，下跌幅度的概率密度分布图
#计算过去的波动率涨跌幅
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol

# 获取指定格式的截面数据
CDAVCDW=CrossDistanceAndVolatilityChangeDifferentCharacters(PATH_VOL_SAMPLE=PATH_VOL_S['put&delta50&days30'],
                                                         num_date=757,
                                                         days_past=30,
                                                         days_future=30
                                                         )

# 依据要求计算定义的变量
models=['rV_past_mean','rV_future']
varibles_future = CDAVCDW.define_varibles_future.varibles_type(cols_varible_type=models[1])
varibles_past = CDAVCDW.define_varibles_past.varibles_type(cols_varible_type=models[0])

data_X = varibles_past[models[0]]
data_Y = varibles_future[models[1]]

#对二者日期取交集，从而保留下来X和Y的共有数据
set_date=list(set(data_X.index).intersection(set(data_Y.index)))
data_X=data_X.loc[set_date,:]
data_Y = data_Y.loc[set_date, :]


#1.绘制所有波动率变化的概率密度图
# values_all=[]
# for col in data_Y.columns:
#     values_all=values_all+data_Y[col].tolist()
# plt_dist(values_all,
#          path_save='H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\生成图片\波动率变化的概率密度图.png',
#          xlabel='Frequency',
#          ylabel='Change of Volatility'
#          )


#2.绘制波动率下跌后的概率密度图
# positive_change_volatility=[]
# for col in data_X.columns:
#     X_positive=data_X[col][data_X[col]>0]
#     positive_change_volatility+=data_Y.loc[X_positive.index,col].tolist()
#
# plt_dist(data=positive_change_volatility,
#          path_save='H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\生成图片\波动率上升0后的未来波动率变化概率密度图.png',
#          xlabel='Frequency',
#          ylabel='Change of Volatility after Increasing 0'
#          )
#
#
# positive_change_volatility=[]
# for col in data_X.columns:
#     X_positive=data_X[col][data_X[col]>0.3]
#     positive_change_volatility+=data_Y.loc[X_positive.index,col].tolist()
#
# plt_dist(data=positive_change_volatility,
#          path_save='H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\生成图片\波动率上升0_3后的未来波动率变化概率密度图.png',
#          xlabel='Frequency',
#          ylabel='Change of Volatility after Increasing 0.3'
#          )
#
#
# positive_change_volatility=[]
# for col in data_X.columns:
#     X_positive=data_X[col][data_X[col]>0.6]
#     positive_change_volatility+=data_Y.loc[X_positive.index,col].tolist()
#
# plt_dist(data=positive_change_volatility,
#          path_save='H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\生成图片\波动率上升0_6后的未来波动率变化概率密度图.png',
#          xlabel='Frequency',
#          ylabel='Change of Volatility after Increasing 0.6'
#          )

#3.绘制不同交易日跨期的 过去波动率上涨幅度 与 未来波动率下跌幅度概率密度分布 之间的曲线关系

results=[]
for base_line in np.arange(0,1,step=0.01):
    positive_change_volatility=[]
    for col in data_X.columns:
        X_positive=data_X[col][data_X[col]>base_line]
        positive_change_volatility+=data_Y.loc[X_positive.index,col].tolist()
    positive_change_volatility=pd.DataFrame(positive_change_volatility)
    results.append([base_line,
                    positive_change_volatility.mean().values[0],
                    positive_change_volatility.std().values[0],
                    positive_change_volatility.skew().values[0],
                    positive_change_volatility.kurt().values[0],
                    ])

results=pd.DataFrame(results,columns=['crireion','mean','std','skew','kurt'])
results.index=results['crireion']
results.drop('crireion',axis=1,inplace=True)
results.round(3).to_csv('H:\python项目\Volatility_Mean_Reversion_Regression\数据文件\生成数据\概率预测\过去波动率的不同上涨幅度所对应的未来波动率变化分布.csv',encoding='utf_8_sig')


results[['mean','std','skew']].plot(grid=True)








