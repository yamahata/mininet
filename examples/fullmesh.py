#!/usr/bin/python

"""
This example creates a multi-controller fullmesh network from
semi-scratch; note a topo object could also be used and
would be passed into the Mininet() constructor.
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.util import custom

Switch = OVSKernelSwitch

def addHost( net, N ):
    "Create host hN and add to net."
    name = 'h%d' % N
    ip = '10.0.0.%d' % N
    return net.addHost( name, ip=ip )

controller_ip = '172.16.3.33'   # XXX

def fullMeshMultiControllerNet(nswitches, nhosts_per_switch, ncontrollers):
    "Create a network with multiple controllers."
    debug("nswtiches %d hosts/switch %d controllers %d\n" %
          (nswitches, nhosts_per_switch, ncontrollers))

    net = Mininet( controller=Controller, switch=Switch)

    print "*** Creating controllers"
    clist = []
    port = 6633
    for c in range(0, ncontrollers):
        debug("controller %d\n" % c)
        clist.append(net.addController(name='c%d' % (c + 1),
                                       controller=RemoteController,
                                       ip=controller_ip,
                                       port=port))
        port += 1

    print "*** Creating switches"
    slist = []
    for s in range(0, nswitches):
        controller = s * ncontrollers / nswitches
        s_n = s + 1
        debug("switch %d controller %d\n" % (s_n, controller))
        switch = net.addSwitch('s%d' % s_n,
                               controller = controller)
        for other in slist:
            #other.linkTo(switch)
            link = custom(TCLink, bw=150)
            other.linkTo(switch, link=link)
        slist.append(switch)

    print "*** Creating hosts"
    hlists = []
    for s in range(0, nswitches):
        hlist = []
        for h in range(0, nhosts_per_switch):
            h_n = s * nhosts_per_switch + h + 1
            host = addHost(net, h_n)
            hlist.append(host)
            slist[s].linkTo(host)
        hlists.append(hlist)

    print "*** Starting network"
    net.start()

    # print "*** wait for nox to be stable"
    # time.sleep(30)

    # print "*** Testing network"
    # net.pingAll()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    #setLogLevel( 'info' )  # for CLI output
    setLogLevel( 'debug' )  # for CLI output
    fullMeshMultiControllerNet(5, 1, 2)
    #fullMeshMultiControllerNet(5, 1, 1)
    #fullMeshMultiControllerNet(3, 1, 1)
