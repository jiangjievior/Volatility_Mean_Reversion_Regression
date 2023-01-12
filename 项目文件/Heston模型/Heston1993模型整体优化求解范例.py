import numpy as np

#

r0, kappa_r, theta_r, sigma_r, t, T = 0.04, 0.3, 0.04, 0.1, 0.5, 5.0

#
def gamma(kappa_r, sigma_r):
    ''' Help Function. '''
    return np.sqrt(kappa_r ** 2 + 2 * sigma_r ** 2)


def b1(alpha):
    ''' Help Function. '''
    r0, kappa_r, theta_r, sigma_r, t, T = alpha
    g = gamma(kappa_r, sigma_r)
    return (((2 * g * np.exp((kappa_r + g) * (T - t) / 2)) /
             (2 * g + (kappa_r + g) * (np.exp(g * (T - t)) - 1))) **
            (2 * kappa_r * theta_r / sigma_r ** 2))


def b2(alpha):
    ''' Help Function. '''
    r0, kappa_r, theta_r, sigma_r, t, T = alpha
    g = gamma(kappa_r, sigma_r)
    return ((2 * (np.exp(g * (T - t)) - 1)) /
            (2 * g + (kappa_r + g) * (np.exp(g * (T - t)) - 1)))


def B(alpha):
    ''' Function to value unit zero-coupon bonds in CIR85 Model.

    Parameters
    ==========
    r0: float
        initial short rate
    kappa_r: float
        mean-reversion factor
    theta_r: float
        long-run mean of short rate
    sigma_r: float
        volatility of short rate
    t: float
        valuation date
    T: float
        time horizon/interval

    Returns
    =======
    zcb_value: float
        value of zero-coupon bond
    '''
    b_1 = b1(alpha)
    b_2 = b2(alpha)
    r0, kappa_r, theta_r, sigma_r, t, T = alpha
    # expected value of r_t
    E_rt = theta_r + np.exp(-kappa_r * t) * (r0 - theta_r)
    zcb_value = b_1 * np.exp(-b_2 * E_rt)
    return zcb_value


# Heston/H93模型是最常用的模型之一，有随机波动率和恒定的短期利率
import numpy as np
from scipy.integrate import quad
import sys
import warnings
warnings.simplefilter('ignore')

# H93 Parameters
kappa_v = 18.7885
theta_v = 0.0142
sigma_v = 0.8914
rho = -0.7213
v0 = 0.00093

# General Parameters
S0 = 100
K = 100.0
T = 1
r = 0.05

#
def H93_call_value(S0, K, T, r,
                   kappa_v= 18.7885,
                   theta_v= 0.0142,
                   sigma_v= 0.8914,
                   rho= -0.7213,
                   v0= 0.00093,
                   ):
    ''' Valuation of European call option in H93 model via Lewis (2001)
    Fourier-based approach.

    Parameters
    ==========
    S0: float
        initial stock/index level
    K: float
        strike price
    T: float
        time-to-maturity (for t=0)
    r: float
        constant risk-free short rate
    kappa_v: float
        mean-reversion factor
    theta_v: float
        long-run mean of variance
    sigma_v: float
        volatility of variance
    rho: float
        correlation between variance and stock/index level
    v0: float
        initial level of variance

    Returns
    =======
    call_value: float
        present value of European call option

    '''
    int_value = quad(lambda u: H93_int_func(u, S0, K, T, r, kappa_v,
                                            theta_v, sigma_v, rho, v0),
                     0, np.inf, limit=250)[0]
    call_value = max(0, S0 - np.exp(-r * T) * np.sqrt(S0 * K) /
                     np.pi * int_value)
    return call_value

