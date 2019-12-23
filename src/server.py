#!/usr/bin/env python3

from flask import Flask
from flask import request
from util import startTunnel, stopTunnel, addressesForInterface
from argparse import ArgumentParser
import logging

app = Flask(__name__)
settings = {}

@app.route("/connect")
def connect():
    address = request.remote_addr
    logging.info("Connect request from {}".format(address))
    startTunnel(address, settings['localIP'], settings['bridge'])
    return "Success", 200

def main():
    global settings
    
    parser = ArgumentParser()
    parser.add_argument("--bridge", type=str)
    parser.add_argument("interface", type=str)
    args = parser.parse_args()

    addrs = addressesForInterface(args.interface)
    if addrs is None:
        logging.error("No such interface: {}".format(args.interface))
        return

    if len(addrs) == 0:
        logging.error("Interface {} has no IP4 address.".format(args.interface))
        return

    settings['localIP'] = addrs[0]
    settings['bridge'] = args.bridge

    app.run(host=addrs[0])

if __name__ == '__main__':
    main()
