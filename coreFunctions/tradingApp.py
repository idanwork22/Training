"""
    This python file will be the TradingApp class for
    all the other python files that need to connect to
    IB server
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd


class TradingApp(EWrapper, EClient):

    def __init__(self):
        """
        The init function - were the TradingApp type
        first create
        """
        EClient.__init__(self, self)
        self.data = {}  # for the historical data
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])  # for order situation
        # account summary
        self.acc_summary = pd.DataFrame(columns=['ReqId', 'Account', 'Tag', 'Value', 'Currency'])
        # account P&L
        self.pnl_summary = pd.DataFrame(columns=['ReqId', 'DailyPnL', 'UnrealizedPnL', 'RealizedPnL'])
        # position details - in the portfolio
        self.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'Position', 'Avg cost'])

    def position(self, account, contract, position, avgCost):
        """
        set the pos_df in Portfolio positions -> Account Symbol  Position  Avg cost
        """
        super().position(account, contract, position, avgCost)
        dictionary = {"Account": account, "Symbol": contract.symbol,
                      "Position": position, "Avg cost": avgCost}
        self.pos_df = self.pos_df.append(dictionary, ignore_index=True)

    def accountSummary(self, reqId, account, tag, value, currency):
        """
        set in acc_summary the account
        """
        super().accountSummary(reqId, account, tag, value, currency)
        dictionary = {"ReqId": reqId, "Account": account, "Tag": tag, "Value": value, "Currency": currency}
        self.acc_summary = self.acc_summary.append(dictionary, ignore_index=True)

    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        """
        set in pnl_summary the p&l data
        """
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        dictionary = {"ReqId": reqId, "DailyPnL": dailyPnL, "UnrealizedPnL": unrealizedPnL, "RealizedPnL": realizedPnL}
        self.pnl_summary = self.pnl_summary.append(dictionary, ignore_index=True)

    def openOrder(self, orderId, contract, order, orderState):
        """
        put in order_df the situation about all the open orders in the system
        """
        super().openOrder(orderId, contract, order, orderState)
        dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId,
                      "Account": order.account, "Symbol": contract.symbol,
                      "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty,
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def nextValidId(self, orderId):
        """
        Set the nextValidId and prints him
        """
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

    def error(self, reqId, errorCode, errorString):
        """
        The error message
        """
        print("Error {} {} {}".format(reqId, errorCode, errorString))

    def historicalData(self, reqId, bar):
        """
        Get the historical data about the kennels
        :param reqId:  request id
        :param bar: the bar size
        :return: prints the message
        """
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
