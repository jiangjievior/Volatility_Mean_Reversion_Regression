import pandas as pd
import numpy as np
import copy

from 数据文件.基本参数 import *


#获取个股公司的财务比率
def finance_ratio_stock():
    pass


#获取个股公司的财务比率
def finance_stock():
    pass







if __name__=='__main__':






    finance=pd.read_csv(PATH_FINANCIAL,iterator=True,chunksize=40000)
    for finance_ in finance:
        finance_
        col=np.array(finance_.columns)














    AAPL=finance[finance['TICKER']=='AAPL']


    len(finance['TICKER'].unique())


