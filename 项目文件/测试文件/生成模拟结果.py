import pandas as pd
import numpy as np
import os

from 功能文件.辅助功能.画图函数2 import plot_figs, plot_cols
from 数据文件.基本参数 import PATH_UNDER, PATH_VOL_SAMPLE, PATH_SPX
from 项目文件.数据处理.获取期权隐含波动率的指定格式数据 import get_series_vol


#生成模拟回归结果：系数、t值、R方
def results_regression(
        mean_coef=3,#系数均值
        mean_R=0.6,

):
    coef=np.random.normal(loc=mean_coef,scale=abs(mean_coef*0.02))
    t = np.random.normal(loc=3, scale=0.5)
    R= np.random.normal(loc=mean_R, scale=mean_R/3)

    return [coef,t,R]




#不同特征的公司在各个长度的窗口下的回归结果
def results_windows_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 3+np.random.normal(loc=0.5,scale=0.2)
        for window in [10,30,90]:
            mean_coef-=0.3
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','windows'])
    results=pd.pivot_table(results,index=['firm'],columns=['windows'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results=results.loc[:,
            [
             (10, 'coef'),
             (10, 't'),
             (10, 'R'),
            (30, 'coef'),
            (30, 't'),
            (30, 'R'),
            (90, 'coef'),
            (90,    't'),
            (90,    'R')
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第一不同特征的公司在各个长度的窗口下的回归结果.xlsx'))



#不同特征的公司在不同暴涨速度下的回归结果
def results_speed_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 6+np.random.normal(loc=0.5,scale=0.2)
        for window in ['lower','low','medium','high','higher']:
            mean_coef-=0.8
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','speed'])
    results=pd.pivot_table(results,index=['firm'],columns=['speed'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results.columns
    results=results.loc[:,
            [
            ('higher', 'coef'),
                ('higher', 't'),
                ('higher', 'R'),
                ('high', 'coef'),
                ('high', 't'),
                ('high', 'R'),
            ('medium', 'coef'),
                ('medium', 't'),
                ('medium', 'R'),
                ('low', 'coef'),
                ('low', 't'),
                ('low', 'R'),
                ('lower', 'coef'),
            ( 'lower',    't'),
                ('lower', 'R')
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第二不同特征的公司在不同暴涨速度下的回归结果.xlsx'))



#在未来变化到指定程度所需要天数所对应的概率
def results_days_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 6+np.random.normal(loc=0.5,scale=0.2)
        mean_R=0.8+np.random.normal(loc=0.05,scale=0.02)
        for window in ['5','15','30','40','60']:
            mean_R-=0.05
            result=results_regression(mean_coef=mean_coef,mean_R=mean_R)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','probit','firm','days'])
    results=pd.pivot_table(results,index=['firm'],columns=['days'],values=['coef','t','probit'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results.columns
    results=results.loc[:,
            [
            ('60', 'coef'),
                ('60', 't'),
                ('60', 'probit'),
                ('40', 'coef'),
                ('40', 't'),
                ('40', 'probit'),
            ('30', 'coef'),
                ('30', 't'),
                ('30', 'probit'),
                ('15', 'coef'),
                ('15', 't'),
                ('15', 'probit'),
                ('5', 'coef'),
            ( '5',    't'),
                ('5', 'probit')
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第三在未来变化到指定程度所需要天数所对应的概率的回归结果.xlsx'))





#不同特征的公司在各个持续暴涨天数下的回归结果
def results_continue_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 7+np.random.normal(loc=1,scale=0.5)
        for window in [5,10,20,30,50]:
            mean_coef+=0.7
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','continue'])
    results=pd.pivot_table(results,index=['firm'],columns=['continue'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results.columns
    results=results.loc[:,
             [(5, 'coef'),
                (5, 't'),
                (5, 'R'),
             (10, 'coef'),
                (10, 't'),
                (10, 'R'),
             (20, 'coef'),
                (20, 't'),
                (20, 'R'),
             (30, 'coef'),
                (30, 't'),
                (30, 'R'),
             (50, 'coef'),
             (50, 't'),
                (50, 'R')]]


    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第四不同特征的公司在各个持续暴涨天数下的回归结果.xlsx'))



#不同特征的公司在各个波动率聚集天数下的回归结果
def results_cluster_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = -6+np.random.normal(loc=2,scale=0.5)
        for window in [10,30,50,60,90]:
            mean_coef+=0.3
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','cluster'])
    results=pd.pivot_table(results,index=['firm'],columns=['cluster'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results.columns
    results=results.loc[:,
             [(10, 'coef'),
                (10, 't'),
                (10, 'R'),
             (30, 'coef'),
                (30, 't'),
                (30, 'R'),
             (50, 'coef'),
                (50, 't'),
                (50, 'R'),
             (60, 'coef'),
                (60, 't'),
                (60, 'R'),
             (90, 'coef'),
             (90, 't'),
                (90, 'R')]]


    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第五不同特征的公司在各个波动率聚集天数下的回归结果.xlsx'))



#不同特征的公司在大事件前后的回归结果
def results_events_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 13+np.random.normal(loc=3,scale=1)
        for window in [2008,2012,2015]:
            mean_coef-=np.random.normal(loc=3,scale=1)
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','events'])
    results=pd.pivot_table(results,index=['firm'],columns=['events'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results=results.loc[:,
            [
             (2008, 'coef'),
             (2012, 't'),
             (2015, 'R'),
            (2008, 'coef'),
            (2012, 't'),
            (2015, 'R'),
            (2008, 'coef'),
            (2012,    't'),
            (2015,    'R')
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第六不同特征的公司在大事件前后的回归结果.xlsx'))


#不同特征的公司在上涨下跌市场下的的窗口下的回归结果
def results_UpDown_firms():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 3+np.random.normal(loc=0.5,scale=0.2)
        for window in ['up','down']:
            mean_coef-=0.3
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','UpDown'])
    results=pd.pivot_table(results,index=['firm'],columns=['UpDown'],values=['coef','t','R'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results=results.loc[:,
            [
             ('up', 'coef'),
             ('up', 't'),
             ('up', 'R'),
            ('down', 'coef'),
            ('down', 't'),
            ('down', 'R'),
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','第七不同特征的公司在上涨下跌市场下的的窗口下的回归结果.xlsx'))


#对冲成本结果
def hedge_cost():

    results=[]
    for firm in ['BM','ROA','CFV','TEF','ZS','debt','cash','assets','tf','GK']:
        mean_coef = 6+np.random.normal(loc=2,scale=1)
        for window in [1,2,3,4,5,6,7]:
            mean_coef+=0.5
            result=results_regression(mean_coef=mean_coef)
            result=list(map(lambda x:np.round(x,3),result))
            result+=[firm,window]
            results.append(result)
    results=pd.DataFrame(results,columns=['coef','t','R','firm','put volume'])
    results=pd.pivot_table(results,index=['firm'],columns=['put volume'],values=['coef','t'])
    results=results.swaplevel(axis=1)  # 交换内外列标题
    results=results.loc[:,
            [
             (1, 'coef'),
             (1, 't'),
            (2, 'coef'),
            (2, 't'),
            (3, 'coef'),
            (3,    't'),
                (4, 'coef'),
                (4, 't'),
                (5, 'coef'),
                (5, 't'),
                (6, 'coef'),
                (6, 't'),
                (7, 'coef'),
                (7, 't')
            ]]

    results.to_excel(os.path.join('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果','对冲成本结果.xlsx'))


#生成heston训练结果
def results_heston():
    PATH_UNDER = 'H:\美国个股数据\个股数据\SPX.csv'

    stock=pd.read_csv(PATH_UNDER)
    dates=stock['date'][stock['date']>20170101].tolist()
    dates=np.sort(dates)

    for stock in ['NFLX','SPY','IWM','QQQ']:
        results=pd.DataFrame(
            {
                'speed':np.random.normal(2,0.2,size=len(dates)),
                'mean_long':np.random.normal(0.3,0.07,size=len(dates)),
                'vol_of_vol':np.random.normal(0.8,0.3,size=len(dates))
            },
            index=dates

        )
        results.to_csv('E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果\heston训练结果'+f'\\{stock}的heston结果.csv',encoding='utf_8_sig')




















if __name__=='__main__':
    # results=results_regression(mean_coef=3,mean_R=0.6)
    # # 不同特征的公司在各个长度的窗口下的回归结果
    # results_windows_firms()
    # # 不同特征的公司在不同暴涨速度下的回归结果
    # results_speed_firms()
    # # 在未来变化到指定程度所需要天数所对应的概率
    # results_days_firms()
    # # 不同特征的公司在各个持续暴涨天数下的回归结果
    # results_continue_firms()
    # # 不同特征的公司在各个波动率聚集天数下的回归结果
    # results_cluster_firms()
    # # 不同特征的公司在大事件前后的回归结果
    # results_events_firms()
    # # 不同特征的公司在上涨下跌市场下的的窗口下的回归结果
    # results_UpDown_firms()
    # # 不同特征的公司在上涨下跌市场下的的窗口下的回归结果
    # results_UpDown_firms()
    # 随机波动率模型参数估计
    results_heston()
    hedge_cost()

    #绘图
    #定义基础数据序列
    #获得指定个股的时间序列数据
    vol_series=get_series_vol(path_vol=PATH_SPX,ticker='SPX',).sort_values('date')
    vol_series.index=np.arange(len(vol_series))
    vol_series['return']=np.log(vol_series['close']/vol_series['close'].shift())
    vol_series=vol_series[vol_series['date']>=20170101]

    # #不同的均值回复速度序列
    # data=pd.DataFrame({
    #     10:vol_series['return']*3+np.random.normal(0,0.04,size=len(vol_series)),
    #     30: vol_series['return'] * 1.5 + np.random.normal(0, 0.02, size=len(vol_series)),
    #     90: vol_series['return'] * 1 + np.random.normal(0, 0.015, size=len(vol_series)),
    # })
    # data.index=vol_series['date'].astype(str)
    # plot_figs(data,xlabel='date',save_path='E:\python_project\Volatility_Mean_Reversion_Regression\数据文件\生成数据\模拟结果\生成图片'+'\不同速度下的均值回复速度序列.png')

    # #不同的均值回复速度序列
    # data=pd.DataFrame({
    #     'higher':vol_series['return']*3+np.random.normal(0.2,0.04,size=len(vol_series)),
    #     'high': vol_series['return'] * 1.5 + np.random.normal(0.1, 0.02, size=len(vol_series)),
    #     'medium': vol_series['return'] * 1 + np.random.normal(0.00, 0.015, size=len(vol_series)),
    #     'low': vol_series['return'] * 1 + np.random.normal(-0.1, 0.015, size=len(vol_series)),
    #     'lower': vol_series['return'] * 1 + np.random.normal(-0.2, 0.015, size=len(vol_series)),
    # })
    # data.index=vol_series['date'].astype(str)
    # data=data*700
    # plot_cols(data, xlabel='date', ylabel='speed',marker=False)


    #绘制概率密度曲线

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings

    warnings.filterwarnings(action='once')

    # Draw Plot
    plt.figure(figsize=(10, 8), dpi=80)
    sns.distplot(vol_series['close'],
                 color="#01a2d9",
                 label="Compact",
                 hist_kws={'alpha': .7},
                 kde_kws={'linewidth': 3})
    plt.ylim(0, 0.35)

    # Decoration
    sns.set(style="whitegrid", font_scale=1.1)
    plt.title('Density Plot of City Mileage by Vehicle Type', fontsize=18)
    plt.legend()
    plt.show()


    k=3












