from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=4000000)
under=pd.read_csv(PATH_UNDER)


for data in option:
    data=pd.DataFrame(data)
    id_option=data['optionid'].sample()
    data.columns.name='l'
    data.columns
    data.loc['l',:]







    data['date']=pd.to_datetime(data['date'],format='%Y%m%d')#通过为数据指定时间格式，快速将数据改为时间数据

    data['exdate'] = pd.to_datetime(data['exdate'], format='%Y%m%d')  # 通过为数据指定时间格式，快速将数据改为时间数据
    data['days']=data['exdate']-data['date']


    data['days'].apply(lambda x:x.days)
















































