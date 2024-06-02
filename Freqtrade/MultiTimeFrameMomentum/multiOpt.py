# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
from functools import reduce
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from typing import Dict, Union
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib
import logging

from freqtrade.strategy.informative_decorator import informative
logger = logging.getLogger(__name__)

class multi3_Opt(IStrategy):
   
    INTERFACE_VERSION = 3

    timeframe = '5m'

    minimal_roi = {
        "0": 0.1,
    }
    
    informative_timeframe = '1h'
    informative_timeframe2 = '15m'
   

    can_short= True
    stoploss = -0.1
    trailing_stop = False   

    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False


    buy_params={
        "fastk_period":5,
        "fastd_period":3,
        "fast_mac":12,
        "slow_mac":26,
        "signal_period":9,
        "rsi_period":14

    }    
    
    rsi_period = IntParameter(5, 100, default=int(buy_params["rsi_period"]),space ='buy') #RSi 
    macd_period = IntParameter(2, 25, default=int(buy_params["fast_mac"]),space ='buy') #macd
    macdsignal_period= IntParameter(2,25, default =int(buy_params['slow_mac']),space ='buy') #macd
    signal_period = IntParameter(5, 25, default=int(buy_params["signal_period"]),space ='buy') #macd
    fastk_period = IntParameter(5, 25, default=int(buy_params["fastk_period"]),space ='buy') #stoch
    fastd_period = IntParameter(3, 25, default=int(buy_params["fastd_period"]),space ='buy') #stoch


    @informative('1h')
    def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Get the 14 day rsi
        dataframe[f'rsi'] = ta.RSI(dataframe, timeperiod=14)
        # Calculate MACD
        macd_default = (12, 26, 9)
  
        macd = ta.MACD(dataframe, *macd_default)
        dataframe[f'macd'] = macd['macd']
        dataframe[f'macd_signal'] = macd['macdsignal']


        # Calculate Stochastic Oscillator
        stoch = ta.STOCHF(dataframe, 5,3,3)
        dataframe[f'fastk'] = stoch['fastk']
        dataframe[f'fastd'] = stoch['fastd']

        return dataframe
   


    @informative('15m')
    def populate_indicators_5m(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe[f'rsi'] = ta.RSI(dataframe, timeperiod=14)

        macd_default = (12, 26, 9)
        macd = ta.MACD(dataframe, *macd_default)
        dataframe[f'macd'] = macd['macd']
        dataframe[f'macd_signal'] = macd['macdsignal']


        stoch = ta.STOCHF(dataframe, 5,3,3)
        dataframe[f'fastk'] = stoch['fastk']
        dataframe[f'fastd'] = stoch['fastd']
        return dataframe



    

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
#-----------------------RSI-----------------------------       
        for val in self.rsi_period.range:
            dataframe[f'rsi_{val}'] = ta.RSI(dataframe, timeperiod = val)


#-----------------------MACD--------------------------------
        for val in self.macd_period.range:
            for val_1 in self.macdsignal_period.range:
                for val_2 in self.signal_period.range:
                    dataframe[f'macd_{val}_{val_1}_{val_2}'] = ta.MACD(dataframe, fast_period = val, slow_period = val_1, signal_period = val_2)['macd']
                    dataframe[f'macdsignal_{val}_{val_1}_{val_2}'] = ta.MACD(dataframe, fast_period = val, slow_period = val_1, signal_period = val_2)['macdsignal']
                    
#-----------------------STOCHF--------------------------------

        for val in self.fastk_period.range:
            for val_1 in self.fastd_period.range:
                dataframe[f'fastk_{val}_{val_1}'] = ta.STOCHF(dataframe, fastk_period=val, fastd_period=val_1)["fastk"]
                dataframe[f'fastd_{val}_{val_1}'] = ta.STOCHF(dataframe, fastk_period=val, fastd_period=val_1)["fastd"]



        return dataframe
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        condition_long = []

        condition_long.append((dataframe[f'rsi_{self.rsi_period.value}_{self.informative_timeframe}'] < 46))


        dataframe.loc[
            reduce(lambda x, y: x & y, condition_long),
            "enter_long",
        ] = 1
        
        # dataframe.loc[

        #     (dataframe[f'rsi_{self.informative_timeframe}'] < 46)& 
        #     (dataframe[f'macd_{self.informative_timeframe}'] > dataframe[f'macd_signal_{self.informative_timeframe}']) &
        #     (dataframe[f'fastk_{self.informative_timeframe}'] > dataframe[f'fastd_{self.informative_timeframe}'])& 
        #     (dataframe[f'fastk_{self.informative_timeframe}'] < 72) &
        #     (dataframe[f'rsi_{self.informative_timeframe2}'] < 45) &
        #     (dataframe[f'macd_{self.informative_timeframe2}'] > dataframe[f'macd_signal_{self.informative_timeframe2}'])&
        #     #(dataframe[f'fastk_{self.informative_timeframe2}'] > dataframe[f'fastd_{self.informative_timeframe2}']) &
        #     (dataframe[f'fastk_{self.informative_timeframe2}'] < 80) &
        #     (dataframe['rsi'] < 50) & 
        #     (dataframe['macd'] > dataframe['macd_signal']) &
        #     (dataframe['fastk'] > dataframe['fastd']) &
        #     (dataframe['fastk'] < 70) 
        #     ,'enter_long'] = 1
        

        # dataframe.loc[

        #     (dataframe[f'rsi_{self.informative_timeframe}'] > 46)& 
        #     (dataframe[f'macd_{self.informative_timeframe}'] < dataframe[f'macd_signal_{self.informative_timeframe}']) &
        #     (dataframe[f'fastk_{self.informative_timeframe}'] < dataframe[f'fastd_{self.informative_timeframe}'])&
        #     (dataframe[f'fastk_{self.informative_timeframe}'] > 72) &
        #     (dataframe[f'rsi_{self.informative_timeframe2}'] > 45) &
        #     (dataframe[f'macd_{self.informative_timeframe2}'] < dataframe[f'macd_signal_{self.informative_timeframe2}'])&
        #     # #(dataframe[f'fastk_{self.informative_timeframe2}'] > dataframe[f'fastd_{self.informative_timeframe2}']) &
        #     #(dataframe[f'fastk_{self.informative_timeframe2}'] > 80)  ## Errore
        #     (dataframe['rsi'] > 50) &
        #     (dataframe['macd'] < dataframe['macd_signal']) &
        #     (dataframe['fastk'] < dataframe['fastd']) 
        #     #(dataframe['fastk'] > 70) ## Errore
        #     , 'enter_short'] = 1
        
        return dataframe
        
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            
                (
                   
                    #dataframe['sma_50'] <= dataframe['sma_200'] 

                ),
                'exit_long'] = 1
       
        

        
        return dataframe

