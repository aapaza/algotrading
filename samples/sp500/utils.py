# Algotrading Samples
#
#       samples/sp500/utils.py
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
import pandas as pd

from algotrading.scraping import csv_from_ticker
from algotrading.scraping import SP500_tickers_from_wikipedia
from algotrading.settings import OUT_DIR

CSV_PATH = os.path.join(OUT_DIR, "calculate_sp500.csv")

def get_fixed_tickers():
    tickers = SP500_tickers_from_wikipedia()
    tickers_fix = {
        "BRK.B": "BRK-B",
        "BF.B": "BF-B" 
    }

    for i, ticker in enumerate(tickers):
        if ticker in tickers_fix:
            tickers[i] = tickers_fix[ticker]
    return tickers

def download_tickers_datasets(tickers):
    csv_paths = []
    for ticker in tickers:
        csv_path = csv_from_ticker(ticker)
        csv_paths.append(csv_path)
        print("%s has been read" % ticker)
    return csv_paths

def join_datasets(tickers, csv_paths):
    if not os.path.exists(CSV_PATH):
        main_df = pd.DataFrame()
        for i, (ticker, csv_path) in enumerate(zip(tickers, csv_paths)):
            df = pd.read_csv(csv_path)
            df.set_index("Date", inplace=True)
            df.rename(columns={"Adj Close": ticker}, inplace=True)
            df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how="outer")

            if i % 10 == 0:
                print(i)
        main_df.to_csv(CSV_PATH)
    return CSV_PATH
