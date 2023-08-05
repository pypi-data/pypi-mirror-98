# Copyright (C) 2019 - 2021 Richard Kemp
# $Id: 382620e198b1f77c84c8de0f5437723ef095b463 $
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Timeseries Module.

Provide:
    - TimeFrame Enum
    - TimeSeries Class
"""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id: 382620e198b1f77c84c8de0f5437723ef095b463 $"
__all__ = [
    "TimeFrame",
    "TimeSeries",
]

from enum import Enum

from pandas import DataFrame

from ..lib.flexarray import FlexArray


class TimeFrame(Enum):
    """Standard trading timeframes in seconds.

    Members:
        S: 1 second
        M1: 1 minute
        M5: 5 minutes
        M15: 15 minutes
        M30: 30 minutes
        H1: 1 hour
        H4: 4 hours
        D1: 1 day
        W1: 1 week
        MN: 1 month

    Ref:
        https://docs.mql4.com/constants/chartconstants/enum_timeframes
    """
    S = 1
    M1 = 60
    M5 = 5 * 60
    M15 = 15 * 60
    M30 = 30 * 60
    H1 = 60 * 60
    H4 = 240 * 60
    D1 = 1440 * 60
    W1 = 10080 * 60
    MN = 43200 * 60


class TimeSeries(FlexArray):
    """TimeSeries Class.

    A classic financial timeseries representation, normalized for internal
    library usage.

    Attributes:
        instrument (str): name of the instrument data belongs to.
        timeframe (TimeFrame): data timeframe scale.
        data (DataFrame): pandas DataFrame representation of data.
    """
    def __init__(self, instrument: str, timeframe: TimeFrame,
                 dataframe: DataFrame) -> None:
        """Class Initializer.

        Args:
            instrument: name of the instrument data belongs to.
            timeframe: data timeframe scale.
            dataframe: pandas DataFrame representation of data.
        """
        self.instrument = instrument
        self.timeframe = timeframe
        self.data = dataframe

        super().__init__(dataframe)
