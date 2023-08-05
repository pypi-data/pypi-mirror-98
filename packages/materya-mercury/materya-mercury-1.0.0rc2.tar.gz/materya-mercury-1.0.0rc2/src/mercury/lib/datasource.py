# -*- coding: utf-8; py-indent-offset:4 -*-
# Copyright (C) 2019 - 2021 Richard Kemp

"""Mercury DataSource module.

Provide:
    - DataSource Interface
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id: 7c2ab42fd75b50e6144dce81dac08656140d844b $"
__all__ = [
    "DataSource",
]


from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime
from typing import Dict


from ..core.timeseries import TimeFrame, TimeSeries


class DataSource(object, metaclass=ABCMeta):
    """DataSource Interface.

    A datasource is a way to retrieve fresh trading data (typically OHLC) from
    a specific source.
    """
    @abstractproperty
    def colsmap(self) -> Dict[str, str]:
        """Columns mapping dictionary.

        Provide a mapping to translate raw time series columns name
        to Mercury DataSource naming convention.

        Expect standard names like "open", "high", "low", "close", "adj_close"
        and "volume".
        """

    @abstractmethod
    def get_timeseries(self, from_date: datetime, to_date: datetime,
                       instrument: str, timeframe: TimeFrame) -> TimeSeries:
        """Retrieve a given timeseries from the datasource.

        Args:
            from_date: timeseries starting date.
            to_date: timeseries last date.
            instrument: target instrument.
            timeframe: target timeframe.

        Returns:
            An Mercury TimeSeries.

        Raises:
            IndexError: The requested time range cannot be satisfied.
        """
