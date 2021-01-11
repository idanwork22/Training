# -*- coding: utf-8 -*-
"""
IBAPI - Fetch position details
"""

import threading
import time
from coreFunctions import connection_functions


def main():
    app = connection_functions.createConnection()  # create connection
    # starting a separate daemon thread to execute the web socket connection
    con_thread = threading.Thread(target=lambda: connection_functions.websocket_con(app), daemon=True)
    con_thread.start()
    time.sleep(1)  # some latency added to ensure that the connection is established

    app.reqPositions()
    time.sleep(1)
    pos_df = app.pos_df
    print(pos_df)
    time.sleep(1)


if __name__ == '__main__':
    main()
