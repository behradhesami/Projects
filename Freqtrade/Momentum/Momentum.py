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


class Momentum_DF(IStrategy):
   
    INTERFACE_VERSION = 3

    
    timeframe = '5m'

    minimal_roi = {
        "0": 0.186,
        "16": 0.028,
        "68": 0.011,
        "151": 0
    }
    

   


    stoploss = -0.261 
    trailing_stop = False   

    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    
   

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
#----------------------STOCH-------------------------------       
        dataframe['sma_50'] = qtpylib.sma(dataframe['close'], window=50)
        dataframe['sma_200'] = qtpylib.sma(dataframe['close'], window=200)



        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       
        dataframe.loc[
            (
                dataframe['sma_50'] > dataframe['sma_200']  
            )
            
                ,
                'enter_long',] = 1
       

        return dataframe
  
        
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            
                (
                   
                    dataframe['sma_50'] <= dataframe['sma_200'] 

                ),
                'exit_long'] = 1
       
        

        
        return dataframe
        