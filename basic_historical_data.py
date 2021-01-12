from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd
import threading
import time
from coreFunctions import connection_functions
import sys


class TradingApp(EWrapper, EClient):
    """
    TradingApp class
    """

    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def historicalData(self, reqId, bar):
        # if the key is not in the data - so create one -> list of a dictionaries
        if reqId not in self.data:
            self.data[reqId] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]
        else:
            # if the key is  in the data - so append to the insider dict
            self.data[reqId].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})
        # prints the bar bar data
        print("reqID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId, bar.date, bar.open,
                                                                                        bar.high, bar.low, bar.close,
                                                                                        bar.volume))


def get_data_tickers(app,tickers):
    """
    for every ticker in the arry - the function calls histData,
    and between calls - there is a sleep time of 5 second - for Preventing confusion
    :param tickers: arry of symbols - type str
    :return: Only call other function
    """
    for ticker in tickers:
        connection_functions.histData(app, tickers.index(ticker), connection_functions.createContract(ticker), '1 D', '5 mins')
        time.sleep(1)  # some latency added to ensure that the contract details request has been processed


def dataDataframe(symbols, TradeApp_obj):
    """
    returns extracted historical data in dataframe format
    """
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
        df_data[symbol].set_index("Date", inplace=True)
    return df_data


def main():
    """
    This is the main function
    """
    # open connection - global
    app = connection_functions.createConnection()
    # starting a separate daemon thread to execute the websocket connection
    con_thread = threading.Thread(target=lambda : connection_functions.websocket_con(app))
    con_thread.setDaemon(True)
    con_thread.start()
    time.sleep(2)  # some latency added to ensure that the connection is established

    # The symbols
    tickers = ["FB", "AMZN", "INTC"]
    get_data_tickers(app,tickers)

    # extract and store historical data in dataframe
    historicalData = dataDataframe(tickers, app)
    print("Finished!")


if __name__ == '__main__':
    main()
