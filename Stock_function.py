import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import yfinance as yf
from datetime import date
import datetime
import time
import requests
import json
from datetime import datetime



def add_cols(new_df, period=20):
    new_df["SMA"] = new_df["Close"].rolling(window=period).mean()
    new_df["STD"] = new_df["Close"].rolling(window=period).std()
    new_df["Upper"] = new_df["SMA"] + (new_df["STD"] * 1.5)
    new_df["Lower"] = new_df["SMA"] - (new_df["STD"] * 1.5)
    return new_df


def get_signal1(data):
    buy_signal = []
    sell_signal = []
    for i in range(len(data["Close"])):
        if data["Close"][i] > data["Upper"][i]:
            buy_signal.append(np.nan)
            sell_signal.append(data["Close"][i])
        elif data["Close"][i] < data["Lower"][i]:
            buy_signal.append(data["Close"][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
    return (buy_signal, sell_signal)


def get_new(new_df):
    new_df["Bollinger Buy"] = get_signal1(new_df)[0]
    new_df["Bollinger Sell"] = get_signal1(new_df)[1]
    return new_df


def get_results(df):
    sell = False
    buy = False
    if df[-1:]["Bollinger Buy"].isnull().to_string(index=False).replace(" ", "") == "False" and df[-1:][
        "Bollinger Sell"].isnull().to_string(index=False).replace(" ", "") == "True":
        buy = True
    # print("Buy!")
    elif df[-1:]["Bollinger Buy"].isnull().to_string(index=False).replace(" ", "") == "True" and df[-1:][
        "Bollinger Sell"].isnull().to_string(index=False).replace(" ", "") == "False":
        sell = True
    #  print("Sell!")
    return (buy, sell)


def get_plot(df):
    plt.figure(figsize=(15, 6))
    plt.plot(df["Close"], label="Close price")
    plt.title("Close price")
    plt.ylabel("Close price")
    plt.xlabel("Date")
    plt.legend(df.columns.values, loc="upper left")


def bollinger_plot(company_name, new_df, buy, sell, time=0):
    fig = plt.figure(figsize=(15, 6))
    ax = fig.add_subplot(1, 1, 1)
    x_axis = new_df.index[time:]
    ax.fill_between(x_axis, new_df["Upper"][time:], new_df["Lower"][time:], color="grey")
    ax.plot(x_axis, new_df["Close"][time:], color="Gold", lw=2, label="Close price")
    ax.plot(x_axis, new_df["SMA"][time:], color="Blue", lw=2, label="SMA")
    ax.scatter(x_axis, new_df["Bollinger Buy"][time:], color="green", label="Buy signal", marker="^", alpha=1)
    ax.scatter(x_axis, new_df["Bollinger Sell"][time:], color="red", label="Sell signal", marker="v", alpha=1)
    ax.set_title(company_name)
    #plt.show()
    if buy:
        fig.savefig("C:/Users/Daniel/PycharmProjects/Stocks/buypics/" + company_name.replace(".", "") + ".png")
    elif sell:
        fig.savefig("C:/Users/Daniel/PycharmProjects/Stocks/sellpics/" + company_name.replace(".", "") + ".png")

def get_trades(firms, total_profit, buy_list, sell_list, trades):
    #global total_profit, buy_list, sell_list, trades
    print(buy_list)
    print("Timestamp", datetime.now())
    print("Total profit before trades:", total_profit)
    print("Total trades before trades:", trades)
    for i in range(len(firms)):
        company_name = firms[i]
        # print("Company name", company_name)
        df = yf.Ticker(firms[i]).history(period="3mo")
        df = add_cols(df, period=20)
        df = get_new(df)
        df["Date"] = df.index
        df = df.reset_index(drop=True)
        buy, sell = get_results(df)
        if buy:
            if company_name not in buy_list:
                print(buy_list)
                buy_price = int(float(df[-1:]["Close"].to_string(index=False).replace(" ", "")))
                print("Buying company {} at price: {}".format(company_name, buy_price))
                bollinger_plot(company_name, df, buy, sell)
                buy_list[company_name] = buy_price
        if sell:
            if company_name in buy_list:
                print("Detected sell for bought stock")
                bollinger_plot(company_name, df)
                buy_price = buy_list[company_name]
                sell_list[company_name] = int(float(df[-1:]["Close"].to_string(index=False).replace(" ", "")))
                profit = sell_list[company_name] - buy_price
                print(
                    "Selling company {} at price {}, giving profit of {}".format(company_name, sell_list[company_name],
                                                                                 profit))
                print("Deleting stock")
                trades += 1
                del buy_list[company_name]
                total_profit += profit
    print("Total trades after trades: {}".format(trades))
    print("Total profit after trades: {}".format(total_profit))
    return total_profit, buy_list, sell_list, trades