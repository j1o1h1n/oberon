"""

DisCoS - distribution coordination server 

A multicast RAFT protocol implementation, and nothing to do with Discord or Eris, and that's the honest truth.

"""
import asyncio
import logging
import socket
import struct
import yaml
import capnp
import oberon.oberon_capnp

HEARTBEAT = range(1)

class DiscosProtocol(asyncio.DatagramProtocol):

    def __init__(self, cfg, loop):
        self.cfg = cfg
        self.name = cfg["name"]
        self.loop = loop
        self.address = tuple(self.cfg["connection"]["address"])
        self.build_all_templates()

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        logging.debug('data received "{}"'.format(data.decode()))
        self.transport.close()

    def error_received(self, exc):
        logging.debug('error received:', exc)

    @asyncio.coroutine
    def heartbeat(self):
        while 1:
            yield from asyncio.sleep(1.0)
            logging.debug('sending heartbeat to %s', self.address)
            hb = self.build_heartbeat(self.loop.time())
            self.transport.sendto(hb, self.address)

    def build_heartbeat(self, t):
        hb = self.templates[HEARTBEAT]
        hb.time = t
        hb.type = "heartbeat"
        hb.source = self.name
        # {"type" : "heartbeat", "source" : self.name}
        return hb.to_bytes()

    def build_all_templates(self):
        self.templates = {
            HEARTBEAT : oberon.oberon_capnp.UnsequencedMessage.new_message(),
        }


class Discos:

    def __init__(self, cfg):
        self.cfg = cfg
        self.name = self.cfg["name"]

    def register(self, loop):
        " register with the event loop "
        logging.info("Register %s discos server", self.name)

        MCAST_GRP, MCAST_PORT = self.cfg["connection"]["address"]
        t = asyncio.Task(loop.create_datagram_endpoint(
            lambda: DiscosProtocol(self.cfg, loop), family = socket.AF_INET, proto = socket.IPPROTO_UDP, 
            local_addr = (MCAST_GRP, MCAST_PORT)))
        loop.run_until_complete(t)
        trans, proto = t.result()
        sock = trans.get_extra_info("socket")
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        logging.info("registration complete")
        return proto.heartbeat()


