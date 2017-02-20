# Algotrading Samples
#
#       samples/correlation_chart.py
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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils

from algotrading.scraping import csv_from_ticker
from algotrading.scraping import SP500_tickers_from_wikipedia
from algotrading.settings import OUT_DIR

tickers = utils.get_fixed_tickers()
csv_paths = utils.download_tickers_datasets(tickers)
CSV_PATH = utils.join_datasets(tickers, csv_paths)

df = pd.read_csv(CSV_PATH)
df_corr = df.corr()
data = df_corr.values

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
fig.colorbar(heatmap)
ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()

column_labels = df_corr.columns
row_labels = df_corr.index

ax.set_xticklabels(column_labels)
ax.set_yticklabels(row_labels)
plt.xticks(rotation=90)
heatmap.set_clim(-1, 1)

plt.tight_layout()
plt.show()
