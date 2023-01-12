import pandas as pd
import numpy as np
import copy

from pandas import DataFrame

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 数据文件.基本参数 import PATH_VOL_SAMPLE
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
from 项目文件.定义公用变量.计算未来波动率涨跌幅度 import DefinitionVolatilityChangeFuture

#获取指定格式的截面数据
vol_cross=get_cross_vol(path_vol=PATH_VOL_SAMPLE,num_date=757,)

# 获取指定格式的截面数据
DVCP = DefinitionVolatilityChangePast(option=vol_cross, col_iv=list(vol_cross.columns))
dV_past=DVCP.dV_past()
rV_past=DVCP.rV_past()
dV_past_mean=DVCP.dV_past_mean()
rV_past_mean=DVCP.rV_past_mean()
dV_past_std=DVCP.dV_past_std()
dV_past_min=DVCP.dV_past_min()
dV_past_max=DVCP.dV_past_max()
rV_past_min=DVCP.rV_past_min()
rV_past_max=DVCP.rV_past_max()
dummy_past_diff_higher_std=DVCP.dummy_past_diff_higher_std(K=1)
dummy_past_diff_lower_std=DVCP.dummy_past_diff_lower_std(K=1)


# 获得指定个股的时间序列数据
DVCP = DefinitionVolatilityChangeFuture(option=vol_cross, col_iv=list(vol_cross.columns))
dV_future=DVCP.dV_future()
rV_future=DVCP.rV_future()
dV_future_mean=DVCP.dV_future_mean()
rV_future_mean=DVCP.rV_future_mean()
dV_future_std=DVCP.dV_future_std()
dV_future_min=DVCP.dV_future_min()
dV_future_max=DVCP.dV_future_max()
rV_future_min=DVCP.rV_future_min()
rV_future_max=DVCP.rV_future_max()
dummy_future_diff_higher_std=DVCP.dummy_future_diff_higher_std(K=1)
dummy_future_diff_lower_std=DVCP.dummy_future_diff_lower_std(K=1)


rV_future_mean
rV_past_mean

data: DataFrame=pd.DataFrame(
    {
        'X':rV_past_mean.T[20200108],
        'Y':rV_future_mean.T[20200108],
    }
)














#获得指定个股的时间序列数据
vol_series=get_series_vol(path_vol=PATH_VOL_SAMPLE,ticker='SPX',)

# 计算过去的波动率涨跌幅
DVCP = DefinitionVolatilityChangePast(option=vol_series)
dV_past=DVCP.dV_past()
rV_past=DVCP.rV_past()
dV_past_mean=DVCP.dV_past_mean()
rV_past_mean=DVCP.rV_past_mean()
dV_past_std=DVCP.dV_past_std()
dV_past_min=DVCP.dV_past_min()
dV_past_max=DVCP.dV_past_max()
rV_past_min=DVCP.rV_past_min()
rV_past_max=DVCP.rV_past_max()
dummy_past_diff_higher_std=DVCP.dummy_past_diff_higher_std(K=1)
dummy_past_diff_lower_std=DVCP.dummy_past_diff_lower_std(K=1)


# 计算未来的波动率涨跌幅
vol_series = get_series_vol(path_vol=PATH_VOL_SAMPLE, ticker='SPX', )
DVCP = DefinitionVolatilityChangeFuture(option=vol_series)
dV_future=DVCP.dV_future()
rV_future=DVCP.rV_future()
dV_future_mean=DVCP.dV_future_mean()
rV_future_mean=DVCP.rV_future_mean()
dV_future_std=DVCP.dV_future_std()
dV_future_min=DVCP.dV_future_min()
dV_future_max=DVCP.dV_future_max()
rV_future_min=DVCP.rV_future_min()
rV_future_max=DVCP.rV_future_max()
dummy_future_diff_higher_std=DVCP.dummy_future_diff_higher_std(K=1)
dummy_future_diff_lower_std=DVCP.dummy_future_diff_lower_std(K=1)


rV_past_mean
rV_future_mean


data=pd.merge(rV_past_mean[['date','impl_volatility']].rename(columns={'impl_volatility':'X'}),
         rV_future_mean[['date','impl_volatility']].rename(columns={'impl_volatility':'Y'}),on=['date'])
data.dropna(inplace=True)


data = pd.DataFrame(  # 创建数据
    {'Y': np.random.normal(0, 1, 30), 'X1': -3 * np.random.normal(0, 1, 30), 'X2': 5 * np.random.normal(0, 1, 30)})
X = data['X']  # 解释变量
Y = data['Y']  # 被解释变量

model, result, resid = OLS_model(X, Y, summary=True, title_params=['X'])
model, result, resid













