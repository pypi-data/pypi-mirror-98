# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:37:59 2020

@author: pierr
"""
from flask import Flask, render_template, request, session
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from datetime import datetime
import seaborn as sns
import pandas as pd
import time
from pathlib import Path
import os
from math import sqrt
from scipy.stats import norm
import pandas_datareader as pdr

class MarketMaker:
    def __init__(self, price_generation):
        self.pnl=0 
        self.price_generation = price_generation
        self.stocks_number=1
    def generate_prices(self, number_of_periods):
        stock_prices = pd.DataFrame(np.ones((1,self.stocks_number))*100, index=[0], columns=["Stock_"+str(i+1) for i in range(self.stocks_number)])
        for i in range(1,number_of_periods):
            if self.price_generation["shock"] != None:
                a = self.price_generation["shock"]
                if a[0]==i:
                    random_variation = np.ones((1,self.stocks_number))*a[1]
                else:
                   random_variation = np.random.randint(-50,51, (1, self.stocks_number))/1000
            else:
                random_variation = np.random.randint(-50,51, (1, self.stocks_number))/1000
            last_prices = np.array(stock_prices.iloc[stock_prices.shape[0]-1,:])
            stock_prices.loc[i,:] = np.multiply(last_prices,(1+random_variation))
        return stock_prices

class Trader:
    def __init__(self, strategy="buy_and_hold", initial_capital=100000, risk_free_rate=0.01):
        self.initial_capital = initial_capital
        self.risk_free_rate = risk_free_rate
        self.stategies={"buy_and_hold":self.buy_and_hold, "double_when_down":self.double_when_down, "moving_average":self.moving_average}
        if strategy in self.stategies.keys():
            self.strategy=strategy
        else:
            raise ValueError ("Incorrect strategy. Possible values :"+str(self.startegies.keys()))
        self.capital_evolution = [self.initial_capital]
        self.pnl_evolution = [0]
        self.invested_capital_evolution = []
        self.position_value_evolution = []
        self.results = None
        self.market_maker_account = 0
        
    def backtest(self, stock_price):
        self.results = stock_price.copy()
        if self.strategy=="buy_and_hold":
            return self.buy_and_hold(stock_price)
        elif self.strategy == "double_when_down":
            return self.double_when_down(stock_price)
        elif self.strategy == "moving_average":
            return self.moving_average(stock_price)
        
    def double_when_down(self, stock_price, threshold = 0.1):
        initial_capital = self.initial_capital / 31
        pnl=0
        stock_price = np.array(stock_price)
        first_price = stock_price[0,:]
        invested_capital = initial_capital
        portfolio_value = initial_capital
        self.invested_capital_evolution.append(invested_capital)
        for i in range(1, stock_price.shape[0]):
            cumul_returns = (np.array(stock_price[i])/first_price)-1
            a = portfolio_value
            portfolio_value = portfolio_value*np.array(stock_price[i])/np.array(stock_price[i-1])
            pnl+=(portfolio_value-a)[0]
            if abs(cumul_returns) >= threshold:
                if cumul_returns > 0 :
                    invested_capital = initial_capital
                    portfolio_value = initial_capital
                    first_price = stock_price[i]
                else:
                    portfolio_value+=(invested_capital+initial_capital)
                    invested_capital=2*invested_capital+initial_capital
                    first_price = stock_price[i]
            self.invested_capital_evolution.append(invested_capital)
            self.capital_evolution.append(self.initial_capital+pnl)
            self.pnl_evolution.append(pnl)
        self.results ["pnl"] = self.pnl_evolution
        self.results ["capital"] = self.capital_evolution
        self.results ["invested_capital"] = self.invested_capital_evolution
        
    def buy_and_hold(self, stock_price):
        pnl=0
        stock_price = np.array(stock_price)
        invested_capital = self.initial_capital
        portfolio_value = self.initial_capital
        self.invested_capital_evolution.append(invested_capital)
        for i in range(1, stock_price.shape[0]):
            portfolio_value = portfolio_value*(np.array(stock_price[i])/np.array(stock_price[i-1]))
            pnl=(portfolio_value-invested_capital)[0]
            self.invested_capital_evolution.append(invested_capital)
            self.capital_evolution.append(self.initial_capital+pnl)
            self.pnl_evolution.append(pnl)
        self.results ["pnl"] = self.pnl_evolution
        self.results ["capital"] = self.capital_evolution
        self.results ["invested_capital"] = self.invested_capital_evolution
    def moving_average(self, stock_price):
        allow_borrowing = False
        pnl=0
        stock_price = np.array(stock_price)
        invested_capital = 0
        portfolio_value = 0
        total_capital = self.initial_capital
        self.invested_capital_evolution.append(invested_capital)
        moving_averages = pd.DataFrame(stock_price, columns=["stock_price"])
        sma_20 = np.array(moving_averages.rolling(20).mean())
        moving_averages["sma_10"] = np.array(moving_averages.rolling(10).mean())
        moving_averages["sma_20"] = sma_20
        for i in range(1, stock_price.shape[0]):
            if i <= 19:
                if i==19:
                    ma_10 = moving_averages.iloc[i,1]
                    ma_20 = moving_averages.iloc[i,2]
                    if ma_10>ma_20 :
                        wait_to = "sell"
                    else:
                        wait_to = "buy"
            else:
                ma_10 = moving_averages.iloc[i,1]
                ma_20 = moving_averages.iloc[i,2]
                today_price = moving_averages.iloc[i,0]
                if invested_capital != 0:
                    previous_value = portfolio_value
                    portfolio_value = portfolio_value*(today_price)/(moving_averages.iloc[i-1,0])
                    pnl += portfolio_value - previous_value
                if (wait_to == "sell") :
                    if (ma_10<ma_20):
                        if invested_capital !=0:
                            invested_capital = 0
                            total_capital = portfolio_value
                            portfolio_value = 0
                        wait_to = "buy"                            
                elif (wait_to=="buy") and (ma_10>ma_20):
                    if invested_capital == 0:
                        invested_capital = total_capital
                        portfolio_value = invested_capital
                    wait_to = "sell"
            self.invested_capital_evolution.append(invested_capital)
            self.capital_evolution.append(self.initial_capital+pnl)
            self.pnl_evolution.append(pnl)
        self.results ["pnl"] = self.pnl_evolution
        self.results ["capital"] = self.capital_evolution
        self.results ["invested_capital"] = self.invested_capital_evolution


class StockExchange:
    def __init__(self, initial_capital=100000, risk_free_rate = 0.01):
        self.risk_free_rate = risk_free_rate
        self.initial_capital = initial_capital
        self.trading_strategies = None
        self.traders = []
        self.market_maker = None
        self.stock_price = None
        
    def perform_simulation(self, trading_strategies = ["buy_and_hold"], price_generation = {"method":"market_maker","dates":50,"price_column_name": None, "path":None, "stress_test":None}):
        self.trading_strategies = trading_strategies
        # Create Traders
        for i in self.trading_strategies:
            self.traders.append(Trader(strategy = i ,initial_capital = self.initial_capital))
        # Generate prices
        self.generate_prices(price_generation)
        # Backtest trading strategies
        for trader in self.traders:
            trader.backtest(self.stock_price)
            
    def display_results(self):
        final_results = self.traders[0].results
        if len(self.traders)>1:
            i=2
            for trader in self.traders[1:]:
                if i==2:
                    final_results = final_results.join(trader.results.drop(trader.results.columns[0], axis=1), lsuffix="_trader_1", rsuffix="_trader_"+str(i))
                else:
                    trader.results.drop(trader.results.columns[0], axis=1, inplace=True)
                    trader.results.columns = [str(cols+"_trader_"+str(i)) for cols in trader.results.columns]
                    final_results = final_results.join(trader.results)
                i+=1
        final_results.rename(columns={final_results.columns[0]:"Stock_Price"},inplace=True)
        return final_results
    
    def generate_prices(self, price_generation):
        if price_generation["method"] == "market_maker":
            self.market_maker = MarketMaker(price_generation)
            self.stock_price = self.market_maker.generate_prices(price_generation["dates"])
        elif price_generation["method"]== "download_data":
            if "path_to_downloads" in price_generation.keys():
                self.get_data_on_web(price_generation["stock_ticker"], price_generation["first_date"], price_generation["end_date"])
            else:
                self.get_data_on_web(price_generation["stock_ticker"], price_generation["first_date"], price_generation["end_date"])
        elif price_generation["method"] == "brownian_motion":
            self.brownian_motion(price_generation["dates"])

    def brownian_motion(self, dates):
        dt = 1
        delta = 2
        n = dates
        x0 = np.asarray(100)
        r = norm.rvs(size=x0.shape + (n,), scale=delta*sqrt(dt))
        out = np.empty(r.shape) 
        np.cumsum(r, axis=-1, out=out)
        out += np.expand_dims(x0, axis=-1)
        self.stock_price = pd.DataFrame(out, columns=["Stock_Price"])

    def get_data_on_web(self, ticker, first_date, end_date):
        self.stock_price = pdr.get_data_yahoo(ticker, start=first_date, end=end_date)[["Close"]].fillna(method="bfill")
        self.stock_price.columns = [ticker]

app = Flask(__name__)
app.secret_key = "anything"
@app.route('/', methods = ['POST', 'GET'])
def home_page():
    session['username'] = 'admin'
    return render_template("home.html")

@app.route('/visualize', methods = ['POST', 'GET'])
def visualize():
    values = request.form.to_dict()
    # Extract the parameters from the dictionnary
    # Global market parameters
    initial_capital = int(values["initial_capital"])
    risk_free_rate = int(values["risk_free_rate"])
    price_generation_method = str(values["method"])
    number_of_simulations = int(values["number_of_simulations"])
    # Parameters if use Download Data
    if price_generation_method=="download_data" :
        first_date = datetime.strptime(str(values["first_date"]), "%Y-%m-%d")
        end_date = datetime.strptime(str(values["end_date"]), "%Y-%m-%d")
        stock_ticker = str(values["stock_ticker"])
        number_of_periods, shock = None, None
    # Parameters if use Market Maker
    if (price_generation_method == "market_maker") or (price_generation_method == "brownian_motion"):
        first_date, end_date, stock_ticker = None, None, None
        number_of_periods = int(values["number_of_periods"])
        try:
            shock = (int(values["shock_date"]),int(values["shock_percentage"]))
        except:
            shock = None
    # Trading strategies
    trading_strategies = []
    for strat in ["buy_and_hold", "double_when_down", "moving_average"]:
        if strat in values.keys():
            if values[strat]=="on":
                trading_strategies.append(strat)
    try:
        threshold = values["threshold"]
    except:
        threshold = None             
    # Perform simulation
    for i in range(1, number_of_simulations+1):
        stock_exchange = StockExchange(initial_capital = initial_capital, risk_free_rate = risk_free_rate)
        stock_exchange.perform_simulation(trading_strategies = trading_strategies,
                                          price_generation = {"method":price_generation_method,
                                                              "dates":number_of_periods,
                                                              "path":None, 
                                                              "first_date" : first_date,
                                                              "end_date": end_date, 
                                                              "stock_ticker":stock_ticker,
                                                              "shock":shock,
                                                              "threshold":threshold})
        data = stock_exchange.display_results()
        if (number_of_simulations == 1) or (price_generation_method == "download_data"):
            # Creating the visualization page
            fig = plt.figure(figsize=(15,5))
            pnl = fig.add_subplot(121)
            plt.title("P&L of the traders")
            pnl.set_xlabel("Time")
            pnl.set_ylabel("P&L (euros)")
            if "pnl" in data.columns:
                pnl.plot(np.linspace(0, data.shape[0]-1, data.shape[0]), np.array(data.pnl))
            else : 
                for j in range(1, 4):
                    if "pnl_trader_"+str(j) in data.columns:
                        pnl.plot(np.linspace(0, data.shape[0]-1, data.shape[0]), np.array(data["pnl_trader_"+str(j)]), label="pnl of trader "+str(j))
            plt.legend()
            stock_price = fig.add_subplot(122)
            stock_price.set_title("Stock price")
            stock_price.set_xlabel("Time")
            stock_price.set_ylabel("Price (euros)")
            stock_price.plot(np.linspace(0, data.shape[0]-1, data.shape[0]), np.array(data.iloc[:,0]))
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            path = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode('utf8')
            data_rounded = data.round(2)
            return render_template('visualize.html', image = path, tables = [data_rounded.to_html(classes='data')])
        else:
            if i==1:
                stock_price_agg=data[["Stock_Price"]]
                if "pnl" in data.columns:
                    pnl_agg=[int(data[["pnl"]].iloc[-1,:])]
                elif "pnl_trader_3" in data.columns:
                    pnl_agg_1=[int(data[["pnl_trader_1"]].iloc[-1,:])]
                    pnl_agg_2=[int(data[["pnl_trader_2"]].iloc[-1,:])]
                    pnl_agg_3=[int(data[["pnl_trader_3"]].iloc[-1,:])]
                else:
                    pnl_agg_1=[int(data[["pnl_trader_1"]].iloc[-1,:])]
                    pnl_agg_2=[int(data[["pnl_trader_2"]].iloc[-1,:])]
            else:
                stock_price_agg["Stock_price_"+str(i)]=np.array(data.Stock_Price)
                if "pnl" in data.columns:
                    pnl_agg.append(int(data[["pnl"]].iloc[-1,:]))
                elif "pnl_trader_3" in data.columns:
                    pnl_agg_1.append(int(data[["pnl_trader_1"]].iloc[-1,:]))
                    pnl_agg_2.append(int(data[["pnl_trader_2"]].iloc[-1,:]))
                    pnl_agg_3.append(int(data[["pnl_trader_3"]].iloc[-1,:]))
                else:
                    pnl_agg_1.append(int(data[["pnl_trader_1"]].iloc[-1,:]))
                    pnl_agg_2.append(int(data[["pnl_trader_2"]].iloc[-1,:]))
        if i==number_of_simulations:
            fig = plt.figure(figsize=(15,5))
            pnl = fig.add_subplot(121)
            plt.title("P&L of the traders")
            pnl.set_xlabel("P&L (euros)")
            pnl.set_ylabel("Density")
            if "pnl" in data.columns:
                data_rounded = pd.DataFrame(np.array(pnl_agg)).describe()
                sns.kdeplot(np.array(pnl_agg))
            elif "pnl_trader_3" in data.columns:
                data_rounded = pd.DataFrame(np.array([pnl_agg_1, pnl_agg_2, pnl_agg_3]).transpose(), columns=["pnl_trader_1","pnl_trader_2","pnl_trader_3"]).describe()
                sns.kdeplot(np.array(pnl_agg_1), label="pnl of trader 1")
                sns.kdeplot(np.array(pnl_agg_2), label="pnl of trader 2")
                sns.kdeplot(np.array(pnl_agg_3), label="pnl of trader 3")
            else:
                data_rounded = pd.DataFrame(np.array([pnl_agg_1,pnl_agg_2]).transpose(), columns=["pnl_trader_1","pnl_trader_2"]).describe()
                sns.kdeplot(np.array(pnl_agg_1), label="pnl of trader 1")
                sns.kdeplot(np.array(pnl_agg_2), label="pnl of trader 2")
            stock_price = fig.add_subplot(122)
            stock_price.set_title("Stock price")
            stock_price.set_xlabel("Time")
            stock_price.set_ylabel("Price (euros)")
            stock_price_agg.plot(ax=plt.gca())
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            path = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode('utf8')
            return render_template('visualize.html', image = path, tables = [data_rounded.to_html(classes='data')])

@app.route('/more_results', methods = ['POST', 'GET'])
def more_results():
    return render_template('more_results.html')

@app.route('/help', methods = ['POST', 'GET'])
def documents():
    return render_template('readme.html')

@app.route('/analysis', methods = ['POST','GET'])
def analysis():
    return render_template('analysis.html')

if __name__ == "__main__":
    app.run()