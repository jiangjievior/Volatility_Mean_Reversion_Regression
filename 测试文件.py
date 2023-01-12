from 数据文件.基本参数 import *
import pandas as pd
import numpy as np
import os

import datetime
import time,timeit


########################################################################################################################
#Heston模型求解范例测试   之   Heston1993年期权计算公式参数最优化求解
########################################################################################################################
from 项目文件.Heston模型.Heston1993期权定价计算公式 import H93_call_value
from 项目文件.Heston模型.Heston1993参数最优化 import Calibrate_Heston_1993
option=pd.read_csv('项目文件/Heston模型/SPY期权.csv')
#添加无风险利率
rate_risk_free=pd.read_csv('项目文件/Heston模型/美国国债利率.csv',usecols=['Date','12.0'])
rate_risk_free.columns=['date','rate_risk_free']
rate_risk_free['date']=rate_risk_free['date'].apply(lambda x:x[:4]+x[5:7]+x[8:])
rate_risk_free['date']=rate_risk_free['date'].astype(int)

option=pd.merge(option,rate_risk_free,on=['date'])
option
option_=option[(option['date']==20200331)&(option['Type']=='C')]
option_=option_[(option_['Volume']>0)&(option_['OpenInterest']>0)&(option_['Expiration']==20200408)]



CH=Calibrate_Heston_1993(option=option_)
p=CH.H93_calibration_full()



option.columns








########################################################################################################################
#Heston模型求解范例测试   之   Heston1993年期权计算公式
########################################################################################################################
from 项目文件.Heston1993模型.Heston1993期权定价计算公式 import H93_call_value

Call=H93_call_value(S0=225.24, K=219.5, T=0.02192, r=0.0089)#5.82












########################################################################################################################
#SPX500期权隐含波动率的均值回复
########################################################################################################################
surface=pd.read_csv(PATH_VOL_SURFACE_SPX,usecols=['date', 'days', 'delta', 'impl_volatility', 'impl_strike',
       'impl_premium', 'dispersion', 'cp_flag'])
surface.columns

series_surface=surface[(surface['days']==30)&(surface['delta']==10)][['date', 'impl_volatility']]
series_surface.reset_index(inplace=True)
#series_surface.index=series_surface['date'].astype(str)
#surface_pivot=pd.pivot_table(surface,index=['delta'],columns=['days'],values=['impl_volatility'])


#记录某个交易日的波动率占过去n个交易日的分位数
quantile_s=[]
for i in range(200,len(series_surface)):
    date=series_surface.loc[i,'date']
    vol=series_surface.loc[i,'impl_volatility']
    series_surface_date=series_surface.loc[:i,:]
    quantile=len(series_surface_date[series_surface_date['impl_volatility']<=vol])/len(series_surface_date)
    quantile_total = len(series_surface[series_surface['impl_volatility'] <= vol]) / len(series_surface)
    quantile_s.append([date,vol,quantile,quantile_total])
    print(date)

quantile_s=pd.DataFrame(quantile_s,columns=['date','vol','quantile','quantile_total'])















t_0=300
t_start=400
t_end=1500
series_surface['impl_volatility'][t_0+t_start:t_0+t_end].plot(figsize=(30,6))
series_surface['impl_volatility'][t_0+t_start:t_0+t_end].describe()



option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=400000)
under=pd.read_csv(PATH_UNDER)


for data in option:
    data=pd.DataFrame(data)


    time.process_time()
    data['issuer'].str.len()  # 计算字符串长度
    print(time.process_time())

    time.process_time()
    data['issuer'].apply(lambda x:len(x))
    print(time.process_time())






    data.info()# 查看数据集信息
    data.describe()#返回描述性统计信息
    data.dtypes#检查数据中各列的数据类型
    data.head(n=6)
    data.tail(n=6)


    data.sample(n=6)#随机挑选6行数据
    data['delta'].rank()#获取数据排名
    data['delta'].clip(0.4,0.6)#截断数据，将数据卡在某个范围（低于0.4的数改为0.4，高于0.6的数改为0.6）
    data['issuer'].str.contains('C')#文本数据操作
    data['issuer'].str.len()  # 计算字符串长度
    data['issuer'].str.repeat(3)  # 重复字符串几次
    pd.DataFrame(data['issuer'].str.split(' ').tolist())  # 分割字符串，将一列扩展为多列
    data['issuer'].str.strip('C')#去除指定字符
    data['issuer'].str.findall('.(.)E.*')#利用正则表达式，去字符串中匹配，返回查找结果的列表

    data.drop(columns=['secid'])#剔除'secid'列
    data.drop(index=[4])  # 剔除4行

    pivot=pd.pivot_table(data,index=['date'],columns=['cp_flag'],values=['delta'])['delta']

    pivot.unstack()
    pivot.stack()
    #将宽表转长表，即表格型数据转为树形数据
    pivot['date']=pivot.index
    pivot.melt(id_vars='date',var_name='cp_flag',value_name='delta')


    data=pd.DataFrame({
        '姓名':['A','B','C','D','E','F','G'],
        '数学':[67,45,43,56,72,64,71],
        '语文':[82,67,78,74,56,58,81],
        '英语':[69,47,97,76,69,65,63],})

    # 将宽表转长表，即表格型数据转为树形数据
    # 以 姓名 为匹配目标，将其他列合并；value_name='成绩' 表示将列标题形成的列命名为 成绩；var_name='科目' 表示将数值形成的列命名为 科目
    melt=data.melt(id_vars='姓名',value_name='成绩',var_name='科目',value_vars=['语文','数学'])#value_vars=['语文','数学'] 表示只保留 语文和数学 成绩


    #将长表转宽表，即树形数据转为表格型数据
    pivot=melt.pivot(index='姓名',columns='科目',values='成绩')
    #如果表内数据为文本型数据，pivot()依然可以正常操作，但pivot_table()只能操作数值型数据
    pivot=melt.astype(str).pivot(index='姓名', columns='科目', values='成绩')

    #数据分组
    groupby=melt.groupby('科目').mean()
    pivot_table=melt.pivot_table(index=['姓名'],columns=['科目'],values=['成绩'],aggfunc=[np.mean,np.max,np.min])


    melt.stack()



















    data['issuer'].contain('C')

















    id_option=data['optionid'].sample(1).values[0]
















