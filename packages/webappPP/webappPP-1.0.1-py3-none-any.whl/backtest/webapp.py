# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:37:59 2020

@author: pierr
"""
from flask import Flask, render_template, request
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import stockexchange.pipeline as pipeline
import numpy as np
from datetime import datetime
import webbrowser
from threading import Timer
import seaborn as sns
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home_page():
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
        stock_exchange = pipeline.StockExchange(initial_capital = initial_capital, risk_free_rate = risk_free_rate)
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

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')
if __name__ == "__main__":
    Timer(1, open_browser).start();
    app.run()