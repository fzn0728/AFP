# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:48:40 2017

@author: Sibo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


###############################################################################
############################# Global Plot Setting #############################
###############################################################################

plt.rcParams['figure.figsize'] = (10,8)
# font
plt.rcParams['font.sans-serif']=['Fira Sans OT']
plt.rcParams['font.size'] = 15
plt.rcParams['legend.fontsize'] = 'medium'
# tick label spacing and tick width
plt.rcParams['xtick.major.pad'] = 4
plt.rcParams['ytick.major.pad'] = 5
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1
# legend style
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.numpoints'] = 3
# color
gray = "444444"
plt.rcParams['axes.facecolor'] = 'f5f5f5'
plt.rcParams['axes.edgecolor'] = gray
plt.rcParams['grid.linestyle'] = '-'
plt.rcParams['grid.alpha'] = .8
plt.rcParams['grid.color'] = 'white'
plt.rcParams['grid.linewidth'] = 2
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['axes.labelcolor'] = gray
plt.rcParams['text.color'] = gray
plt.rcParams['xtick.color'] = gray
plt.rcParams['ytick.color'] = gray


###############################################################################
##################################### Code ####################################
###############################################################################

############################### Stock Return Data #############################

# load data
Ret_Raw = pd.read_csv('../02. Data/return.csv')

# some gvkeys might have multiple series of tickers, keep only 01 
temp_ret = Ret_Raw.copy()
temp_ret = temp_ret[temp_ret.iid == '01']
print(len(temp_ret.tic.unique())) # number of ticker left
# change index to datetime
temp_ret['Date'] = pd.to_datetime(temp_ret.datadate, format='%Y%m%d', errors='ignore')
temp_ret.index = temp_ret.Date
temp_ret = temp_ret.drop('Date', axis=1)
# change return from % to number
temp_ret['trt1m'] = temp_ret['trt1m'] / 100

# get a return df for all stocks
temp = {}
for ticker, group in temp_ret.groupby(by='tic'):
    temp[ticker] = group

# store data in a 3-dimensional array using panel function 
pan = pd.Panel(temp)
# return slice of panel along minor axis
Ret = pan.minor_xs('trt1m')   
    
del [temp, temp_ret]

############################# Fama French Return Data #########################

# load data
Ret_FF_Raw = pd.read_csv('../02. Data/F-F_Research_Data_Factors.csv')

# create a FF return copy to use
temp_ret = Ret_FF_Raw.copy()
# use part of df only after Jan 1995
loc = np.where(temp_ret.Date == 199501)[0][0]
temp_ret = temp_ret.iloc[loc:]
# change index and drop useless columns
temp_ret.index = Ret.index
temp_ret = temp_ret.drop(['Date','RF'], axis=1)
# change return from % to number
temp_ret = temp_ret / 100

Ret_FF = temp_ret.copy()
del temp_ret


