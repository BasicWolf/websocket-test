#!/usr/bin/env python3

import logging
import threading
from time import sleep

from my_bitmex_websocket import BitMEXWebsocket


logger: logging.Logger
loglevel = logging.INFO # logging.DEBUG

bws: BitMEXWebsocket


def main():
    global bws, logger

    logger = setup_logger()

    logger.debug('Initializing BitMEXWebsocket')
    bws = BitMEXWebsocket(
        endpoint="https://testnet.bitmex.com/api/v1",
        symbol="XBTUSD",
        api_key=None,
        api_secret=None,
    )

    cw = threading.Thread(target=compute_worker)
    cw.start()


def compute_worker():
    logger.debug('Starting compute worker')
    while(bws.ws.sock.connected):
        logger.info("Market Depth: %s..." % str(bws.market_depth())[:50])
        logger.info("Recent Trades: %s...\n\n" % str(bws.recent_trades())[:50])
        sleep(10)


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    main()
