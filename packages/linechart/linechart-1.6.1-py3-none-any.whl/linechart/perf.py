# Copyright 2017 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd

from quantrocket.blotter import read_pnl_csv
from quantrocket.moonshot import read_moonshot_csv

from .utils import *
from .utils import trim_outliers as trim_outliers_func
from .exceptions import InsufficientData, MoonchartError


class DailyPerformance(object):
    """
    Class representing daily performance and derived statistics.

    Typically constructed using DailyPerformance.from_moonshot_csv.

    Parameters
    ----------
    returns : DataFrame, required
        a Dataframe of pct returns

    pnl : DataFrame, optional
        a DataFrame of pnl

    net_exposures : DataFrame, optional
        a Dataframe of net (hedged) exposure

    abs_exposures : DataFrame, optional
        a Dataframe of absolute exposure (ignoring hedging)

    total_holdings : DataFrame, optional
        a Dataframe of the number of holdings

    turnover : DataFrame, optional
        a DataFrame of turnover, that is, changes to positions

    commission_amounts : DataFrame, optional
        a DataFrame of commission amounts, in the base currency

    commissions : DataFrame, optional
        a DataFrame of commissions, as a proportion of capital

    slippages : DataFrame, optional
        a DataFrame of slippages, as a proportion of capital

    benchmark : Series, optional
        a Series of prices for a benchmark

    riskfree : float, optional
        the riskfree rate (default 0)

    compound : bool
         True for compound/geometric returns, False for arithmetic returns (default True)

    rolling_sharpe_window : int, optional
        compute rolling Sharpe over this many periods (default 200)

    trim_outliers: int or float, optional
        discard returns that are more than this many standard deviations from the mean
    """

    def __init__(
        self,
        returns,
        results=None,
        pnl=None,
        net_exposures=None,
        abs_exposures=None,
        total_holdings=None,
        turnover=None,
        commission_amounts=None,
        commissions=None,
        slippages=None,
        benchmark=None,
        riskfree=0,
        compound=True,
        rolling_sharpe_window=200,
        trim_outliers=None,
        weights=None,
    ):

        self.returns = returns
        if len(self.returns.index) < 2:
            raise InsufficientData(
                "Moonchart needs at least 2 dates to analyze performance, "
                "but returns DataFrame has length {0}".format(len(self.returns.index)))
        self._trim_outliers = trim_outliers
        if self._trim_outliers:
            self.returns = trim_outliers_func(returns, z_score=trim_outliers)
        else:
            # warn the user if there are >10-sigma returns
            z_scores = get_zscores(returns)
            max_zscore = z_scores.abs().max()
            if isinstance(returns, pd.DataFrame):
                max_zscore = max_zscore.max()
            if max_zscore > 20:
                import warnings
                warnings.warn("Found returns which are {0} standard deviations from the "
                              "mean, consider removing them with the `trim_outliers` parameter".format(
                                  round(max_zscore)))
        self.pnl = pnl
        self.results = results
        self.net_exposures = net_exposures
        self.abs_exposures = abs_exposures
        self.total_holdings = total_holdings
        self.turnover = turnover
        self.commission_amounts = commission_amounts
        self.commissions = commissions
        self.slippages = slippages
        self.riskfree = riskfree
        self.compound = compound
        self.rolling_sharpe_window = rolling_sharpe_window
        self.weights = weights
        self.returns_longs = None if self.weights is None else self.returns[self.weights > 0]
        self.returns_shorts = None if self.weights is None else self.returns[self.weights < 0]
        self._benchmark_prices = benchmark
        self._benchmark_returns = None
        self._benchmark_cum_returns = None
        self._cum_returns = None
        self._cum_commissions = None
        self._cum_slippages = None
        self._cum_commission_amounts = None
        self._sharpe = None
        self._rolling_sharpe = None
        self._cagr = None
        self._drawdowns = None
        self._max_drawdown = None
        self._cum_pnl = None
        self._average_holding_periods_pos = None
        self._average_holding_periods_null = None
        self._top_movers = None
        self._bar_size = None
        self._cagr_shorts = None
        self._cagr_longs = None
        self._cum_returns_shorts = None
        self._cum_returns_longs = None

    @classmethod
    def _from_moonshot_or_pnl(cls, results,
                              start_date=None,
                              end_date=None,
                              trim_outliers=None,
                              how_to_aggregate=None,
                              riskfree=0,
                              compound=True,
                              rolling_sharpe_window=200):
        """
        Creates a DailyPerformance instance from a moonshot backtest results
        DataFrame or a PNL DataFrame.
        """
        if "Time" in results.index.names:
            results = intraday_to_daily(results, how=how_to_aggregate)

        if start_date:
            results = results[results.index.get_level_values("Date") >= start_date]

        if end_date:
            results = results[results.index.get_level_values("Date") <= end_date]

        fields = results.index.get_level_values("Field").unique()
        kwargs = dict(
            trim_outliers=trim_outliers,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window
        )
        kwargs["results"] = results
        kwargs["returns"] = results.loc["Return"]

        if "Pnl" in fields:
            kwargs["pnl"] = results.loc["Pnl"]
        if "NetExposure" in fields:
            kwargs["net_exposures"] = results.loc["NetExposure"]
        if "AbsExposure" in fields:
            kwargs["abs_exposures"] = results.loc["AbsExposure"]
        if "TotalHoldings" in fields:
            kwargs["total_holdings"] = results.loc["TotalHoldings"]
        if "Turnover" in fields:
            kwargs["turnover"] = results.loc["Turnover"]
        if "Commission" in fields:
            kwargs["commissions"] = results.loc["Commission"]
        if "CommissionAmount" in fields:
            kwargs["commission_amounts"] = results.loc["CommissionAmount"].astype(np.float64)
        if "Slippage" in fields:
            kwargs["slippages"] = results.loc["Slippage"]
        if "Benchmark" in fields:
            kwargs["benchmark"] = results.loc["Benchmark"]
        if "Weight" in fields:
            kwargs["weights"] = results.loc["Weight"]

        return cls(**kwargs)

    @classmethod
    def from_moonshot_csv(cls, filepath_or_buffer,
                          start_date=None,
                          end_date=None,
                          trim_outliers=None,
                          how_to_aggregate=None,
                          riskfree=0,
                          compound=True,
                          rolling_sharpe_window=200):
        """
        Creates a DailyPerformance instance from a Moonshot backtest results CSV.

        Parameters
        ----------
        filepath_or_buffer : str or file-like object
            filepath or file-like object of the CSV

        start_date : str (YYYY-MM-DD), optional
            truncate at this start date (otherwise include entire date range)

        end_date : str (YYYY-MM-DD), optional
            truncate at this end date (otherwise include entire date range)

        trim_outliers: int or float, optional
            discard returns that are more than this many standard deviations from
            the mean. Useful for dealing with data anomalies that cause large
            spikes in plots.

        how_to_aggregate : dict, optional
            a dict of {fieldname: aggregation method} specifying how to aggregate
            fields from intraday to daily. See the docstring for
            `moonchart.utils.intraday_to_daily` for more details.

        riskfree : float, optional
            the riskfree rate (default 0)

        compound : bool
             True for compound/geometric returns, False for arithmetic returns (default True)

        rolling_sharpe_window : int, optional
            compute rolling Sharpe over this many periods (default 200)

        Returns
        -------
        DailyPerformance

        Examples
        --------
        Plot cumulative returns:

        >>> perf = DailyPerformance.from_moonshot_csv("backtest_results.csv")
        >>> perf.cum_returns.plot()
        """
        try:
            results = read_moonshot_csv(filepath_or_buffer)
        except ValueError as e:
            # "ValueError: 'Date' is not in list" might mean the user passed
            # a paramscan csv by mistake
            if "Date" not in repr(e):
                raise
            results = pd.read_csv(filepath_or_buffer)
            if "StrategyOrDate" in results.columns:
                raise MoonchartError("this is a parameter scan CSV, please use ParamscanTearsheet.from_moonshot_csv")
            else:
                raise

        return cls._from_moonshot_or_pnl(
            results,
            start_date=start_date,
            end_date=end_date,
            trim_outliers=trim_outliers,
            how_to_aggregate=how_to_aggregate,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window)

    @classmethod
    def from_pnl_csv(cls, filepath_or_buffer,
                     start_date=None,
                     end_date=None,
                     trim_outliers=None,
                     how_to_aggregate=None,
                     riskfree=0,
                     compound=True,
                     rolling_sharpe_window=200):
        """
        Creates a DailyPerformance instance from a PNL CSV.

        Parameters
        ----------
        filepath_or_buffer : str or file-like object
            filepath or file-like object of the CSV

        start_date : str (YYYY-MM-DD), optional
            truncate at this start date (otherwise include entire date range)

        end_date : str (YYYY-MM-DD), optional
            truncate at this end date (otherwise include entire date range)

        trim_outliers: int or float, optional
            discard returns that are more than this many standard deviations from the mean

        how_to_aggregate : dict, optional
            a dict of {fieldname: aggregation method} specifying how to aggregate
            fields from intraday to daily. See the docstring for
            `moonchart.utils.intraday_to_daily` for more details.

        riskfree : float, optional
            the riskfree rate (default 0)

        compound : bool
             True for compound/geometric returns, False for arithmetic returns (default True)

        rolling_sharpe_window : int, optional
            compute rolling Sharpe over this many periods (default 200)

        Returns
        -------
        DailyPerformance

        Examples
        --------
        Plot cumulative returns:

        >>> perf = DailyPerformance.from_pnl_csv("pnl.csv")
        >>> perf.cum_returns.plot()
        """
        results = read_pnl_csv(filepath_or_buffer)

        return cls._from_moonshot_or_pnl(
            results,
            start_date=start_date,
            end_date=end_date,
            trim_outliers=trim_outliers,
            how_to_aggregate=how_to_aggregate,
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window)

    @property
    def cum_returns(self):
        if self._cum_returns is None:
            self._cum_returns = get_cum_returns(self.returns, compound=self.compound)

        return self._cum_returns

    @property
    def cum_returns_longs(self):
        if self._cum_returns_longs is None:
            self._cum_returns_longs = get_cum_returns(self.returns_longs, compound=self.compound)

        return self._cum_returns_longs

    @property
    def cum_returns_shorts(self):
        if self._cum_returns_shorts is None:
            self._cum_returns_shorts = get_cum_returns(self.returns_shorts, compound=self.compound)

        return self._cum_returns_shorts

    @property
    def cum_commissions(self):

        if self._cum_commissions is None and self.commissions is not None:
            self._cum_commissions = get_cum_returns(self.commissions, compound=False)

        return self._cum_commissions

    @property
    def cum_commission_amounts(self):

        if self._cum_commission_amounts is None and self.commission_amounts is not None:
            self._cum_commission_amounts = self.commission_amounts.cumsum()

        return self._cum_commission_amounts

    @property
    def cum_slippages(self):

        if self._cum_slippages is None and self.slippages is not None:
            self._cum_slippages = get_cum_returns(self.slippages, compound=False)

        return self._cum_slippages

    @property
    def cagr(self):
        if self._cagr is None:
            self._cagr = get_cagr(self.cum_returns, compound=self.compound)

        return self._cagr

    @property
    def cagr_longs(self):
        if self._cagr_longs is None:
            self._cagr_longs = get_cagr(self.cum_returns_longs, compound=self.compound)

        return self._cagr_longs

    @property
    def cagr_shorts(self):
        if self._cagr_shorts is None:
            self._cagr_shorts = get_cagr(self.cum_returns_shorts, compound=self.compound)

        return self._cagr_shorts

    @property
    def sharpe(self):
        if self._sharpe is None:
            self._sharpe = get_sharpe(self.returns, riskfree=self.riskfree)

        return self._sharpe

    @property
    def rolling_sharpe(self):
        if self._rolling_sharpe is None:
            self._rolling_sharpe = get_rolling_sharpe(
                self.returns,
                window=self.rolling_sharpe_window,
                riskfree=self.riskfree)

        return self._rolling_sharpe

    @property
    def drawdowns(self):
        if self._drawdowns is None:
            self._drawdowns = get_drawdowns(self.cum_returns)

        return self._drawdowns

    @property
    def max_drawdown(self):
        return self.drawdowns.min()

    @property
    def cum_pnl(self):
        if self._cum_pnl is None and self.pnl is not None:
            self._cum_pnl = self.pnl.cumsum()

        return self._cum_pnl

    @property
    def benchmark_returns(self):
        """
        Returns a Series of benchmark returns from the DataFrame of benchmark
        prices, if any. If more than one strategy/column has benchmark
        prices, uses the first to compute returns.
        """
        if self._benchmark_returns is not None:
            return self._benchmark_returns

        if self._benchmark_prices is None:
            return None

        have_benchmarks = self._benchmark_prices.notnull().any(axis=0)
        have_benchmarks = have_benchmarks[have_benchmarks]
        if have_benchmarks.empty:
            return None

        col = have_benchmarks.index[0]
        if len(have_benchmarks.index) > 1:
            import warnings
            warnings.warn("Multiple benchmarks found, only using first ({0})".format(col))

        benchmark_prices = self._benchmark_prices[col]

        self._benchmark_returns = benchmark_prices.pct_change().fillna(0)
        self._benchmark_returns.name = "benchmark"

        return self._benchmark_returns

    @property
    def benchmark_cum_returns(self):

        if self._benchmark_cum_returns is None and self._benchmark_returns is not None:
            self._benchmark_cum_returns = get_cum_returns(self._benchmark_returns, compound=True)

        return self._benchmark_cum_returns

    @property
    def average_holding_periods_pos(self):
        if self._average_holding_periods_pos is None:
            self._average_holding_periods_pos = get_average_holding_periods(self.total_holdings)

        return self._average_holding_periods_pos

    @property
    def average_holding_periods_null(self):
        if self._average_holding_periods_null is None:
            self._average_holding_periods_null = get_average_holding_periods(self.total_holdings, lambda x: x == 0)

        return self._average_holding_periods_null

    @property
    def top_movers(self):
        if self._top_movers is None:
            self._top_movers = get_top_movers(self.returns)

        return self._top_movers

    @property
    def bar_size(self):
        if self._bar_size is None:
            self._bar_size = get_bar_size(self.returns)

        return self._bar_size


