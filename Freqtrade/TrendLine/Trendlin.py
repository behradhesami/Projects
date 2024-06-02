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


def detect_trendline(df, window=2):
    # Define the rolling window
    roll_window = window
    # Create new columns for the linear regression slope and y-intercept
    df['slope'] = np.nan
    df['intercept'] = np.nan

    for i in range(window, len(df)):
        x = np.array(range(i-window, i))
        y = df['Close'][i-window:i]
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        df.at[df.index[i], 'slope'] = m
        df.at[df.index[i], 'intercept'] = c

    # Create a boolean mask for trendline support
    mask_support = df['slope'] > 0

    # Create a boolean mask for trendline resistance
    mask_resistance = df['slope'] < 0

    # Create new columns for trendline support and resistance
    df['support'] = np.nan
    df['resistance'] = np.nan

    # Populate the new columns using the boolean masks
    df.loc[mask_support, 'support'] = df['Close'] * df['slope'] + df['intercept']
    df.loc[mask_resistance, 'resistance'] = df['Close'] * df['slope'] + df['intercept']

    return df
class TrendlineStrategy(IStrategy):


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = detect_trendline(dataframe)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['Close'] > dataframe['support']) &
            (qtpylib.crossed_above(dataframe['close'], dataframe['support']))
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['Close'] < dataframe['resistance']) &
            (qtpylib.crossed_below(dataframe['Close'], dataframe['resistance']))
            'exit_long'] = 1
        return dataframe
 

   