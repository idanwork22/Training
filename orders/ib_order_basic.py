# -*- coding: utf-8 -*-
"""
IBAPI - placing simple orders

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorString))

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


def createConnection():
    """
    This function creates connection with the server
    127.0.0.1 - the localhost IP
    7497 - the socket port
    clientId = the client id (can be any number)
    :return: return connection type Wrapper and EClient
    """
    app = TradingApp()
    # port 4002 for ib gateway paper trading/7497 for TWS paper trading
    app.connect("127.0.0.1", 7497, clientId=1)
    return app


def websocket_con():
    app.run()


# creating object of the Contract class - will be used as a parameter for other function calls
def usTechStk(symbol, sec_type="STK", currency="USD", exchange="SMART"):
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


def createLimitOrder(action, orderType, totalQuantity, lmtPrice):
    order = Order()
    order.action = action
    order.orderType = orderType
    order.totalQuantity = totalQuantity
    order.lmtPrice = lmtPrice
    return order


app = createConnection()


def main():
    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)

    # starting a separate daemon thread to execute the websocket connection
    con_thread = threading.Thread(target=websocket_con, daemon=True)
    con_thread.start()
    time.sleep(1)  # some latency added to ensure that the connection is established

    # creating object of the Contract class - will be used as a parameter for other function calls
    contract = Contract()
    contract.symbol = "MSFT"
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"

    # creating object of the Contract class - will be used as a parameter for other function calls
    order = Order()
    order.action = "BUY"
    order.orderType = "LMT"
    order.totalQuantity = 1
    order.lmtPrice = 180

    app.placeOrder(app.nextValidOrderId, contract, order)  # EClient function to request contract details
    time.sleep(5)  # some latency added to ensure that the contract details request has been processed


if __name__ == '__main__':
    main()
