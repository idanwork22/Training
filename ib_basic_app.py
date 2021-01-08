# -*- coding: utf-8 -*-
"""
IBAPI - EClient and EWrapper classes intro

"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorString))

    def contractDetails(self, reqId, contractDetails):
        print("redID: {}, contract:{}".format(reqId, contractDetails))


def main():
    app = TradingApp()
    app.connect("127.0.0.1", 7497, clientId=1)

    contract = Contract()  # Create contract
    contract.symbol = "AAPL"  # symbol
    contract.secType = "STK"  # Security type
    contract.currency = "USD"  # Currency
    contract.exchange = "SMART"  # necessary exchange

    app.reqContractDetails(100, contract)
    app.run()


if __name__ == '__main__':
    main()
