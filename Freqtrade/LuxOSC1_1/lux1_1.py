
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# ---- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from functools import reduce
import logging
import math

from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

logger = logging.getLogger(__name__)
def LUX_SuperTrendOscillator(dtloc, source = 'close', length = 6, mult = 9, smooth = 1):
    """
    // This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
    // ?? LuxAlgo
      https://www.tradingview.com/script/dVau7zqn-LUX-SuperTrend-Oscillator/
     :return: List of tuples in the format (osc, signal, histogram)   
     translated for freqtrade: viksal1982  viktors.s@gmail.com
    """
    dtSPB = dtloc.copy()
    dtSPB['atrcol'] = np.nan
    dtSPB['hl2col'] = np.nan
    dtSPB['upcol'] = np.nan
    dtSPB['dncol'] = np.nan
    dtSPB['uppercol'] = np.nan
    dtSPB['lowercol'] = np.nan
    dtSPB['trendcol'] = np.nan
    dtSPB['sptcol'] = np.nan
    dtSPB['osc1col'] = np.nan
    dtSPB['osc2col'] = np.nan
    dtSPB['osccol'] = np.nan
    dtSPB['alphacol'] = np.nan
    dtSPB['amacol'] = np.nan
    dtSPB['histcol'] = np.nan




    
    dtSPB['atrcol'] = ta.ATR(dtloc, timeperiod = length) * mult
    dtSPB['hl2col'] =  (dtSPB['high'] + dtSPB['low'] )/2
    dtSPB['upcol'] =  dtSPB['hl2col'] + dtSPB['atrcol']
    dtSPB['dncol'] =  dtSPB['hl2col'] - dtSPB['atrcol']
    def calc_upper(dfr, init=0):
        global calc_Lux_STO_upper
        global calc_Lux_STO_src
        if init == 1:
            calc_Lux_STO_upper = 0.0
            calc_Lux_STO_src = 0.0
            return
        if calc_Lux_STO_src < calc_Lux_STO_upper:
            calc_Lux_STO_upper = min(dfr['upcol'], calc_Lux_STO_upper)
        else:
            calc_Lux_STO_upper = dfr['upcol']
        calc_Lux_STO_src = dfr[source]
        return calc_Lux_STO_upper
    calc_upper(None, init=1)
    dtSPB['uppercol'] = dtSPB.apply(calc_upper, axis = 1)
    def calc_lower(dfr, init=0):
        global calc_Lux_STO_lower
        global calc_Lux_STO_src
        if init == 1:
            calc_Lux_STO_lower = 0.0
            calc_Lux_STO_src = 0.0
            return
        if calc_Lux_STO_src > calc_Lux_STO_lower:
            calc_Lux_STO_lower= max(dfr['dncol'], calc_Lux_STO_lower)
        else:
            calc_Lux_STO_lower = dfr['dncol']
        calc_Lux_STO_src = dfr[source]
        return calc_Lux_STO_lower
    calc_lower(None, init=1)
    dtSPB['lowercol'] = dtSPB.apply(calc_lower, axis = 1)
    def calc_trend(dfr, init=0):
        global calc_Lux_STO_trend
        global calc_Lux_STO_lower
        global calc_Lux_STO_upper
        if init == 1:
            calc_Lux_STO_trend = 0.0
            calc_Lux_STO_lower = 0.0
            calc_Lux_STO_upper = 0.0
            return
        if dfr[source] > calc_Lux_STO_upper:
            calc_Lux_STO_trend = 1
        elif dfr[source] < calc_Lux_STO_lower:
            calc_Lux_STO_trend = 0
        calc_Lux_STO_upper = dfr['uppercol']
        calc_Lux_STO_lower = dfr['lowercol']
        return calc_Lux_STO_trend
    calc_trend(None, init=1)
    dtSPB['trendcol'] = dtSPB.apply(calc_trend, axis = 1)
    dtSPB['sptcol'] = dtSPB['trendcol'] * dtSPB['lowercol'] + (1-dtSPB['trendcol'] ) * dtSPB['uppercol']
    dtSPB['osc1col'] = (dtSPB[source] - dtSPB['sptcol']) / (dtSPB['uppercol'] - dtSPB['lowercol'])
    dtSPB['osc2col'] = np.where(dtSPB['osc1col'] < 1, dtSPB['osc1col'], 1 )
    dtSPB['osccol'] = np.where(dtSPB['osc2col'] > -1, dtSPB['osc2col'], -1)
    dtSPB['alphacol'] = dtSPB['osccol'].pow(2)/length
    def calc_ama(dfr, init=0):
        global calc_Lux_STO_ama
        if init == 1:
            calc_Lux_STO_ama = 0.0
            return
        calc_Lux_STO_ama = calc_Lux_STO_ama + dfr['alphacol'] * (dfr['osccol'] - calc_Lux_STO_ama)
        return calc_Lux_STO_ama
    calc_ama(None, init=1)
    dtSPB['amacol'] = dtSPB.apply(calc_ama, axis = 1)
    dtSPB['histcol'] = ta.EMA((dtSPB['osccol']- dtSPB['amacol']),timeperiod = smooth)

    return dtSPB['osccol'] * 100,  dtSPB['amacol'] * 100 , dtSPB['histcol']  * 100, dtSPB['sptcol']
 
