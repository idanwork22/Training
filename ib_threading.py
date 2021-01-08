# -*- coding: utf-8 -*-
"""
IB API - Daemon Threads

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

import threading
import time

def randNumGen():
    for a in range(30):
        print(a)
        time.sleep(1)


def greeting():
    for i in range(10):
        print("Hello")
        time.sleep(1)


def main():
    thr2 = threading.Thread(target=randNumGen)  # creating a separate thread to execute the randNumGen function
    thr2.daemon = True
    thr2.start()  # start execution of randNumGen function on the parallel thread

    greeting()


if __name__ == '__main__':
    main()