# 积分函数
def H93_int_func(u, S0, K, T, r, kappa_v, theta_v, sigma_v, rho, v0):
    ''' Valuation of European call option in H93 model via Lewis (2001)
    Fourier-based approach: integration function.

    Parameter definitions see function H93_call_value.'''
    char_func_value = H93_char_func(u - 1j * 0.5, T, r, kappa_v,
                                    theta_v, sigma_v, rho, v0)
    int_func_value = 1 / (u ** 2 + 0.25) \
        * (np.exp(1j * u * np.log(S0 / K)) * char_func_value).real
    return int_func_value

# characteristic functions
# 特征函数
def H93_char_func(u, T, r, kappa_v, theta_v, sigma_v, rho, v0):
    ''' Valuation of European call option in H93 model via Lewis (2001)
    Fourier-based approach: characteristic function.

    Parameter definitions see function BCC_call_value.'''
    c1 = kappa_v * theta_v
    c2 = -np.sqrt((rho * sigma_v * u * 1j - kappa_v) ** 2 -
                  sigma_v ** 2 * (-u * 1j - u ** 2))
    c3 = (kappa_v - rho * sigma_v * u * 1j + c2) \
        / (kappa_v - rho * sigma_v * u * 1j - c2)
    H1 = (r * u * 1j * T + (c1 / sigma_v ** 2) *
          ((kappa_v - rho * sigma_v * u * 1j + c2) * T -
           2 * np.log((1 - c3 * np.exp(c2 * T)) / (1 - c3))))
    H2 = ((kappa_v - rho * sigma_v * u * 1j + c2) / sigma_v ** 2 *
          ((1 - np.exp(c2 * T)) / (1 - c3 * np.exp(c2 * T))))
    char_func_value = np.exp(H1 + H2 * v0)
    return char_func_value


print("H93 Value   %10.4f"
          % H93_call_value(S0, K, T, r, kappa_v, theta_v, sigma_v, rho, v0))


# Calibration of CIR85 model
#
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.interpolate as sci
from scipy.optimize import fmin

mpl.rcParams['font.family'] = 'serif'
np.set_printoptions(suppress=True,
                    formatter={'all': lambda x: '%7.6f' % x})

#

#
t_list = np.array((1, 7, 14, 30, 60, 90, 180, 270, 360)) / 360.
r_list = np.array((-0.032, -0.013, -0.013, 0.007, 0.043,
                   0.083, 0.183, 0.251, 0.338)) / 100

factors = (1 + t_list * r_list)
zero_rates = 1 / t_list * np.log(factors)

r0 = r_list[0]  # 0.0  # set to zero

#
# Interpolation of Market Data
#

tck = sci.splrep(t_list, zero_rates, k=3)  # cubic splines
tn_list = np.linspace(0.0, 1.0, 24)
ts_list = sci.splev(tn_list, tck, der=0)
de_list = sci.splev(tn_list, tck, der=1)

f = ts_list + de_list * tn_list
# forward rate transformation


def plot_term_structure():
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, r_list, 'ro', label='rates')
    # cubic splines
    plt.plot(tn_list, ts_list, 'b', label='interpolation', lw=1.5)
    # first derivative
    plt.plot(tn_list, de_list, 'g--', label='1st derivative', lw=1.5)
    plt.legend(loc=0)
    plt.xlabel('time horizon in years')
    plt.ylabel('rate')


#
# Model Forward Rates
#
def CIR_forward_rate(opt):
    ''' Function for forward rates in CIR85 model.

    Parameters
    ==========
    kappa_r: float
        mean-reversion factor
    theta_r: float
        long-run mean
    sigma_r: float
        volatility factor

    Returns
    =======
    forward_rate: float
        forward rate
    '''
    kappa_r, theta_r, sigma_r = opt
    t = tn_list
    g = np.sqrt(kappa_r ** 2 + 2 * sigma_r ** 2)
    sum1 = ((kappa_r * theta_r * (np.exp(g * t) - 1)) /
            (2 * g + (kappa_r + g) * (np.exp(g * t) - 1)))
    sum2 = r0 * ((4 * g ** 2 * np.exp(g * t)) /
                 (2 * g + (kappa_r + g) * (np.exp(g * t) - 1)) ** 2)
    forward_rate = sum1 + sum2
    return forward_rate

