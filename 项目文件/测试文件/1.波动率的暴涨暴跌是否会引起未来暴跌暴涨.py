from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# 1.波动率的暴涨暴跌是否会引起未来暴跌暴涨
from 项目文件.测试文件.研究波动率的过去变化与未来变化之间的关系 import RelationFutureAndPast

surface = pd.read_csv(PATH_VOL_SURFACE_SPX)
surface_days_delta = surface[(surface['days'] == 30) & (surface['delta'] == -50)]
surface_days_delta.index = range(len(surface_days_delta))
RFAP =RelationFutureAndPast(surface=surface_days_delta ,)
RFAP.run(num_past=30, num_future=30)
# 波动率暴涨之后，未来是否有可能跌得更狠
results_up = RFAP.protfolios_sort(col_X='rate_min_windows_past', col_Y='rate_min_windows_future')
# 波动率暴跌之后，未来是否有可能涨得更狠
results_down = RFAP.protfolios_sort(col_X='rate_max_windows_past', col_Y='rate_max_windows_future')



