# -*- coding: utf-8 -*-
"""
IBAPI - Getting historical data intro

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)


def websocket_con():
    app.run()


app = TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established

# creating object of the Contract class - will be used as a parameter for other function calls
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "ISLAND"

# https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#aad87a15294377608e59aec1d87420594 - for
# more info
app.reqHistoricalData(reqId=1,
                      contract=contract,
                      endDateTime='',  # the empty string indicates current present moment
                      durationStr='3 M',  # The amount of time (or Valid Duration String units) to go back from the
                      # request's given end date and time.
                      barSizeSetting='5 mins',  # The data's granularity or Valid Bar Sizes
                      whatToShow='MIDPOINT',  # The type of data to retrieve.
                      useRTH=1,  # Whether (1) or not (0) to retrieve data generated only within Regular Trading
                      # Hours (RTH)
                      formatDate=1,  # set to 1 to obtain the bars' time as yyyyMMdd HH:mm:ss
                      keepUpToDate=0,  # Whether a subscription is made to return updates of unfinished real time
                      # bars as they are available (True), or all data is returned on a one-time basis (False)
                      chartOptions=[])  # EClient function to request contract details
time.sleep(5)  # some latency added to ensure that the contract details request has been processed
