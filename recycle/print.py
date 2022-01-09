# -*- coding: utf-8 -*-
"""
plot the temperature change under different scenarios.
This function is set up for the 
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


def read_result(database, scenarios):
    conn = sqlite3.Connection(database)
    df = []
    for _ in scenarios:
        query = f"SELECT agentid, tripid, length AS {_}_length,\
            mrt_exp AS {_}_mrt, wbgt_exp AS {_}_wbgt\
            FROM {_} WHERE mrt_exp > 0"
        df.append(pd.read_sql(query, conn))
    conn.close()
    # merge dataframes
    new_df = df[0]
    for _ in range(1,len(scenarios)):
        temp_df =  pd.merge(new_df, df[_], how = 'left', left_on = ['agentid', 'tripid'],
                          right_on = ['agentid', 'tripid']).reset_index()
        
        temp_df[f"{scenarios[_]}_wbgt_cool"] = temp_df[f"{scenarios[_]}_wbgt"] - temp_df["s0_wbgt"]
        
        temp_df[f"{scenarios[_]}_mrt_cool"] = temp_df[f"{scenarios[_]}_mrt"] - temp_df["s0_mrt"]
        new_df = temp_df
    return new_df


def plot_hist(df: pd.DataFrame, scenarios: list, temp: str = 'mrt', bin_num: int = 20):
    linestyle=('solid','dashed')
    value = []
    weight = []
    for _ in range(len(scenarios)):
        data = list(df[f"{scenarios[_]}_{temp}"])
        counts, bins = np.histogram(data, bins = bin_num)
        count = counts/len(data)
        value.append(data)
        weight.append(count)
        plt.hist(bins[:-1], bins, histtype='step', weights=count, 
                 alpha=0.8, linestyle = linestyle[_%2], label = scenarios[_])
        plt.plot()
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.legend(loc='upper left')
    plt.xlabel(f'{temp} temperature (C)')
    plt.ylabel('percent')
    plt.show()
    return value, weight
    

database = r"C:\test_codes_delete_later\db_test\db_test.db"
scenarios = ['s0', 's2', 's5', 's7', 's9']
dff = read_result(database, scenarios)
plot_hist(dff, scenarios, bin_num = 10)

def plot_length(sce, db):
    dff_1 = read_result(database, sce)
    dff_1[f'{sce[-1]}_delta'] = dff_1[f'{sce[-1]}_length']- dff_1[f'{sce[0]}_length']
    dff_1[(dff_1[f'{sce[-1]}_delta']>0)].boxplot(column = f'{sce[-1]}_delta',showfliers = True )
    return dff_1[['agentid','tripid', f'{sce[-1]}_delta', 's0_length']]

s1 = read_result(database, ['s0','s2'])
s2 = plot_length(['s0','s2'], database)