class AggregateDailyPerformance(DailyPerformance):
    """
    Class representing aggregate daily performance.

    Given a DailyPerformance instance containing multi-column (that is,
    multi-strategy or detailed single-strategy) DataFrames, this class
    represents the aggregate performance.

    Parameters
    ----------
    performance : DailyPerformance, required
        daily performance results to aggregate

    trim_outliers: int or float, optional
        discard returns that are more than this many standard deviations from the mean
        (copied from DailyPerformance if omitted)

    riskfree : float, optional
        the riskfree rate (copied from DailyPerformance if omitted)

    compound : bool
         True for compound/geometric returns, False for arithmetic returns (copied from
         DailyPerformance if omitted)

    rolling_sharpe_window : int, optional
        compute rolling Sharpe over this many periods (copied from DailyPerformance if
        omitted)

    Returns
    -------
    AggregatePerformance

    Examples
    --------
    Plot aggregate cumulative returns:

    >>> perf = DailyPerformance.from_moonshot_csv("backtest_results.csv")
    >>> agg_perf = AggregateDailyPerformance(perf)
    >>> agg_perf.cum_returns.plot()
    """

    def __init__(self, performance, riskfree=None,
                 compound=None,
                 rolling_sharpe_window=None,
                 trim_outliers=None):

        if riskfree is None:
            riskfree = performance.riskfree
        if compound is None:
            compound = performance.compound
        if rolling_sharpe_window is None:
            rolling_sharpe_window = performance.rolling_sharpe_window
        if trim_outliers is None:
            trim_outliers = performance._trim_outliers

        super(AggregateDailyPerformance, self).__init__(
            performance.returns.sum(axis=1),
            riskfree=riskfree,
            compound=compound,
            rolling_sharpe_window=rolling_sharpe_window,
            benchmark=performance._benchmark_prices,
            trim_outliers=trim_outliers
        )
        if performance.pnl is not None:
            self.pnl = performance.pnl.sum(axis=1)

        if performance.commission_amounts is not None:
            self.commission_amounts = performance.commission_amounts.sum(axis=1)

        if performance.commissions is not None:
            self.commissions = performance.commissions.sum(axis=1)

        if performance.slippages is not None:
            self.slippages = performance.slippages.sum(axis=1)

        if performance.net_exposures is not None:
            self.net_exposures = performance.net_exposures.sum(axis=1)

        if performance.abs_exposures is not None:
            self.abs_exposures = performance.abs_exposures.sum(axis=1)

        if performance.total_holdings is not None:
            self.total_holdings = performance.total_holdings.sum(axis=1)

        if performance.turnover is not None:
            self.turnover = performance.turnover.sum(axis=1)
