# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import copy

from pandas import DataFrame

from 功能文件.模型拟合.拟合OLS模型 import OLS_model
from 数据文件.基本参数 import PATH_VOL_SAMPLE
from 项目文件.数据处理.获取指定个股的财务数据 import finance_ratio_stock
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
                 days_past=30,#过去变量的移动窗口长度（天数）
                 days_future=30,#未来变量的移动窗口长度（天数）
                 ):
        # 提取横截面数据
        self.option = get_cross_vol(path_vol=PATH_VOL_SAMPLE)

        self.titile=PATH_VOL_SAMPLE#文件名称

        self.dates=list(self.option.index)
        self.stocks=list(self.option.columns)

        self.days_past = days_past  # 过去变量的移动窗口长度（天数）
        self.days_future = days_future  # 未来变量的移动窗口长度（天数）

        # 定义波动率的涨跌幅
        self.definate_varibles()




    # 定义波动率的涨跌幅
    def definate_varibles(self):
        # 定义波动率过去的涨跌幅
        self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks,days_past=self.days_past)

        #定义波动率未来的涨跌幅
        self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks,days_future=self.days_future)



    #用OLS对截面数据在每个交易日依据每个特征进行拟合
    def OLS_Distance_and_VolChange_date(self,
                                   Distance,
                                   VolChange,
                                   ):


        # self.


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
                X=data[f'{date}X'].dropna()
                Y=data[f'{date}Y'].dropna()

                #保留X和Y的共有股票数据
                stocks_common=set(X.index).intersection(set(Y.index))
                X=X[stocks_common]
                Y = Y[stocks_common]

                result=self.OLS_Distance_and_VolChange_date(Distance=X,VolChange=Y)
                result_s[date]=result
                print(f'{self.titile}\n拟合截面数据已经完成{date}的{title}')

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
                models=[['rV_past_mean', 'dV_past_std'],
                        ['rV_future_mean', 'dV_future_std']],
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
        result_s={}

        for days_past,days_future in zip(self.days_past_windows,self.days_future_windows):
            try:
                # 在指定的窗口长度上，定义波动率过去、未来的涨跌幅
                self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks,days_past=days_past)
                self.varibles_future = self.define_varibles_future.varibles_type(cols_varible_type=list(set(models[1])))

                self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks,days_future=days_future)
                self.varibles_past = self.define_varibles_past.varibles_type(cols_varible_type=list(set(models[0])))


                # 将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
                # result_cross_windows = {}
                for col_future, col_past in zip(models[1], models[0]):
                    try:
                        title = f'{col_future}_{days_future} ~ {col_past}_{days_past}'
                        data_X = self.varibles_past[col_past].T
                        data_Y = self.varibles_future[col_future].T

                        data_X.columns = data_X.columns.astype(str) + 'X'
                        data_Y.columns = data_Y.columns.astype(str) + 'Y'

                        data = pd.concat([data_X, data_Y], axis=1)
                        #data = data.T.dropna().T
                        result, result_describe = self.OLS_Distance_and_VolChange(data=data, title=title)
                        result_cross[title] = result_describe
                        result_s[title]=result
                    except:
                        continue
            except:
                continue

        result_cross=pd.concat(result_cross.values(),keys=result_cross.keys(),axis=0)

        return result_s,result_cross


