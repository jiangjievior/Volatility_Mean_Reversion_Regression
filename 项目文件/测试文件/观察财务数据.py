import pandas as pd
import numpy as np
import copy

from 数据文件.基本参数 import *



finance=pd.read_csv(PATH_FINANCIAL)
AAPL=finance[finance['TICKER']=='AAPL']


len(finance['TICKER'].unique())


