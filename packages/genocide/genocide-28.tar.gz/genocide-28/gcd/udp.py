# This file is placed in the Public Domain.

"udp to irc relay"

# imports

import socket
import time

from op import Cfg, Object
from op.bus import Bus
from op.dbs import last
from op.thr import launch

# defines

def init(hdl):
    u = UDP()
    return launch(u.start)

# classes

class Cfg(Cfg):

    host = "localhost"
    port = 5500

    def __init__(self):
        super().__init__()
        self.host = Cfg.host
        self.port = Cfg.port

class UDP(Object):

    def __init__(self):
        super().__init__()
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def output(self, txt, addr):
        Bus.announce(txt.replace("\00", ""))

    def server(self):
        try:
            self._sock.bind((self.cfg.host, self.cfg.port))
        except (socket.gaierror, OSError):
            return
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        last(self.cfg)
        launch(self.server)

# functions

def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))