#基于历史波动率不同的上涨幅度或下跌幅度，在不同的过去未来窗口上，波动率均值回复特征回归结果
class MeanReversionRegressionDifferentWindowsDifferentVolatilityChange():

    def __init__(self,
                 PATH_VOL_S,
                 models=[['rV_past_mean', 'dV_past_std'],
                         ['rV_future_mean', 'dV_future_std']],
                 days_past_windows=[30,60,100,200],#各种过去变量的滑动窗口长度
                 days_future_windows=[30,60,100,200],#各种未来变量的滑动窗口长度
                 nodes=[0.1, 0.3, 0.5, 0.7],#划分样本时所使用的分位数节点
                 ):
        self.PATH_VOL_S=PATH_VOL_S
        self.models=models
        self.nodes=nodes
        self.days_past_windows=days_past_windows
        self.days_future_windows = days_future_windows

    def run_OLS(self,
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
        result_cross_s=[]#详细回归结果

        #读取不同类型的波动率曲面数据
        for key in self.PATH_VOL_S.keys():
            try:
                # 提取横截面数据
                self.option = get_cross_vol(path_vol=self.PATH_VOL_S[key])
                # 文件名称
                self.titile = self.PATH_VOL_S[key]
                self.put_call=key.split('&')[0]
                self.delta=int(key.split('&')[1][-2:])
                self.days_to_maturity=int(key.split('&')[2][-2:])

                #交易日期
                self.dates = list(self.option.index)
                #可交易股票名称
                self.stocks = list(self.option.columns)

                #运行不同的窗口长度的数据
                for days_past,days_future in zip(self.days_past_windows,self.days_future_windows):
                    try:
                        # 在指定的窗口长度上，定义波动率过去、未来的涨跌幅
                        self.define_varibles_past = DefinitionVolatilityChangePast(option=self.option, col_iv=self.stocks,days_past=days_past)
                        self.varibles_past = self.define_varibles_past.varibles_type(
                            cols_varible_type=list(set(self.models[0])))

                        self.define_varibles_future = DefinitionVolatilityChangeFuture(option=self.option, col_iv=self.stocks,days_future=days_future)
                        self.varibles_future = self.define_varibles_future.varibles_type(
                            cols_varible_type=list(set(self.models[1])))

                        # 将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
                        for col_future, col_past in zip(self.models[1], self.models[0]):
                            try:
                                title = f'{col_future}_{days_future} ~ {col_past}_{days_past}'
                                data_X = self.varibles_past[col_past].T
                                data_Y = self.varibles_future[col_future].T

                                data_X.columns = data_X.columns.astype(str) + 'X'
                                data_Y.columns = data_Y.columns.astype(str) + 'Y'

                                data = pd.concat([data_X, data_Y], axis=1)
                                # result_s = {}

                                #在不同的交易日上，拟合不同的结果
                                for date in self.dates:
                                    try:
                                        X = data[f'{date}X'].dropna()
                                        Y = data[f'{date}Y'].dropna()

                                        # 保留X和Y的共有股票数据
                                        stocks_common = set(X.index).intersection(set(Y.index))
                                        X = X[stocks_common]
                                        Y = Y[stocks_common]

                                        #将数据划分为不同节点
                                        #nodes=[0.1,0.3,0.5,0.7]#分位数节点
                                        
                                        X_up=X[X>0]
                                        for node in self.nodes:
                                            try:
                                                quantitle_X_up_node=X_up.quantile(node)
                                                X_up_node=X_up[X_up>quantitle_X_up_node]
                                                Y_up_node=Y[X_up_node.index]
                                                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X_up_node,Y_up_node)

                                                result_cross_s.append(
                                                    [self.put_call, self.delta, self.days_to_maturity, col_past,
                                                     days_past, col_future, days_future, date, 'up', node] +
                                                    params[1] + tvalues[1] + pvalues[1] + [R_2])
                                            except:
                                                continue

                                        X_down = -X[X <0 ]
                                        for node in self.nodes:
                                            try:
                                                quantitle_X_down_node = X_down.quantile(node)
                                                X_down_node = X_down[X_down > quantitle_X_down_node]
                                                Y_down_node = Y[X_down_node.index]
                                                model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(
                                                    -X_down_node, Y_down_node)

                                                result_cross_s.append(
                                                    [self.put_call,self.delta,self.days_to_maturity,col_past,days_past,col_future,days_future,date,'down',node] +
                                                                      params[1] + tvalues[1] + pvalues[1] + [R_2])
                                            except:
                                                continue
                                        

                                        print(f'{self.titile}\n拟合截面数据已经完成{date}的{title}')

                                    except:
                                        continue



                            except:
                                continue
                    except:
                        continue
            except:
                continue

        result_cross = pd.DataFrame(result_cross_s,
                                      columns=['put_call', 'delta', 'days', 'col_past', 'days_past', 'col_future',
                                               'days_future', 'date', 'down', 'node', 'params', 't', 'p', 'R'])

        return result_cross_s

    #生成数据节点，用以数据分组
    def node(self,
             data,#np.array()
             type, #节点类型
             num=5,#节点个数
             ):

        #按照数据的百分比分位数，产生节点
        if type=='quant_q':
            nodes=pd.DataFrame(data).quantile(q=np.arange(0,1,1/5))[0].tolist()
            return nodes

        #按照绝对
        elif type=='absolute':
            pass







        pass


