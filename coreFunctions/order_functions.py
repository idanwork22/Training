"""
    This python file contain all the necessary functions about
    all the order types
"""
from ibapi.order import Order


def limitOrder(direction, quantity, lmt_price):
    """
    This function create a limit order
    :param direction: BUY / SELL (the order type)
    :param quantity: the quantity of the stock amount
    :param lmt_price: the limit price
    :return: return order type Order
    """
    order = Order()
    order.action = direction
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmt_price
    return order


def marketOrder(direction, quantity):
    """
    This function create a market order
    :param direction: BUY / SELL (the order type)
    :param quantity: the quantity of the stock amount
    :return: return order type Order
    """
    order = Order()
    order.action = direction
    order.orderType = "MKT"
    order.totalQuantity = quantity
    return order


def stopOrder(direction, quantity, st_price):
    """
    This function create a stop order
    :param direction: BUY / SELL (the order type)
    :param quantity: the quantity of the stock amount
    :param st_price: the stop price
    :return: return order type Order
    """
    order = Order()
    order.action = direction
    order.orderType = "STP"
    order.totalQuantity = quantity
    order.auxPrice = st_price
    return order


def stopLimitOrder(direction,quantity,lmtPrice,stpPrice):
    """
    This function create a stop limit order
    :param direction: BUY / SELL (the order type)
    :param quantity: The quantity of the stock amount
    :param lmtPrice: The limit price
    :param stpPrice: The stop price
    :return:
    """
    order = Order()
    order.action = direction
    order.orderType = "STP LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmtPrice
    order.auxPrice = stpPrice
    return order


def trailStopOrder(direction, quantity, st_price, tr_step=1):
    """

    This function create a stop order
    :param direction: BUY / SELL (the order type)
    :param quantity: the quantity of the stock amount
    :param st_price: the stop price
    :param tr_step: the trail stop
    :return:
    """
    order = Order()
    order.action = direction
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.auxPrice = tr_step
    order.trailStopPrice = st_price
    return order


def cancelWaitingOrders(app,order_id):
    """
    This function cancel the current waiting order
    :param app: the connection to IB - type TradingApp
    :param order_id: The number of the oder_id type int
    :return: Only cancel
    """
    app.cancelOrder(order_id)

