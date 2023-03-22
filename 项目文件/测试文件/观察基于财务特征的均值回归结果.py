import pandas as pd
import os
import pandas as pd

path_base='E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\基于财务特征的均值回复结果'
files=os.listdir(path_base)

files

pivot_s= {}
for file in files:
    data=pd.read_csv(os.path.join(path_base,file))
    data
    pivot=pd.pivot_table(data,index=['quantitle'],values=['coef','t'])
    pivot_s[file]=pivot


pivot_s




































