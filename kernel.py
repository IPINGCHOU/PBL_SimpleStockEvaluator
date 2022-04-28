#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
#%%
def fetch_close(stock_name, period, interval):

    my_share = stock_name + '.T'
    my_share = share.Share(my_share)
    symbol_data = None

    try: 
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_YEAR, period,
            share.FREQUENCY_TYPE_DAY, interval)
    except YahooFinanceError as e:
        return 1

    df = pd.DataFrame(symbol_data)
    df["datetime"] = pd.to_datetime(df.timestamp, unit="ms").dt.date
    # df["datetime_JST"] = df["datetime"].dt.date

    return df

def comb_close(stock_set, period, interval):
    all_df = []
    error_list = []
    success_list = []
    for stock in stock_set:
        cur = fetch_close(stock, period, interval)
        if isinstance(cur, int):
            error_list.append(stock)
        else:
            cur.set_index('datetime', inplace = True, drop = True)
            cur = cur['close']
            all_df.append(cur)
            success_list.append(stock)
    
    stocks_df = pd.concat(all_df, axis = 'columns', join = 'inner')
    stocks_df.columns = success_list
    print(len(stocks_df))
    return stocks_df, success_list, error_list


class stockEval:
    def __init__(self, stock_df, frame, suc_list, err_list):
        l = len(stock_df)
        self.success_list = suc_list
        self.error_list = err_list
        self.stock_df = stock_df.pct_change().dropna()
        self.stock_name = self.stock_df.columns.values.tolist()
        self.cumulative_df = (1+self.stock_df).cumprod()
        self.sharpe_df =(self.stock_df.mean() * l) / (self.stock_df.std() * np.sqrt(l))
        self.sharpe_df = self.sharpe_df.sort_values(ascending = False)

        self.initial_port = 10000
        self.stock_mc_sim = dict()
        self.get_VaR()

        self.figsize = (9,4)
        self.fig = plt.figure(figsize = self.figsize, dpi=50)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def draw_plot(self, target):
        print("Now: ", target)
        if target == 'Raw':
            self.ax.plot(self.stock_df)
            self.ax.set_title('Daily Return')
            self.ax.legend(self.stock_name)
        elif target == 'Cumulative':
            self.ax.plot(self.cumulative_df)
            self.ax.set_title("Cumulative Return")
            self.ax.legend(self.stock_name)
        elif target == 'Raw-Box':
            self.ax.boxplot(self.stock_df)
            self.ax.set_title("Portfolio Risk")
            self.ax.set_xticklabels(self.stock_name)
        elif target == '30days-rolling':
            self.ax.plot(self.stock_df.rolling(window=30).std())
            self.ax.set_title("30 Days Rolling Std.")
            self.ax.legend(self.stock_name)
        elif target == 'Sharpe':
            self.ax = self.sharpe_df.plot(figsize=self.figsize, kind = 'bar')
            self.ax.set_title("Sharpe Ratio")
            self.ax.set_xticklabels(self.stock_name, rotation = 0, rotation_mode = 'anchor')
        elif target in self.stock_name:
            self.ax.plot(self.stock_mc_sim[target])
            self.ax.axhline(y=self.initial_port ,c="blue",linewidth = 3, label = 'Initial capital')
            self.ax.axhline(y=self.stock_var[target], c = "lawngreen", linewidth = 3, label = 'VaR')
            self.ax.axhline(y=self.stock_cvar[target], c = 'red', linewidth = 3, label = 'CVaR')
            self.ax.legend()
            self.ax.set_title(target + " Value at Risk(VaR) Monte Carlo Sim, 400 trails, 100 days, alpha = 0.05")
            xlabel_text = "VaR \${}    CVaR \${}".format(round(self.stock_var[target],2), round(self.stock_cvar[target],2))
            self.ax.set_xlabel(xlabel_text, fontsize = 10)

        self.canvas.draw()
        self.ax.clear()

    def mcport(self, name, stock, trials = 400, days = 100):
        mean = stock.mean()
        var = np.array(stock.var()).reshape(1,1)
        meanM = np.full(shape = (days, 1), fill_value = mean)
        meanM = meanM.T

        portfolio_sims = np.full(shape = (100, trials), fill_value = 0.0)

        for s in range(trials):
            Z = np.random.normal(size = (days, 1))
            L = np.linalg.cholesky(var)
            dR = meanM + np.inner(L, Z)
            portfolio_sims[:, s] = np.cumprod(np.inner(np.array([1]), dR.T)+1) * self.initial_port

        self.stock_mc_sim[name] = portfolio_sims
        return portfolio_sims[-1, :]

    def mcVaR(self, returns, alpha = 5):
        return np.percentile(returns, alpha)
    
    def mcCVaR(self, returns, alpha = 5):
        below = returns <= self.mcVaR(returns, alpha = alpha)
        return returns[below].mean()

    def get_VaR(self):
        self.stock_risk = dict()
        self.stock_var = dict()
        self.stock_cvar = dict()
        for colname, colval in self.stock_df.iteritems():

            port_res = pd.Series(self.mcport(colname, colval))
            VaR = self.initial_port - self.mcVaR(port_res)
            CVaR = self.initial_port - self.mcCVaR(port_res)
            VaR_ratio = VaR / self.initial_port
            CVaR_ratio = CVaR / self.initial_port
            self.stock_var[colname] = -1*VaR + self.initial_port
            self.stock_cvar[colname] = -1*CVaR + self.initial_port

            if VaR_ratio > 0.35 and CVaR_ratio > 0.45:
                self.stock_risk[colname] = 'High'
            elif VaR_ratio < 0.15 or CVaR_ratio < 0.10:
                self.stock_risk[colname] = 'Low'
            else:
                self.stock_risk[colname] = 'Med'

            print('VaR ${}'.format(round(VaR,2)))
            print('CVaR ${}'.format(round(CVaR,2)))




# %%
