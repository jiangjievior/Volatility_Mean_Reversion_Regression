import pandas as pd
import numpy as np
import copy

from pandas import DataFrame

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 数据文件.基本参数 import PATH_VOL_SAMPLE
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_cross_vol, get_series_vol
from 项目文件.定义公用变量.计算过去波动率涨跌幅度 import DefinitionVolatilityChangePast
from 项目文件.定义公用变量.计算未来波动率涨跌幅度 import DefinitionVolatilityChangeFuture

#从时间序列数据的角度，拟合 波动率变化 与 波动率和均值的距离 之间的关系
class SeriesDistanceAndVolatilityChange():

    def __init__(self,option
                 ):
        self.option = option  # 期权数据
        self.min_MSE=10000
        self.params_min_MSE=()
        self.i=0
        pass


#从截面数据的角度，拟合 波动率变化 与 波动率和均值的距离 之间的关系
class CrossDistanceAndVolatilityChange():

    def __init__(self,
                 PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                 num_date=757,
                 days_windows=[]
                 ):
        # 提取横截面数据
        self.option = get_cross_vol(path_vol=PATH_VOL_SAMPLE, num_date=num_date, )

        self.dates=list(self.option.index)
        self.stocks=list(self.option.columns)

        # 定义波动率的涨跌幅
        self.definate_varibles()




    # 定义波动率的涨跌幅
    def definate_varibles(self):
        # 定义波动率过去的涨跌幅
        self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks)

        #定义波动率未来的涨跌幅
        self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks)



    #用OLS对截面数据在每个交易日进行拟合
    def OLS_Distance_and_VolChange_date(self,
                                   Distance,
                                   VolChange,
                                   ):

        model, result, resid = OLS_model(X=Distance, Y=VolChange, summary=True, title_params=['X'])
        return result


    # 用OLS对截面数据在所有交易日进行拟合，并返回 每个交易日的拟合结果 及 总体结果的描述性统计分析
    def OLS_Distance_and_VolChange(self,
                                   data,
                                   title='',#本次运行的变量组合名称
                                  ):

        result_s={}
        for date in self.dates:
            try:
                X=data[f'{date}X']
                Y=data[f'{date}Y']
                result=self.OLS_Distance_and_VolChange_date(Distance=X,VolChange=Y)
                result_s[date]=result
                print(f'用OLS拟合截面数据已经完成{date}')

            except:
                continue

        result_s_=pd.concat(result_s.values(),keys=result_s.keys())
        result_s_=result_s_.loc[pd.IndexSlice[:,'X'],:]
        result_s_=pd.DataFrame(result_s_.values,columns=result_s_.columns,index=result_s_.index.get_level_values(0))
        result_s_.index.name='date'

        result_s_describe=result_s_[['系数','系数t值','系数p值','调整后R方']].describe()

        return result_s_,result_s_describe


    #使用最小二乘法对截面数据进行拟合
    def run_OLS(self,
                models=[['rV_past_mean','dV_past_std'],
                        ['rV_future_mean','dV_future_std']],
                #拟合时，代使用的模型，即 X 与 Y 的一一对应关系
                #其中第一个列表为X，第二列表为Y

                #例如：
                # [['rV_past_mean', 'dV_past_std'],
                # ['rV_future_mean', 'dV_future_std']]将会产生 'rV_past_mean'~'rV_future_mean' 和 'dV_past_std'~'dV_future_std' 的对应关系

                # 波动率距离均值距离 的 变量类型 可选择范围
                #  ['dV_past', 'rV_past', 'dV_past_mean', 'rV_past_mean', 'dV_past_std', 'dV_past_min',
                #  'dV_past_max', 'rV_past_min', 'rV_past_max', 'dummy_past_diff_higher_std',
                #  'dummy_past_diff_lower_std', ]
                # 未来波动率变化 的 变量类型 可选择范围
                #  ['dV_future','rV_future','dV_future_mean','rV_future_mean','dV_future_std','dV_future_min','dV_future_max','rV_future_min','rV_future_max','dummy_future_diff_higher_std','dummy_future_diff_lower_std',]

                ):

        #依据要求计算定义的变量
        self.varibles_future=self.define_varibles_future.varibles_type(cols_varible_type=list(set(models[1])))
        self.varibles_past = self.define_varibles_past.varibles_type(cols_varible_type=list(set(models[0])))


        #将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
        result_cross={}
        for col_future,col_past in zip(models[1],models[0]):
            title=f'{col_future} ~ {col_past}'
            data_X=self.varibles_past[col_past].T
            data_Y=self.varibles_future[col_future].T

            data_X.columns=data_X.columns.astype(str)+'X'
            data_Y.columns = data_Y.columns.astype(str) + 'Y'

            data=pd.concat([data_X,data_Y],axis=1)
            data=data.T.dropna().T
            result_,result_describe=self.OLS_Distance_and_VolChange(data=data,title=title)
            result_cross[title]=[result_,result_describe]

        return result_cross




