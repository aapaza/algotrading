# Algotrading
#
#       src/visual.py
#
# Copyright (c) 2017, Fabian Orccon <cfoch.fabian@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from settings import OUT_DIR


def csv_from_ticker(ticker, start=None, end=None):
    filename = ticker.lower() + ".csv"
    csv_path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(csv_path):
        if start is None:
            start = dt.datetime(2000, 1, 1)
        if end is None:
            end = dt.datetime.now().replace(second=0, microsecond=0)
        df = web.DataReader(ticker.upper(), 'yahoo', start, end)
        df.to_csv(csv_path)
    return csv_path

def plot_ma_from_csv(csv_path):
    df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
    df["100ma"] = df["Adj Close"].rolling(window=100, min_periods=0).mean()

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.plot(df.index, df["Adj Close"])
    ax1.plot(df.index, df["100ma"])
    ax2.plot(df.index, df["Volume"])
    plt.show()

def plot_candlestick_from_csv(csv_path):
    """
    Plot a candlestick chart.
    """
    df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
    df_ohlc = df["Adj Close"].resample("10D").ohlc()
    df_volume = df["Volume"].resample("10D").sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    # x axis, y axis, From 0 to the y axis
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    plt.show()