class LuxOSC1_1(IStrategy):

    INTERFACE_VERSION = 2
    minimal_roi = {
        "0": 0.13,
        "33": 0.046,
        "50": 0.024,
        "100": 0
    }


    # Buy hyperspace params:
    buy_params = {
        "cross_buy": -61,
        "length_buy": 33,
        "mult_buy": 99,
        "short_cross": 87,
        "smooth_buy": 30,
    }

    # Sell hyperspace params:
    sell_params = {
        "cross_sell": 70,
    }
    length_buy = IntParameter(2, 50, default= int(buy_params['length_buy']), space='buy')
    mult_buy = IntParameter(2, 100, default= int(buy_params['mult_buy']), space='buy')
    smooth_buy = IntParameter(2, 100, default= int(buy_params['smooth_buy']), space='buy')
    cross_buy = IntParameter(-100, -50, default= int(buy_params['cross_buy']), space='buy')
    cross_sell = IntParameter(-100, 100, default= int(sell_params['cross_sell']), space='sell')
    short_cross = IntParameter(50, 100, default= int(buy_params['short_cross']), space='buy')
    stoploss = -0.145
    trailing_stop = False
   

    timeframe = '5m'
    custom_info = {}
  
    process_only_new_candles = False

  
    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

   
    startup_candle_count: int = 30


    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

 
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }
    
    plot_config = {

        'main_plot': {
            'supertrend': {'color': 'green'},
        },
        'subplots': {

            "OSC": {
                'osc': {'color': 'blue'},
                'signal': {'color': 'orange'},
                'histogram': {'color': 'green'},
            } 
        }
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # for val in self.length_buy.range:
        #     for val_1 in self.mult_buy.range:
        #         dataframe[f'osc_{val}_{val_1}']=ta.EMA(dataframe, short_lenght = val,long_lenght = val_1)
#------------------------------------------------------------------------------------------------------------------------------------------------------------
        #for val in self.length_buy.range:
            #for val_1 in self.mult_buy.range:
                #dataframe[f'osc_{val}_{val_1}'] =LUX_SuperTrendOscillator(dataframe,source='close', length = int(self.length_buy.value), mult =int(self.mult_buy.value), smooth =int(self.smooth_buy.value))

        # for val in self.length_buy.range:
        #     for val_1 in self.mult_buy.range:
        #         for val_2 in self.smooth_buy.range:
        #             dataframe[f'supertrend_{val}_{val_1}_{val_2}'] =LUX_SuperTrendOscillator(dataframe,source='close', length = val, mult =val_1, smooth =val_2)

        # for val in self.length_buy.range:
        #     for val_1 in self.mult_buy.range:
        #         for val_2 in self.smooth_buy.range:
        #             dataframe[f'signal_{val}'] =LUX_SuperTrendOscillator(dataframe,source='close', length = val, mult =val_1, smooth =val_2)

        # for val in self.length_buy.range:
        #     for val_1 in self.mult_buy.range:
        #         for val_2 in self.smooth_buy.range:
        #             dataframe[f'histogram_{val}_{val_1}_{val_2}'] =LUX_SuperTrendOscillator(dataframe,source='close', length = val, mult =val_1, smooth =val_2)

#--------------------------------------------------------------------------------------------------------------------------------------------------------
         for val in self.length_buy.range:
             for val_1 in self.mult_buy.range:
                for val_2 in self.smooth_buy.range:
                    dataframe[f'osc_{val}_{val_1}_{val_2}'],  dataframe[f'signal_{val}_{val_1}_{val_2}'] , dataframe[f'histogram_{val}_{val_1}_{val_2}'],dataframe[f'supertrend_{val}_{val_1}_{val_2}'] =LUX_SuperTrendOscillator(dataframe, length = int(self.length_buy.value),
                    mult = int(self.mult_buy.value), smooth = int(self.smooth_buy.value))




        # for val in self.length_buy.range:
        #     for val_1 in self.mult_buy.range:
        #         for val_2 in self.smooth_buy.range: 
        #             dataframe[f'supertrend_{val}_{val_1}_{val_2}'], 
        #             dataframe[f'osc_{val}_{val_1}'],  
        #             dataframe[f'signal_{val}'] , 
        #             dataframe[f'histogram_{val}_{val_1}_{val_2}']= LUX_SuperTrendOscillator(dataframe,source='close', length = int(self.length_buy.value),
        #           mult = int(self.mult_buy.value), smooth = int(self.smooth_buy.value))                    

        


#------------------------------------------------------------------------------------------------------------------------------------------------------------
        # dataframe['osc'],  dataframe['signal'] , dataframe['histogram'], dataframe['supertrend'] =LUX_SuperTrendOscillator(dataframe, length = int(self.length_buy.value),
        #  mult = int(self.mult_buy.value), smooth = int(self.smooth_buy.value))

         return dataframe
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        condination_long =[]
        condination_long.append(qtpylib.crossed_above(
                dataframe[f'osc_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}'],
                int(self.cross_buy.value)
        ))

        condination_long.append(
            dataframe[f'supertrend_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}']
            > dataframe['close']


        )
        #enter_short
        condination_short =[]
        condination_short.append(qtpylib.crossed_below(
                dataframe[f'osc_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}'],
                int(self.short_cross.value)
        ))

        condination_short.append(
            dataframe[f'supertrend_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}']
            < dataframe['close'])


        dataframe.loc[
            reduce(lambda x, y: x & y,condination_long ),
            "enter_long",
        ] = 1

        dataframe.loc[
            reduce(lambda x, y: x & y,condination_short ),
            "enter_short",
        ] = 1

    
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        condination_long =[]
        condination_long.append(qtpylib.crossed_below(
                dataframe[f'osc_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}'],
                int(self.cross_sell.value)
        ))
        #exit_short
        condination_short =[]
        condination_short.append(qtpylib.crossed_above(
                dataframe[f'osc_{self.length_buy.value}_{self.mult_buy.value}_{self.smooth_buy.value}'],
                int(self.cross_sell.value)
        ))



        dataframe.loc[
                reduce(lambda x, y: x & y, condination_long),
                "exit_long"] = 1
        dataframe.loc[
                reduce(lambda x, y: x & y, condination_short),
                "exit_short"] = 1
        

        return dataframe
    