data=pd.DataFrame({'date_start':['2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07'],
                   'date_end':['2020-03-08', '2020-03-09', '2020-03-10', '2020-03-11'],})
#将字符串修改日期格式
data['date_start']=pd.to_datetime(data['date_start'],format='%Y-%m-%d')
data['date_end']=pd.to_datetime(data['date_end'],format='%Y-%m-%d')
#计算两个日期之间的相差天数
data['days']=data['date_end']-data['date_start']
data['days']=data['days'].apply(func=lambda x:x.days)
#将日期修改为指定格式
data['date_start']=data['date_start'].dt.strftime('%Y%m%d')
data['date_end']=data['date_end'].dt.strftime('%Y%m%d')








array_date=pd.DataFrame(pd.date_range(start='20180501',freq='m',periods=30))
array_date.dt.strftime('%Y%m%d')


data=pd.DataFrame(pd.date_range('20200304','20200817',freq='d'),columns=['date'])
data['date'].dt.strftime('%Y%m%d')#更改为‘20200817’
data['date'].dt.strftime('%Y.%m')#更改为‘202008’





#pd.date_range()生成日期序列
pd.date_range(start='20180501',end='20190302')#生成从'20180501'到'20190302'日度日期序列
pd.date_range(start='20180501',end='20190302',freq='D')#生成从'20180501'到'20190302'日度日期序列
pd.date_range(start='20180501',freq='m',periods=30)#生成从'20180501'开始，总数为30的月度日期序列







#获取每一个时间戳的年、月、日、时、分、秒
array_date=pd.date_range(start='20180501',freq='m',periods=30)
array_date[0].year
array_date[0].month
array_date[0].day
array_date[0].hour
array_date[0].minute
array_date[0].second


#pd.to_datetime()修改日期格式,并计算两个日期之间的相差天数
data=pd.DataFrame({'date_start':pd.date_range('2018-03-01',periods=50),
                   'date_end':pd.date_range('2019-06-21',periods=50),})

data['date_start']=pd.to_datetime(data['date_start'],format='%Y-%m-%d')#根据指定格式修改日期格式
data['date_end']=pd.to_datetime(data['date_end'],format='%Y-%m-%d')

data['days']=data['date_end']-data['date_start']#计算两个日期之间的相差天数
data['days'].apply(func=lambda x:x.days)
data.applymap(func=lambda data:data['date_end']-data['date_start'])




pd.DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04',
                   '2018-01-05', '2018-01-06', '2018-01-07', '2018-01-08'],
                  dtype='datetime64[ns]', freq='D')




pd.period_range()
pd.interval_range()
pd.timedelta_range()
pd.DatetimeIndex()
pd.DatetimeTZDtype()









pd.to_datetime()
np.datetime_data()
np.datetime_as_string()


data=pd.DataFrame(
    {
        'date_start':[]
    }
)


















option=pd.read_csv(PATH_OPTION,iterator=True,chunksize=4000000)
under=pd.read_csv(PATH_UNDER)


for data in option:
    data['date']=pd.to_datetime(data['date'],format='%Y%m%d')#通过为数据指定时间格式，快速将数据改为时间数据

    data['exdate'] = pd.to_datetime(data['exdate'], format='%Y%m%d')  # 通过为数据指定时间格式，快速将数据改为时间数据
    data['days']=data['exdate']-data['date']


    data['days'].apply(lambda x:x.days)




    data['date'].year



    #data['date'].astype(str).apply(lambda x:datetime.datetime.strptime(x,'%Y%m%d'))
    datetime.datetime.strptime('20200213','%Y%m%d')



























    #data=data[data['date']>20100101]
    data['days'] = pd.to_datetime(data['exdate'], format='%Y%m%d') - pd.to_datetime(data['date'],
                                                                                              format='%Y%m%d')
    data['days']





























