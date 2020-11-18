# StockIdentifier
Identifies which stocks to purchase based on bollinger band moving average deviations.

-Scrapes etoro for stock tickers then uses yfinance package to download data for individual tickers. Moving average at 20 day period is calculated.
-Bollinger low and highs are produced based on SMA.mean() + 1.5 * SMA.std().
-For each stock, if current close is less than lower bound then trade signal to buy and sell for the opposite. 
-If indicated to buy, append to a buy list and produce a bollinger plot to buypics directory. 
-If a stock is in buy list and then is indicated to sell, remove from buy list like in reality and increment total profit.
-Program runs every hour.

