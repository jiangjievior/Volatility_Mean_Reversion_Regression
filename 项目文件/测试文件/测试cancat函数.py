import pandas as pd
import numpy as np



data_1=pd.DataFrame(
    np.random.rand(4,5),columns=[1,2,3,4,5],index=['a','b','c','d']
)

data_2=pd.DataFrame(
    np.random.rand(4,5),columns=[1,2,3,4,5],index=['a','b','c','d']
)

data_3=pd.DataFrame(
    np.random.rand(4,5),columns=[1,2,3,4,5],index=['a','b','c','d']
)

data_4=pd.DataFrame(
    np.random.rand(4,5),columns=[1,2,3,4,5],index=['a','b','c','d']
)


data__1=pd.concat([data_1,data_2],keys=['a','b'],axis=1)
data__2=pd.concat([data_1,data_2],keys=['a','b'],axis=1)




data__=pd.concat([data__1,data__2],keys=[1,2],axis=0)





