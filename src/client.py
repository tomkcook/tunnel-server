#!/usr/bin/env python3

from argparse import ArgumentParser
from util import startTunnel, stopTunnel, addressesForInterface, srcAddressForDst
import logging
import signal
import requests
import socket

def main():
    parser = ArgumentParser()
    parser.add_argument("--bridge", type=str)
    parser.add_argument("remoteIP", type=str)
    args = parser.parse_args()

    try:
        args.remoteIP = socket.gethostbyname(args.remoteIP)
    except:
        logging.error("Unabled to resolve remote host: {}".format(args.remoteIP))
        return
    
    src = srcAddressForDst(args.remoteIP)
    if src is None:
        logging.error("Could not determine source address for destination {}.".format(args.remoteIP))
        return

    response = requests.get("http://{}:5000/connect".format(args.remoteIP))
    if response.status_code != 200:
        logging.error("Could not connect to server: HTTP {}: {}", response.status_code, response.text)
        return
    
    startTunnel(args.remoteIP, src, args.bridge)
    try:
        signal.pause()
    except KeyboardInterrupt:
        stopTunnel(args.remoteIP)

if __name__ == "__main__":
    main()
    
    