#
# Error Function
#


def CIR_error_function(opt):
    ''' Error function for CIR85 model calibration. '''
    kappa_r, theta_r, sigma_r = opt
    if 2 * kappa_r * theta_r < sigma_r ** 2:
        return 100
    if kappa_r < 0 or theta_r < 0 or sigma_r < 0.001:
        return 100
    forward_rates = CIR_forward_rate(opt)
    MSE = np.sum((f - forward_rates) ** 2) / len(f)
    # print opt, MSE
    return MSE

#
# Calibration Procedure
#


def CIR_calibration():
    opt = fmin(CIR_error_function, [1.0, 0.02, 0.1],
               xtol=0.00001, ftol=0.00001,
               maxiter=300, maxfun=500)
    return opt

#
# Graphical Results Output
#


def plot_calibrated_frc(opt):
    ''' Plots market and calibrated forward rate curves. '''
    forward_rates = CIR_forward_rate(opt)
    plt.figure(figsize=(8, 7))
    plt.subplot(211)
    plt.ylabel('forward rate $f(0,T)$')
    plt.plot(tn_list, f, 'b', label='market')
    plt.plot(tn_list, forward_rates, 'ro', label='model')
    plt.legend(loc=0)
    plt.axis([min(tn_list) - 0.05, max(tn_list) + 0.05,
              min(f) - 0.005, max(f) * 1.1])
    plt.subplot(212)
    wi = 0.02
    plt.bar(tn_list - wi / 2, forward_rates - f, width=wi)
    plt.xlabel('time horizon in years')
    plt.ylabel('difference')
    plt.axis([min(tn_list) - 0.05, max(tn_list) + 0.05,
              min(forward_rates - f) * 1.1, max(forward_rates - f) * 1.1])
    plt.tight_layout()


def plot_zcb_values(p0, T):
    ''' Plots unit zero-coupon bond values (discount factors). '''
    t_list = np.linspace(0.0, T, 20)
    r_list = B([r0, p0[0], p0[1], p0[2], t_list, T])
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, r_list, 'b')
    plt.plot(t_list, r_list, 'ro')
    plt.xlabel('time horizon in years')
    plt.ylabel('unit zero-coupon bond value')


# 模型校准
import pandas as pd
data=pd.read_excel('C:/Users/gws/Desktop/FBM/沪深300虚值.xlsx')
data.head(2)
len(data)

#H93模型校准
# Calibration of Bakshi, Cao and Chen (1997)
import sys
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.optimize import brute, fmin

mpl.rcParams['font.family'] = 'serif'
np.set_printoptions(suppress=True,
                    formatter={'all': lambda x: '%5.3f' % x})

kappa_r, theta_r, sigma_r = CIR_calibration()

S0 = 4.736
r0 = 0.015
t=0

# Option Selection
tol = 0.9  # percent ITM/OTM options
options = data[(np.abs(data['行权价'] - S0) / S0) < tol]
options['交易时间'] = pd.DatetimeIndex(options['交易时间'])
options['到期日'] = pd.DatetimeIndex(options['到期日'])
options


# Adding Time-to-Maturity and Short Rates
for row, option in options.iterrows():
    T = (option['到期日'] - option['交易时间']).days / 365.+0.01
    options.loc[row, 'T'] = T
    B0T = B([kappa_r, theta_r, sigma_r, r0, t,T])
    options.loc[row, 'r'] = -math.log(B0T) / T

## Calibration Functions
i = 0
min_MSE = 0.005


