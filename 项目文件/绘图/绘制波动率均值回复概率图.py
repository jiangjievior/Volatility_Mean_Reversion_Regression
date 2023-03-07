import os

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import pandas as pd

from 数据文件.基本参数 import PATH_VOL_S
from 项目文件.定义公用变量.计算未来波动率涨跌幅度 import DefinitionVolatilityChangeFuture
from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol
from 项目文件.模型拟合.过去波动率变化_与_未来波动率回复的概率_之间关系 import \
    volatility_multiple_dimension_probability_mean_reversion



#绘制均值回复概率分布图
def plot_probability_MeanReversion(
        results,
        volatility_change_past=[0.1, 0.3, 0.5],  # 过去涨幅(%)
        volatility_change_future=[-0.1, -0.3, -0.5],  # 未来跌幅(%)
        pig_save='',
        ):

    plt.figure(figsize=(12,8))
    fig, (ax1, ax2,ax3) = plt.subplots(nrows=3)

    for  window_future,ax in zip([15,30,60],[ax1,ax2,ax3]):
        x = results[results['window_future']==window_future]['volatility_change_past']
        y = results[results['window_future']==window_future]['volatility_change_future']
        z =results[results['window_future']==window_future]['probability']

        xi = volatility_change_past
        yi = volatility_change_future

        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = interpolator(Xi, Yi)

        ax.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
        cntr1 = ax.contourf(xi, yi, zi, levels=14, cmap="RdBu_r")
        fig.colorbar(cntr1, ax=ax)
        ax.plot(x, y, 'ko', ms=1)
        ax.set_ylabel(f'FutureChange{window_future}')
        ax.set(xlim=(min(volatility_change_past), max(volatility_change_past)), ylim=(min(volatility_change_future), max(volatility_change_future)))

    ax3.set_xlabel('PastChange')
    plt.show()
    plt.savefig(pig_save)
















pass









