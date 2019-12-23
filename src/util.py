import subprocess
import logging
import netifaces as ni

def command(args):
    logging.warning(args)
    result = subprocess.run(
        args.split(" "),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    return result

def startTunnel(remoteIP, localIP, bridge=None):
    name = remoteIP.replace(" ", "")
    result = command(
        "ip link add {} type gretap remote {} local {}".format(name, remoteIP, localIP))
    if result.returncode != 0:
        logging.error("Failed to start gretap tunnel: {}".format(result.stdout))
        return
    if bridge:
        result = command(
            "ip link set {} master {}".format(name, bridge))
        if result.returncode != 0:
            logging.error("Failed to slave gretap tunnel {} to bridge {}: {}".format(name, bridge, result.stdout))

def stopTunnel(remoteIP):
    name = remoteIP.replace(" ", "")
    result = command("ip link del {}".format(name))

def addressesForInterface(iface, family=ni.AF_INET):
    try:
        return [x['addr'] for x in ni.ifaddresses(iface)[family]]
    except ValueError:
        return None

def srcAddressForDst(dst):
    result = command("ip route get {}".format(dst))
    if result.returncode != 0:
        return None
    words = result.stdout.split(" \n")
    if 'src' not in words:
        return None
    idx = words.index('src')
    return words[idx+1]
