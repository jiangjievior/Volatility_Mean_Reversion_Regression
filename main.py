from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os


option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=400000)
under=pd.read_csv(PATH_UNDER)

i=0
for data in option:
    #data=data[data['date']>20100101]
    # data['days'] = pd.to_datetime(data['exdate'], format='%Y%m%d') - pd.to_datetime(data['date'],
    #                                                                                           format='%Y%m%d')
    # data['days']
    i+=1



























