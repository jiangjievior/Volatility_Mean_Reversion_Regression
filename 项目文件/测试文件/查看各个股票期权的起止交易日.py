import pandas as pd
import os
from 数据文件.基本参数 import *
from 项目文件.测试文件.研究波动率的过去变化与未来变化之间的关系 import RelationFutureAndPast

paths_surface=os.listdir(PATH_FOLDER_VOL_SURFACE)

results=[]
files=[]
error=[]
for file in paths_surface:
    try:
        if os.path.getsize(os.path.join(PATH_FOLDER_VOL_SURFACE,file))/1024>1985:

            surface = pd.read_csv(os.path.join(PATH_FOLDER_VOL_SURFACE,file))
            surface_days_delta = surface[(surface['days'] == 30) & (surface['delta'] == 50)]
            surface_days_delta.index = range(len(surface_days_delta))

            RFAP=RelationFutureAndPast(surface=surface_days_delta,)
            result_up,result_down=RFAP.run(num_past=30, num_future=30)
            result=pd.concat([result_up,result_down],axis=1)
            result.reset_index(inplace=True)

            results.append(result)
            files.append(file[:-4])

            print(f'已经完成{file}')
    except:
        error.append(file)
        continue
results_=pd.concat(results,keys=files)
results_.to_csv(r'E:\python_project\波动率的均值回复特征\数据文件\生成数据\550只主要个股期权分组回归结果.csv',encoding='utf_8_sig')












