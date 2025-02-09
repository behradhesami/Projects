# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from typing import Optional, Union
from datetime import timedelta
import datetime
import logging
from functools import reduce
from typing import Dict

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, merge_informative_pair,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

logger = logging.getLogger(__name__)
# This class is a sample. Feel free to customize it.
class Bolinger(IStrategy):

    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = True

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {

        "0": 0.085
    }

    stoploss = -0.085

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Optimal timeframe for the strategy.
    timeframe = '1h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False



    startup_candle_count: int = 40

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }
    std_dev_multiplier_buy = CategoricalParameter(
        [0.75, 1, 1.25, 1.5, 1.75], default=1.25, space="buy", optimize=True)
    std_dev_multiplier_sell = CategoricalParameter(
        [0.75, 1, 1.25, 1.5, 1.75], space="sell", default=1.25, optimize=True)

    def feature_engineering_expand_all(self, dataframe: DataFrame, period: int,
                                       metadata: Dict, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.
        All features must be prepended with `%` to be recognized by FreqAI internals.
        Access metadata such as the current pair/timeframe with:
        `metadata["pair"]` `metadata["tf"]`
        More details on how these config defined parameters accelerate feature engineering
        in the documentation at:
        https://www.freqtrade.io/en/latest/freqai-parameter-table/#feature-parameters
        https://www.freqtrade.io/en/latest/freqai-feature-engineering/#defining-the-features
        :param dataframe: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        :param metadata: metadata of current pair
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """



        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=period, stds=2.2
        )
        dataframe["bb_lowerband-period"] = bollinger["lower"]
        dataframe["bb_middleband-period"] = bollinger["mid"]
        dataframe["bb_upperband-period"] = bollinger["upper"]

        dataframe["%-bb_width-period"] = (
            dataframe["bb_upperband-period"]
            - dataframe["bb_lowerband-period"]
        ) / dataframe["bb_middleband-period"]
        # dataframe["%-close-bb_lower-period"] = (
        #     dataframe["close"] / dataframe["bb_lowerband-period"]
        # )

        dataframe["%-rsi-period"]=ta.RSI(dataframe, timeperiod=period)

        return dataframe  


    def set_freqai_targets(self, dataframe: DataFrame, metadata: Dict, **kwargs) -> DataFrame:

        """ I Realy Dont Underestand This Sh"""


        dataframe["&-s_close"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["close"]
            - 1
            )



        return dataframe


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe = self.freqai.start(dataframe, metadata, self)

        for val in self.std_dev_multiplier_buy.range:
            dataframe[f'target_roi_{val}'] = (
                dataframe["&-s_close_mean"] + dataframe["&-s_close_std"] * val
                )
        for val in self.std_dev_multiplier_sell.range:
            dataframe[f'sell_roi_{val}'] = (
                dataframe["&-s_close_mean"] - dataframe["&-s_close_std"] * val
                )
        return dataframe


    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        """"""
        df.loc[
            (
                (qtpylib.crossed_above(df['rsi'],70))&
                (df['bb_width-period'] < 0.60)



            ),

            'exit_long'] = 1
        
        df.loc[
            (
                (qtpylib.crossed_above(df['rsi'],70))&
                (df['bb_width-period'] < 0.60)



            ),

            'exit_short'] = 1

        return df


    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                #(qtpylib.crossed_above(dataframe['rsi'],70))&
                #(dataframe['percent'] > 0.60)



            ),

            'exit_long'] = 1
        dataframe.loc[
            (
                #(qtpylib.crossed_above(dataframe['rsi'],70))&
                #(dataframe['percent'] > 0.60)



            ),

            'exit_short'] = 1

        return dataframe

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                proposed_leverage: float, max_leverage: float, entry_tag: Optional[str], side: str,
                **kwargs) -> float:

        return 1