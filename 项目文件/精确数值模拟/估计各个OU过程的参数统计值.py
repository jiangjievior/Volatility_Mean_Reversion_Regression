from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os







data=pd.read_csv("H:\美国个股期权数据\SPX.csv")
data

data['cp_flag']







from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
# 计算过去的波动率涨跌幅
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol

# 获取指定格式的截面数据
days=30
vol_cross = get_cross_vol(path_vol=PATH_VOL_S['put&delta50&days30'] )
DVCP = DefinitionVolatilityChangePast(option=vol_cross,days_past=30)
vol_cross=DVCP.dV_past()
vol_cross



vol_diff=vol_cross.diff(days)

vol_diff=vol_diff.loc[20120427,:].dropna()
vol_diff.mean()
vol_diff.std()
vol_diff.skew()







