#从截面数据的角度，在不同长度的滑动窗口上，拟合 波动率变化 与 波动率和均值的距离 之间的关系
class CrossDistanceAndVolatilityChangeDifferentWindows(CrossDistanceAndVolatilityChange):

    def __init__(self,
                 PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                 num_date=757,
                 days_past_windows=[30,60,100,200],#各种过去变量的滑动窗口长度
                 days_future_windows=[30,60,100,200],#各种未来变量的滑动窗口长度
                 ):
        super(CrossDistanceAndVolatilityChangeDifferentWindows,self).__init__(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,num_date=num_date)
        self.days_past_windows=days_past_windows
        self.days_future_windows = days_future_windows


    def run_OLS(self,
                models=[['rV_past_mean'],
                        ['rV_future_mean']],
                #拟合时，代使用的模型，即 X 与 Y 的一一对应关系
                #其中第一个列表为X，第二列表为Y

                #例如：
                # [['rV_past_mean', 'dV_past_std'],
                # ['rV_future_mean', 'dV_future_std']]将会产生 'rV_past_mean'~'rV_future_mean' 和 'dV_past_std'~'dV_future_std' 的对应关系

                # 波动率距离均值距离 的 变量类型 可选择范围
                #  ['dV_past', 'rV_past', 'dV_past_mean', 'rV_past_mean', 'dV_past_std', 'dV_past_min',
                #  'dV_past_max', 'rV_past_min', 'rV_past_max', 'dummy_past_diff_higher_std',
                #  'dummy_past_diff_lower_std', ]
                # 未来波动率变化 的 变量类型 可选择范围
                #  ['dV_future','rV_future','dV_future_mean','rV_future_mean','dV_future_std','dV_future_min','dV_future_max','rV_future_min','rV_future_max','dummy_future_diff_higher_std','dummy_future_diff_lower_std',]

                ):
        result_cross={}


        for days_past,days_future in zip(self.days_past_windows,self.days_future_windows):
            # 在指定的窗口长度上，定义波动率过去、未来的涨跌幅
            self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks,days_past=days_past)
            self.varibles_future = self.define_varibles_future.varibles_type(cols_varible_type=list(set(models[1])))

            self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks,days_future=days_future)
            self.varibles_past = self.define_varibles_past.varibles_type(cols_varible_type=list(set(models[0])))


            # 将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
            # result_cross_windows = {}
            for col_future, col_past in zip(models[1], models[0]):
                title = f'{col_future}_{days_future} ~ {col_past}_{days_past}'
                data_X = self.varibles_past[col_past].T
                data_Y = self.varibles_future[col_future].T

                data_X.columns = data_X.columns.astype(str) + 'X'
                data_Y.columns = data_Y.columns.astype(str) + 'Y'

                data = pd.concat([data_X, data_Y], axis=1)
                data = data.T.dropna().T
                _, result_describe = self.OLS_Distance_and_VolChange(data=data, title=title)
                result_cross[title] = result_describe

        result_cross=pd.concat(result_cross.values(),keys=result_cross.keys(),axis=0)

        return result_cross


#从截面数据的角度，依据不同特征，拟合 波动率变化 与 波动率和均值的距离 之间的关系
class CrossDistanceAndVolatilityChangeDifferentCharacters(CrossDistanceAndVolatilityChange):

    def __init__(self,
                 PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                 num_date=757,
                 ):
        super(CrossDistanceAndVolatilityChangeDifferentCharacters,self).__init__(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,num_date=num_date)





    def run_OLS(self,
                models=[['rV_past_mean'],
                        ['rV_future_mean']],
                #拟合时，代使用的模型，即 X 与 Y 的一一对应关系
                #其中第一个列表为X，第二列表为Y

                #例如：
                # [['rV_past_mean', 'dV_past_std'],
                # ['rV_future_mean', 'dV_future_std']]将会产生 'rV_past_mean'~'rV_future_mean' 和 'dV_past_std'~'dV_future_std' 的对应关系

                # 波动率距离均值距离 的 变量类型 可选择范围
                #  ['dV_past', 'rV_past', 'dV_past_mean', 'rV_past_mean', 'dV_past_std', 'dV_past_min',
                #  'dV_past_max', 'rV_past_min', 'rV_past_max', 'dummy_past_diff_higher_std',
                #  'dummy_past_diff_lower_std', ]
                # 未来波动率变化 的 变量类型 可选择范围
                #  ['dV_future','rV_future','dV_future_mean','rV_future_mean','dV_future_std','dV_future_min','dV_future_max','rV_future_min','rV_future_max','dummy_future_diff_higher_std','dummy_future_diff_lower_std',]

                ):
        result_cross={}


        for days_past,days_future in zip(self.days_past_windows,self.days_future_windows):
            # 在指定的窗口长度上，定义波动率过去、未来的涨跌幅
            self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks,days_past=days_past)
            self.varibles_future = self.define_varibles_future.varibles_type(cols_varible_type=list(set(models[1])))

            self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks,days_future=days_future)
            self.varibles_past = self.define_varibles_past.varibles_type(cols_varible_type=list(set(models[0])))


            # 将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
            # result_cross_windows = {}
            for col_future, col_past in zip(models[1], models[0]):
                title = f'{col_future}_{days_future} ~ {col_past}_{days_past}'
                data_X = self.varibles_past[col_past].T
                data_Y = self.varibles_future[col_future].T

                data_X.columns = data_X.columns.astype(str) + 'X'
                data_Y.columns = data_Y.columns.astype(str) + 'Y'

                data = pd.concat([data_X, data_Y], axis=1)
                data = data.T.dropna().T
                _, result_describe = self.OLS_Distance_and_VolChange(data=data, title=title)
                result_cross[title] = result_describe

        result_cross=pd.concat(result_cross.values(),keys=result_cross.keys(),axis=0)

        return result_cross