def H93_error_function(p0):
    '''
    Parameters
    ==========
    kappa_v: float
        mean-reversion factor
    theta_v: float
        long-run mean of variance
    sigma_v: float
        volatility of variance
    rho: float
        correlation between variance and stock/index level
    v0: float
        initial, instantaneous variance

    Returns
    =======
    MSE: float
        mean squared error
    '''
    global i, min_MSE
    kappa_v, theta_v, sigma_v, rho, v0 = p0
    if kappa_v < 0.0 or theta_v < 0.005 or sigma_v < 0.0 or \
            rho < -1.0 or rho > 1.0:
        return 0.005
    if 2 * kappa_v * theta_v < sigma_v ** 2:
        return 0.005
    se = []
    for row, option in options.iterrows():
        model_value = H93_call_value(S0, option['行权价'], option['T'],
                                     option['r'], kappa_v, theta_v, sigma_v,
                                     rho, v0)
        se.append((model_value - option['收盘价']) ** 2)
    MSE = sum(se) / len(se)
    min_MSE = min(min_MSE, MSE)
    if i % 25 == 0:
        print('%4d |' % i, np.array(p0), '| %7.3f | %7.3f' % (MSE, min_MSE))
    i += 1
    return MSE


def H93_calibration_full():
    ''' Calibrates H93 stochastic volatility model to market quotes. '''
    # first run with brute force
    # (scan sensible regions)
    p0 = brute(H93_error_function,
               ((0, 10.6, 7.0),  # kappa_v
                (0.01, 1, 0.05),  # theta_v
                (0.05, 5, 0.1),  # sigma_v
                (-0.1, 0.00, 0.3),  # rho
                (0.01, 1, 0.01)),  # v0
               finish=None)

    # second run with local, convex minimization
    # (dig deeper where promising)
    opt = fmin(H93_error_function, p0,
               xtol=0.0001, ftol=0.0001,
               maxiter=500, maxfun=650)

    return opt


def H93_calculate_model_values(p0):
    ''' Calculates all model values given parameter vector p0. '''
    kappa_v, theta_v, sigma_v, rho, v0 = p0
    values = []
    for row, option in options.iterrows():
        model_value = H93_call_value(S0, option['Strike'], option['T'],
                                     option['r'], kappa_v, theta_v, sigma_v,
                                     rho, v0)
        values.append(model_value)
    return np.array(values)

options
data['交易时间'] = pd.DatetimeIndex(data['交易时间'])
data['到期日'] = pd.DatetimeIndex(data['到期日'])
data.head(2)

# %time opt_sv = H93_calibration_full()
# opt_sv#最优参数
#参数设置
S0 =data['标的资产价格']  # initial index level
K = 5.25  # strike level
T = data['剩余到期日'] # call option maturity
r = data['无风险利率']/100 # constant short rate
t=0
# H93模型参数
kappa_v = 18
theta_v = 0.026
sigma_v = 0.978
rho =  -0.821
v0 =0.035

Heston_value=[]
for i in range(len(data)):
    Heston_value.append(H93_call_value(S0[i], K, T[i], r[i], kappa_v, theta_v, sigma_v, rho, v0))


# # Heston_value
# Heston_value
# a = Heston_value
# # from tkinter import _flatten
# b=list(_flatten(a))
# pred=b
# # pred


# label=data['收盘价']
# # mape
# mape=np.mean(np.abs((pred-label)/label))
# # rmse
# rmse=np.sqrt(np.mean(np.square(pred-label)))
# # mae
# mae=np.mean(np.abs(pred-label))
# #MSE
# mse=np.sum((label-pred)**2)/len(pred)
# print('Heston模型测试集的mape:',mape,' rmse:',rmse,' mae:',mae,'MSE:',mse)

# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# import matplotlib.pyplot as plt
# plt.figure(figsize=(12,10))
# pred=pd.DataFrame(pred)
# plt.plot(pred[230:],label='Heston lewis')
# (data['收盘价'][230:]).plot(label='option value')
# plt.xlabel('days')
# plt.ylabel('option value')
# plt.grid()
# plt.legend()
# plt.grid()
# plt.show()

