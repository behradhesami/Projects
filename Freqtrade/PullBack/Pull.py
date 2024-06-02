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


class Pull(IStrategy):
   
    INTERFACE_VERSION = 3

    
    timeframe = '5m'

    minimal_roi = {
        "0":0.01
    }
    

   

    can_short =True
    stoploss = -0.01
    trailing_stop = False   

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    
   

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        #dataframe['entry_long'] = 0
        #dataframe['entry_short'] = 0
        #dataframe['entry_candle_high'] = 0.0
        #dataframe['entry_candle_low'] = 0.0
        #dataframe['entry_candle_close'] = 0.0
        #dataframe['entry_candle_open'] = 0.0


        dataframe.loc[
            
                (
                   
                   (dataframe['close'].shift(1) > dataframe['open'].shift(1))&
                   (dataframe['low'] < dataframe['low'].shift(1))&
                   (dataframe['close'] > dataframe['high'].shift(1))     
                ),
                'enter_long'] =1

        
#_____________________________________SHORT CONDITION________________________________        
            
        dataframe.loc[
            
                (
                   
                   (dataframe['close'].shift(1) > dataframe['open'].shift(1))&
                   (dataframe['high'] > dataframe['high'].shift(1))&
                   (dataframe['close'] < dataframe['low'].shift(1))     
                ),
                'enter_short'] =1
        return dataframe
  
        



    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['entry_candle_low'] = 0.0
        dataframe['entry_candle_high'] = 0.0

    #LONG CONDITION 
        long_exit_condition = (
                (dataframe['close'].shift(1) > dataframe['open'].shift(1))&
                (dataframe['low'] < dataframe['low'].shift(1))&
                (dataframe['close'] > dataframe['high'].shift(1))     

                )
        short_exit_condition =(
            (dataframe['close'].shift(1) > dataframe['open'].shift(1))&
            (dataframe['high'] > dataframe['high'].shift(1))&
            (dataframe['close'] < dataframe['low'].shift(1))     


        )
    #SAVE THE CANDLE
        if long_exit_condition:
            dataframe.all['entry_candle_low'] =dataframe['low']
        if short_exit_condition:
            dataframe.all['entry_candle_high']= dataframe['high']
        # dataframe.loc[long_exit_condition, 'entry_candle_low'] = dataframe['low']
        # dataframe.loc[short_exit_condition, 'entry_candle_high'] = dataframe['high']
        

        dataframe.loc[
            
                (
                    dataframe['close'] < dataframe['entry_candle_low']


                ),
                'exit_long'] = 1
       
     
        
            
        dataframe.loc[
              
                (
                    
                    dataframe['close'] > dataframe['entry_candle_high']
 
                ),
                'exit_short'] = 1
        
        return dataframe
        
