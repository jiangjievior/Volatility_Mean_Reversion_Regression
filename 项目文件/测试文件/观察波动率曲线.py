from 功能文件.辅助功能.Debug时获取外部数据绝对路径 import data_real_path
from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

surface=pd.read_csv(PATH_VOL_SURFACE_SPX)
surface
surface_days_delta=surface[(surface['days']==30)&(surface['delta']==50)]
surface_days_delta.index=surface_days_delta['date'].astype(str)
surface_days_delta.loc['20050304':'20070507','impl_volatility'].plot(figsize=(30,8))





















