import requests
import json

def getAnalysis(tickers, time_range):
    
  # create an empty list to store the results
  results = []

  # split the tickers into a list
  tickers = tickers.split(",")

  # loop through each ticker
  for ticker in tickers:
    # make the API request to get the stock data
    url = f"https://query1.finance.yahoo.com/v7/finance/chart/{ticker}?range={time_range}&interval=1d&indicators=quote&includeTimestamps=true"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = response.json()

    # get the list of quotes from the API response
    quotes = data["chart"]["result"][0]["indicators"]["quote"][0]
    timestamps = data["chart"]["result"][0]["timestamp"]

    # loop through each quote and calculate the day over day percent change
    for i in range(1, len(quotes["close"])):
      prev_close = quotes["close"][i-1]
      close = quotes["close"][i]
      pct_change = 100 * (close / prev_close - 1)

      # create a dictionary to store the result
      result = {
        "ticker": ticker,
        "date": timestamps[i],
        "pct_change": pct_change
      }

      # add the result to the list
      results.append(result)

  # sort the results by the largest pct_change
  results.sort(key=lambda x: abs(x["pct_change"]), reverse=True)

  # return the top 5 results
  return results[:5]

print(getAnalysis(tickers="MSFT,F,CMG", time_range="6mo"))
