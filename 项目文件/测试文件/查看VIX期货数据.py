import numpy as np
import pandas as pd




future=pd.read_csv("F:\金融数据\美国个股数据\个股期货.csv")


future=future[future['ticker']=='VIX']

'VIX' in future['ticker'].str[:1]

tickers=future['ticker'].unique()

np.sort(tickers)
tickers[pd.DataFrame(tickers)[0]=='VIX']






