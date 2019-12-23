# tunnel-server
A Linux GRETAP tunnel server &amp; client

## Usage
On the server:

```
sudo server/server.py --bridge br0 eth0
```

Here `eth0` is the interface to listen for connections on and to route
tunnel traffic over.

On the client:

```
sudo client/client.py <IP address of server>
```

## What this does
This creates a GRETAP tunnel between the client and the server.  At
either end of the tunnel, the resulting GRETAP interface can be
attached to a bridge by specifying `--bridge <bridge-name>`.

No attempt is made to monitor the connection or keep it alive.

## What this DOES NOT do
**This is not a VPN.**  If you want a VPN, use a VPN.  This gives you
a virtual layer 2 connection between two hosts, nothing more.  It
implements no authentication, no authorisation and no encryption.

## Why would I want this?
I use this over a layer 3 VPN.  That is, a VPN which can route IP
traffic from one host to another.  A layer 3 VPN is useless if you are
testing Ethernet equipment because Ethernet is a layer 2 protocol and
you can't create an Ethernet connection over a layer 3 VPN.  So a
layer 2 tunnel over the top of the VPN gives you a virtual "Ethernet"
connection between two hosts that don't have a real (direct) Ethernet
connection but can talk to each other by IP.

There are generally three ways of using this:

* **Point to Point** By default, it just creates a GRETAP interface at
  each end of the tunnel.  You are responsible for whatever
  configuration you want on top of that.
* **Join a remote network** In this mode, you are responsible for
  creating a network bridge at one end, let's say it's called `br0`.
  At that end of the tunnel, you specify `--bridge br0` on the command
  line.  That end of the tunnel will be added to the bridge you
  specify.  Suppose that bridge also has an Ethernet interface slaved
  to it which is on an office network; now the other end of the tunnel
  can use its GRETAP interface as though it was a real Ethernet
  interface plugged into that remote network (hint: start a DHCP
  client on the remote end and it'll get an IP address from the office
  network's DHCP server.  IP6 link local addresses will also work over
  it).
* **Join two networks** In this mode, create a bridge at both ends of
  the tunnel and specify `--bridge br0` at both ends.  This lets you
  join two remote networks into a single layer 2 broadcast domain,
  effectively joining them into a single Ethernet network.  **Be
  careful doing this**.  If you bridge your office network onto your
  home network and your home DHCP server starts serving up IP
  addresses for your office network, your IT guy is not likely to be
  impressed.
  
## And let's say this one more time
**THIS IS NOT A VPN.**  Don't use this over the internet unless you
are sure the traffic it's carrying could also be carried safely over
the internet.  If you're not sure, set up a VPN first (eg OpenVPN) and
then start this through the VPN connection.
