# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class zemastoch1_1(IStrategy):
   
    INTERFACE_VERSION = 3

    
    timeframe = '5m'

    minimal_roi = {
        "0":0.02 #0.5  5 %
    }
    

   


    stoploss = -0.04 #1  ta 10% 
    trailing_stop = False   

    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    
   

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod =20) #5 ta 50 
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod =50) #10 ta 100
        sag = ta.STOCHRSI(dataframe, timeperiod =14,fastk_period =5 , fastd_period =3) #timepriod  7 ta 25 , fastk 2 ta 7 , fastd 2 ta 5 
        dataframe['fastk'] = sag['fastk']
        dataframe['fastd'] = sag['fastd']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       
        dataframe.loc[
            
                (
                    (qtpylib.crossed_below(dataframe['ema20'],dataframe['ema50']))&
                    (dataframe['fastd'] < dataframe['fastk'])

                    #(qtpylib.crossed_above(dataframe['ema20'],dataframe['ema50']))&
                    #(dataframe['fastd'] < dataframe['fastk']) 
                      
                ),
                'enter_long',] = 1
       
        dataframe.loc[
            
                (
                    (qtpylib.crossed_above(dataframe['ema20'],dataframe['ema50']))&
                    (dataframe['fastd'] > dataframe['fastk'])

                    #(qtpylib.crossed_below(dataframe['ema20'],dataframe['ema50']))&
                    #(dataframe['fastd'] > dataframe['fastk']) 
                     
                ),
                'enter_short'] =1
        return dataframe
  
        
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            
                (
                    #(qtpylib.crossed_below(dataframe['close'],dataframe['ema50']))
                    #(qtpylib.crossed_above(dataframe['ema20'],dataframe['ema50']))


                ),
                'exit_long'] = 1
       
        
        dataframe.loc[
              
                (
                    #(qtpylib.crossed_above(dataframe['close'],dataframe['ema50']))
                    #(qtpylib.crossed_below(dataframe['ema20'],dataframe['ema50']))
                    
                ),
                ['exit_short']] = 1
        
        return dataframe
        