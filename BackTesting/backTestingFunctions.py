import pandas as pd
import numpy as np


def CAGR(DF):
    """function to calculate the Cumulative Annual Growth Rate; DF should have ret column"""
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df) / 252
    CAGR = (df["cum_return"].tolist()[-1]) ** (1 / n) - 1
    return CAGR


def volatility(DF):
    """function to calculate annualized volatility; DF should have ret column"""
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252 * 26)
    return vol


def sharpe(DF, rf):
    """function to calculate sharpe ratio ; rf is the risk free rate"""
    df = DF.copy()
    sr = (CAGR(df) - rf) / volatility(df)
    return sr


def max_dd(DF):
    """function to calculate max drawdown"""
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["draw_down"] = df["cum_roll_max"] - df["cum_return"]
    df["draw_down_pct"] = df["draw_down"]/df["cum_roll_max"]
    return df["draw_down_pct"].max()
