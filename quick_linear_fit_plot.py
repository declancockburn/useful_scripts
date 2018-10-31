# -*- coding: utf-8 -*-
"""
Created by dcockbur on 25/10/2018	
"""
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def make_series(csv):
    """Returns a series from a single signal vs. time exported CSV from grafana"""
    df = pd.read_csv('grafana_data_export.csv', sep=';', parse_dates=True)
    df['Time'] = pd.to_datetime(df['Time'])
    df.dropna(inplace=True)
    df.drop('Series', axis=1, inplace=True)
    df.set_index('Time', inplace=True)
    return df['Value']


def linear_fit(ts, howfarback=1, howfarfwd=50, periods=50):
    """Input: Takes a time-series (datetime index and float or integer values.
        howfarback: percentage (decimal) how much of data to fit
        howfarfwd: how far in future to plot, from last data point in days
    Output: Linear fit of data, as time-series."""
    if not isinstance(ts, pd.Series):  # Check that the input is indeed a series
        print("Error, input is {}, not a pandas Series".format(type(ts)))
        return ''
    slice = int(len(ts)*howfarback)  # Slice portion of most recent data for fitting.
    ts = ts[-slice:]  # Filter out only that data

    dt_fl = ts.index.values.astype(float)  # Take the float of the timestamp index
    y_d = ts.values  # Take the values of the series
    p = np.polyfit(dt_fl, y_d, 1)   # Least squares 1D polynomial coefficients fit to data.
    m, c = p  # Separate the coefficients
    fit_range = pd.date_range(start=ts.index.values[0], end=ts.index.values[-1]+pd.Timedelta(days=howfarfwd),
                             periods=periods)  # Make an x time range to plot
    fit_range_fl = fit_range.values.astype(float) # convert range to float values
    y_fit = m*fit_range_fl + c  # Get fit's y values with line equation
    return pd.Series(index=fit_range, data=y_fit)  # Pair y-vals with time-range (as opposed to floats).


def quickplot(csv):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ser = make_series(csv)
    ser.plot(ax=ax, style='.')
    fit = linear_fit(ser)
    fit.plot(ax=ax, style='-')
    ax.legend()
    ax.axhline(y=0.35)
    return ax, ser, fit

