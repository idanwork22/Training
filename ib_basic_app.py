# -*- coding: utf-8 -*-
"""
IBAPI - Getting historical data (multiple tickers)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time


class TradingApp(EWrapper, EClient):
    """
    TradingApp class
    """
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)


def createConnection():
    """
    This function creates connection with the server
    127.0.0.1 - the localhost IP
    7497 - the socket port
    clientId = the client id (can be any number)
    :return: return connection type Wrapper and EClient
    """
    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    return app


def websocket_con():
    app.run()


# open connection - global
app = createConnection()


def main():
    """
    This is the main function
    """
    # open connection at  app = createConnection()
    # starting a separate daemon thread to execute the websocket connection
    con_thread = threading.Thread(target=websocket_con, daemon=True)
    con_thread.start()
    time.sleep(1)  # some latency added to ensure that the connection is established

    # The symbols
    tickers = ["FB", "AMZN", "INTC"]
    get_data_tickers(tickers)


# creating object of the Contract class - will be used as a parameter for other function calls
def usTechStk(symbol, sec_type="STK", currency="USD", exchange="ISLAND"):
    """
    Create contract with the given parameters
    :param symbol: The stoke symbol
    :param sec_type: always STK
    :param currency: always USD
    :param exchange: always ISLAND
    :return: returns connection
    """
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract


def histData(req_num, contract, duration, candle_size):
    """

    :param req_num: request number - every symnol - different reqId
    :param contract: given from usTechStk function
    :param duration: The amount of time to go back from
    :param candle_size: The canndle size
    :return: prints the data
    """
    # https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#aad87a15294377608e59aec1d87420594
    # - for more info
    app.reqHistoricalData(reqId=req_num,
                          contract=contract,
                          endDateTime='',  # the empty string indicates current present moment
                          durationStr=duration,
                          # The amount of time (or Valid Duration String units) to go back from the
                          # request's given end date and time.
                          barSizeSetting=candle_size,  # The data's granularity or Valid Bar Sizes
                          whatToShow='ADJUSTED_LAST',  # The type of data to retrieve.
                          useRTH=1,  # Whether (1) or not (0) to retrieve data generated only within Regular Trading
                          # Hours (RTH)
                          formatDate=1,  # set to 1 to obtain the bars' time as yyyyMMdd HH:mm:ss
                          keepUpToDate=0,  # Whether a subscription is made to return updates of unfinished real time
                          # bars as they are available (True), or all data is returned on a one-time basis (False)
                          chartOptions=[])  # EClient function to request contract details
    # some latency added to ensure that the contract details request has been processed


def get_data_tickers(tickers):
    """
    for every ticker in the arry - the function calls histData,
    and between calls - there is a sleep time of 5 second - for Preventing confusion
    :param tickers: arry of symbols - type str
    :return: Only call other function
    """
    for ticker in tickers:
        histData(tickers.index(ticker), usTechStk(ticker), '1 D', '5 mins')
        time.sleep(1)  # some latency added to ensure that the contract details request has been processed


if __name__ == '__main__':
    main()
