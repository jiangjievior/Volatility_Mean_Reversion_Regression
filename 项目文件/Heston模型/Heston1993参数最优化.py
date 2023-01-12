import numpy as np
import pandas as pd
from scipy.integrate import quad
import sys
import math
import warnings

from 项目文件.Heston模型.Heston1993期权定价计算公式 import H93_call_value

warnings.simplefilter('ignore')
import scipy.interpolate as sci
from scipy.optimize import brute, fmin

np.set_printoptions(suppress=True,
                    formatter={'all': lambda x: '%5.3f' % x})


class Calibrate_Heston_1993():

    def __init__(self,option
                 ):
        self.option = option  # 期权数据
        self.min_MSE=10000
        self.params_min_MSE=()
        self.i=0
        pass


    def MSE_heston_1993(self, p0: tuple):
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
        #不满足以下关系，本次运行无效
        if kappa_v < 0.0 or theta_v < 0.005 or sigma_v < 0.0 or \
                rho < -1.0 or rho > 1.0:
            return 0.005
        if 2 * kappa_v * theta_v < sigma_v ** 2:
            return 0.005
        self.option['close_pred']=self.option.apply(lambda data:H93_call_value(data['UnderlyingPrice'], data['Strike'], data['years'],
                                         data['rate_risk_free'], kappa_v, theta_v, sigma_v,
                                         rho, v0),axis=1)


        MSE = sum((self.option['close_pred'] - self.option['close']) ** 2)/len(self.option)
        if self.min_MSE > MSE: self.params_min_MSE = p0
        self.min_MSE = min(self.min_MSE, MSE)
        if self.i % 25 == 0:
            print('%4d |' % self.i, np.array(p0), '| %7.3f | %7.3f' % (MSE, self.min_MSE),f'最优参数：{np.array(self.params_min_MSE)}')
        self.i += 1
        return MSE

    def H93_calibration_full(self):
        ''' Calibrates H93 stochastic volatility model to market quotes. '''
        # first run with brute force
        # (scan sensible regions)
        p0 = brute(self.MSE_heston_1993,
                   ((0, 10.6, 6.0),  # kappa_v
                    (0.01, 1, 0.05),  # theta_v
                    (0.05, 5, 0.1),  # sigma_v
                    (-0.1, 0.00, 0.3),  # rho
                    (0.01, 1, 0.01)),  # v0
                   finish=None)

        # second run with local, convex minimization
        # (dig deeper where promising)
        opt = fmin(self.MSE_heston_1993, p0,
                   xtol=0.0001, ftol=0.0001,
                   maxiter=500, maxfun=650)

        return opt


kappa_v = 18.7885,
theta_v = 0.0142,
sigma_v = 0.8914,
rho = -0.7213,
v0 = 0.00093,





















