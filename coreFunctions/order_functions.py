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
