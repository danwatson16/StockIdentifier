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
from Stock_function import get_trades
import json

with open('C:/Users/Daniel/PycharmProjects/Stocks/text.txt', 'r') as f:
    a = json.loads(f.read())

total_profit = a[0]
buy_list = a[1]
sell_list = a[2]
trades = a[3]
firms = a[4]
while True:
    total_profit, buy_list, sell_list, trades = get_trades(firms, total_profit, buy_list, sell_list, trades)
    print("Updating stats")
    with open('text.txt', 'w') as f:
        features = [total_profit, buy_list, sell_list, trades, firms]
        f.write(json.dumps(features))
    time.sleep(3600)