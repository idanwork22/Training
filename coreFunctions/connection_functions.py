from ibapi.client import EClient  # create connection
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract  # get information about stocks


class TradingApp(EWrapper, EClient):
    """
        TradingApp class
    """

    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorString))

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

    """
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
        """


def websocket_con(app):
    """
    :param app: type TradingApp
    :return: run the app
    """
    app.run()


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


# creating object of the Contract class - will be used as a parameter for other function calls
def createContract(symbol, sec_type="STK", currency="USD", exchange="SMART"):
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


def histData(app, req_num, contract, duration, candle_size):
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
