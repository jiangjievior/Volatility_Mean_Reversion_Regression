import pandas as pd
import numpy as np
import copy
from 数据文件.基本参数 import *


#获取个股公司的财务比率
def finance_ratio_stock(
        tickers=[],
        name_fin=[],
        # ['gvkey', 'permno', 'adate', 'qdate', 'public_date', 'CAPEI', 'bm',
        #  'evm', 'pe_op_basic', 'pe_op_dil', 'pe_exi', 'pe_inc', 'ps', 'pcf',
        #  'dpr', 'npm', 'opmbd', 'opmad', 'gpm', 'ptpm', 'cfm', 'roa', 'roe',
        #  'roce', 'efftax', 'aftret_eq', 'aftret_invcapx', 'aftret_equity',
        #  'pretret_noa', 'pretret_earnat', 'GProf', 'equity_invcap',
        #  'debt_invcap', 'totdebt_invcap', 'capital_ratio', 'int_debt',
        #  'int_totdebt', 'cash_lt', 'invt_act', 'rect_act', 'debt_at',
        #  'debt_ebitda', 'short_debt', 'curr_debt', 'lt_debt', 'profit_lct',
        #  'ocf_lct', 'cash_debt', 'fcf_ocf', 'lt_ppent', 'dltt_be', 'debt_assets',
        #  'debt_capital', 'de_ratio', 'intcov', 'intcov_ratio', 'cash_ratio',
        #  'quick_ratio', 'curr_ratio', 'cash_conversion', 'inv_turn', 'at_turn',
        #  'rect_turn', 'pay_turn', 'sale_invcap', 'sale_equity', 'sale_nwc',
        #  'rd_sale', 'adv_sale', 'staff_sale', 'accrual', 'ptb', 'PEG_trailing',
        #  'divyield', 'TICKER', 'cusip']
):
    finance_ratio=pd.read_csv(PATH_FINANCIAL_RATIO)
    finance_ratio_=finance_ratio.loc[:,['TICKER', 'cusip', 'public_date']+name_fin]

    return finance_ratio_.rename(columns={'TICKER':'ticker','public_date':'date'})

