#从截面数据的角度，依据不同特征，拟合 波动率变化 与 波动率和均值的距离 之间的关系
class CrossDistanceAndVolatilityChangeDifferentCharacters(CrossDistanceAndVolatilityChange):

    def __init__(self,
                 PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                 num_date=757,
                 days_past=30,
                 days_future=30,
                 ):
        super(CrossDistanceAndVolatilityChangeDifferentCharacters,self).__init__(PATH_VOL_SAMPLE=PATH_VOL_SAMPLE,
                                                                                 num_date=num_date,
                                                                                 days_past=days_past,
                                                                                 days_future=days_future
                                                                                 )


    # 将特征数据在各个日期排序分组
    def sort_characters_date(self,
                        character,
                        q=5,
                        q_labels='',
                        col_character='',
                        ):
        self.col_character=col_character#特征的名称
        self.q_labels=np.arange(1, q + 1) if q_labels=='' else q_labels#组合标签
        self.q = q  # 组合数量

        character_qcut = []
        for col in character.columns:
            character_qcut.append(pd.qcut(character[col], q=self.q, labels=self.q_labels))
        character_qcut = pd.DataFrame(character_qcut, index=character.columns,
                                          columns=character.index).T

        self.character_qcut=character_qcut


    #依据特征，将期权数据进行分组排序
    def sort_options_according_charactes(self,
                                         col_Characters='roe',  # 特征名称
                                         q=5,#分组数
                                         ):
        # 生成特征数据，用于将数据划分为不同小组合
        finance_ratio = finance_ratio_stock(
            tickers=self.option.columns,
            name_fin=[col_Characters],
            dates=self.option.index, )
        finance_ratio = pd.pivot_table(finance_ratio, index=['date'], columns=['cusip'], values=[col_Characters])[
            col_Characters].T

        # 依据特征数据的分组排序结果，对各个小组进行拟合
        self.sort_characters_date(character=finance_ratio, q=q, col_character=col_Characters,
                                     q_labels=np.arange(1, q + 1))






    #用OLS对截面数据在每个交易日依据每个特征进行拟合
    def OLS_Distance_and_VolChange_date_characters(self,
                                   Distance,
                                   VolChange,
                                   ):


        model,params,tvalues,pvalues,resid,F,p_F,R_2 = OLS_model(X=Distance, Y=VolChange)
        return model,params,tvalues,pvalues,resid,F,p_F,R_2

    # 用OLS对截面数据在所有交易日进行拟合，并返回 每个交易日的拟合结果 及 总体结果的描述性统计分析
    def OLS_Distance_and_VolChange_characters(self,
                                   data,
                                   title='',  # 本次运行的变量组合名称
                                   ):

        result_s = []
        date_q_s=self.character_qcut.columns
        for i in range(len(date_q_s)):
            try:


                if i==0:
                    date_q=date_q_s[i]

                    #挑选财务日期范围内的数据
                    data_q=data.loc[:,data.columns<=date_q]



                else:
                    pass


            except:
                continue




        result_s = []
        for date in self.dates:
            try:
                character_qcut_date=self.character_qcut[date]
                for q in self.q_labels:
                    try:
                        stock_q=character_qcut_date[character_qcut_date==q].index

                        X = data.loc[stock_q,f'{date}X']
                        Y = data.loc[stock_q,f'{date}Y']
                        model,params,tvalues,pvalues,resid,F,p_F,R_2 = self.OLS_Distance_and_VolChange_date_characters(Distance=X, VolChange=Y)
                        result_s.append([date,q,params,tvalues,pvalues,R_2])
                    except:
                        continue
                    print(f'用OLS拟合截面数据已经完成{date}的{title}')

            except:
                continue

        result_s_ = pd.concat(result_s.values(), keys=result_s.keys())
        result_s_ = result_s_.loc[pd.IndexSlice[:, 'X'], :]
        result_s_ = pd.DataFrame(result_s_.values, columns=result_s_.columns,
                                 index=result_s_.index.get_level_values(0))
        result_s_.index.name = 'date'

        result_s_describe = result_s_[['系数', '系数t值', '系数p值', '调整后R方']].describe()

        return result_s_, result_s_describe


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

        # 依据要求计算定义的变量
        self.varibles_future = self.define_varibles_future.varibles_type(cols_varible_type=list(set(models[1])))
        self.varibles_past = self.define_varibles_past.varibles_type(cols_varible_type=list(set(models[0])))

        # 将X和Y的各个变量逐步配对，并使用OLS逐对拟合模型
        result_cross = []
        for col_future, col_past in zip(models[1], models[0]):
            title = f'{col_future} ~ {col_past}'
            data_X = self.varibles_past[col_past]
            data_Y = self.varibles_future[col_future]

            #对二者日期取交集，从而保留下来X和Y的共有数据
            set_date=list(set(data_X.index).intersection(set(data_Y.index)))
            data_X=data_X.loc[set_date,:]
            data_Y = data_Y.loc[set_date, :]

            #将期权波动率数据按照财务表的日期范围进行切分
            #由于财务表的日期为跨月度的日期，所以需要对波动率日度数据进行切分
            date_q_s = self.character_qcut.columns
            num=1#进度条总进程
            for i in range(len(date_q_s)):
                try:

                    if i == 0:
                        date_end = date_q_s[i]

                        # 挑选财务日期范围内的数据
                        data_X_Character_date = data_X.loc[data_X.index <= date_end,:]
                        data_Y_Character_date = data_Y.loc[data_Y.index <= date_end,:]

                    else:
                        date_start = date_q_s[i-1]
                        date_end = date_q_s[i ]

                        # 挑选财务日期范围内的数据
                        data_X_Character_date = data_X.loc[(data_X.index <= date_end)&(data_X.index > date_start), :]
                        data_Y_Character_date = data_Y.loc[(data_X.index <= date_end)&(data_X.index > date_start), :]

                    #在每个交易日期拟合均值回复
                    for date in data_X_Character_date.index:
                        try:
                            data_X_date=data_X_Character_date.loc[date,:]
                            data_Y_date=data_Y_Character_date.loc[date,:]

                            #依据财务指标对期权数据分组,并回归
                            for q in self.q_labels:
                                try:
                                    stocks_q=self.character_qcut[date_end][self.character_qcut[date_end]==q].index
                                    data_X_q=data_X_date[stocks_q].dropna()
                                    data_Y_q = data_Y_date[stocks_q].dropna()

                                    #保留X和Y的共有股票
                                    stocks_common=set(data_X_q.index).intersection(set(data_Y_q.index))
                                    data_X_q=data_X_q[stocks_common]
                                    data_Y_q=data_Y_q[stocks_common]

                                    model, params, tvalues, pvalues, resid, F, p_F, R_2 = OLS_model(X=data_X_q,
                                                                                                    Y=data_Y_q)
                                    result_cross.append([date,title, q, params[-1], tvalues[-1], pvalues[-1], R_2])

                                    #进度条展示
                                    num_total=len(self.q_labels)*len(data_X_Character_date.index)*len(date_q_s)*len(list(zip(models[1], models[0])))
                                    print(f'已经完成{title}的{date}在分组{q}的结果，已经完成任务{round(num/num_total,4)}')
                                    num+=1

                                except:
                                    continue
                        except:
                            continue
                except:
                    continue

        result_cross=pd.DataFrame(result_cross,columns=['date','title','quantitle','coef','t','p','R'])

        result=pd.pivot_table(result_cross,index=['quantitle'],values=['coef','t','p','R'])

        return result




            # data_X.columns = data_X.columns.astype(str) + 'X'
            # data_Y.columns = data_Y.columns.astype(str) + 'Y'

        #     data = pd.concat([data_X, data_Y], axis=1)
        #     data = data.T.dropna().T
        #
        #
        #
        #     result_, result_describe = self.OLS_Distance_and_VolChange_characters(data=data, title=title)
        #
        #     result_cross[title] = [result_, result_describe]
        #
        # return result_cross























