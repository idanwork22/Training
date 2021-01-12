# -*- coding: utf-8 -*-
"""
IBAPI - Fetch Open Orders

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time
import pandas as pd
from coreFunctions import connection_functions,order_functions


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])

    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty,
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


def main():

    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)

    # starting a separate daemon thread to execute the websocket connection
    con_thread = threading.Thread(target=lambda: connection_functions.websocket_con(app), daemon=True)
    con_thread.start()
    time.sleep(1)  # some latency added to ensure that the connection is established
    order_id = app.nextValidOrderId
    #  self, orderId:OrderId , contract:Contract, order:Order -  EClient function to request
    app.placeOrder(order_id, connection_functions.createContract("FB"), order_functions.limitOrder("BUY", 2, 200))
    app.reqOpenOrders()
    time.sleep(1)
    order_df = app.order_df
    order_df.to_csv('check.csv')
    print(order_df)
    time.sleep(5)


if __name__ == '__main__':
    main()