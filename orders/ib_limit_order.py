# -*- coding: utf-8 -*-
"""
IBAPI - placing limit order and storing order id
"""
import threading
import time
from coreFunctions import order_functions
from coreFunctions import connection_functions


def main():
    """
    The main function
    :return:
    """

    app = connection_functions.createConnection()  # Create Connection

    # starting a separate daemon thread to execute the web socket connection
    con_thread = threading.Thread(target=lambda: connection_functions.websocket_con(app), daemon=True)
    con_thread.start()
    time.sleep(1)  # some latency added to ensure that the connection is established

    order_id = app.nextValidOrderId
    #  self, orderId:OrderId , contract:Contract, order:Order -  EClient function to request
    app.placeOrder(order_id, connection_functions.createContract("FB"), order_functions.limitOrder("BUY", 2, 200))
    time.sleep(2)
    print(order_id)
    order_functions.cancelWaitingOrders(app,order_id)
    time.sleep(2)  # some latency added to ensure that the contract details request has been processed


if __name__ == '__main__':
    main()
