# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:06:28 2021

@author: sozenr
"""

from ta.momentum import rsi,stochrsi
from ta.trend import *
from ta.volatility import donchian_channel_pband
from ta.volatility import BollingerBands
import  numpy as np
import os
from ta.momentum import *
from ta.volume import *

def heikin_ashi_prep(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])

    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)

    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)

    return heikin_ashi_df

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def add_features(data):

    new_data=data.copy()
    indicator_bb = BollingerBands(close=data["close"], window=20, window_dev=2)
    bb_h = indicator_bb.bollinger_hband()
    bb_l = indicator_bb.bollinger_lband()
    new_data["b_perc"]=((new_data.close-bb_l)/(bb_h-bb_l))*100
    new_data["roc"]=ROCIndicator(new_data.close).roc()
    new_data["roc"]=WilliamsRIndicator(new_data.high,new_data.low,new_data.close).williams_r()
    new_data["RSI"]=rsi(new_data.close)

    new_data["RSI6"]=rsi(new_data.close,6)

    new_data["RSI2"]=rsi(new_data.close,2)





    rsi_sma = new_data['RSI6'].rolling(window=14).mean()
    new_data['rsi6_corr_14'] = new_data['close'].rolling(window=14).corr(rsi_sma)
    new_data.loc[new_data['rsi6_corr_14'] < -1, 'rsi6_corr_14'] = -1
    new_data.loc[new_data['rsi6_corr_14'] > 1, 'rsi6_corr_14'] = 1
    rsi_sma = new_data['RSI2'].rolling(window=14).mean()
    new_data['rsi12_corr_14'] = new_data['close'].rolling(window=14).corr(rsi_sma)
    new_data.loc[new_data['rsi12_corr_14'] < -1, 'rsi12_corr_14'] = -1
    new_data.loc[new_data['rsi12_corr_14'] > 1, 'rsi12_corr_14'] = 1

    new_data["stoch"]=stochrsi(new_data.close)


    new_data["dcp"]=donchian_channel_pband(data.high,data.low,data.close)

    sma8 = new_data['close'].rolling(window=8).mean()
    new_data["sma8"]=sma8
    new_data['corr8'] = new_data["sma8"].corr(sma8)
    new_data.loc[new_data['corr8'] < -1, 'corr8'] = -1
    new_data.loc[new_data['corr8'] > 1, 'corr8'] = 1

    sma13 = new_data['close'].rolling(window=13).mean()
    new_data["sma13"]=sma13
    new_data['corr13'] =  new_data["sma13"].corr(sma13)
    new_data.loc[new_data['corr13'] < -1, 'corr13'] = -1
    new_data.loc[new_data['corr13'] > 1, 'corr13'] = 1

    sma21 = new_data['close'].rolling(window=21).mean()
    new_data["sma21"] = sma21
    new_data['corr21'] = new_data["sma21"].corr(sma21)

    new_data.loc[new_data['corr21'] < -1, 'corr21'] = -1
    new_data.loc[new_data['corr21'] > 1, 'corr21'] = 1


    sma34 = new_data['close'].rolling(window=34).mean()
    new_data["sma34"]=sma34
    new_data['corr34'] = new_data['close'].corr(sma34)
    new_data.loc[new_data['corr34'] < -1, 'corr34'] = -1
    new_data.loc[new_data['corr34'] > 1, 'corr34'] = 1


    sma100 = new_data['close'].rolling(window=100).mean()
    new_data["sma100"]=sma100
    new_data['corr100'] =  new_data["sma100"].corr(sma100)
    new_data.loc[new_data['corr100'] < -1, 'corr100'] = -1
    new_data.loc[new_data['corr100'] > 1, 'corr100'] = 1





    # highs=new_data.high.rolling(20).max()
    # lows=new_data.low.rolling(20).min()
    # new_data["highs"]=highs.shift(1)
    # new_data["lows"]=lows.shift(1)

    # new_data.loc[:,"resis"]=0
    # new_data.loc[:,"support"]=0
    #
    #
    #
    # new_data.loc[ (np.abs(new_data["highs"]-new_data["close"])<new_data["close"]*0.0001 ) ,"resis"]=1
    #
    # new_data.loc[ (np.abs(new_data["lows"]-new_data["close"])<new_data["close"]*0.0001 ) ,"support"]=1


    # new_data["high_low_perc"]=((new_data.close-lows)/(highs-lows))*100


    # Create columns 'OO' with the difference between the current minute's open and last minute's open
    # new_data['OO'] = new_data['open'] - new_data['open'].shift(1)

    # Create columns 'OC' with the difference between the current minute's open and last minute's close
    # new_data['OC'] = new_data['open'] - new_data['close'].shift(1)


    # new_data["return"]=new_data["close"].pct_change()
    #
    # new_data["log_change"]=np.log(new_data.close)-np.log(new_data.close.shift(1))


    open=new_data.open
    high=new_data.high
    low=new_data.low
    close=new_data.close

    cols=new_data.columns
    for c in cols[4:]:
        for i in range(1,5):
            new_data[c+"_"+str(i)]=new_data[c].shift(i)
            new_data[c+"_diff_"+str(i)]=new_data[c]-new_data[c].shift(i)


    for i in [8,21,50,100,200]:

        new_data["trend_sma_"+str(i)]=0
        new_data.loc[ (new_data.close>new_data['close'].rolling(window=i).mean() ),"trend_sma_" + str(i)] = 1
        new_data.loc[ (new_data.close<new_data['close'].rolling(window=i).mean() ),"trend_sma_" + str(i)] = -1
        new_data["ratio_trend_sma_"+str(i)] = (new_data["trend_sma_"+str(i)] - new_data['close']) / new_data['close']

    new_data=new_data.drop(columns=["open", "high", "low", "close"])

    return  new_data