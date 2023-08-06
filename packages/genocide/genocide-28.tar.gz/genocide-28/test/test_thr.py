# This file is placed in the Public Domain.

import unittest

from op import cfg
from op.evt import Command
from op.thr import launch

from test.prm import param
from test.run import h

events = []

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()
        h.stop()

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    for cmd in h.modnames:
        for ex in getattr(param, cmd, [""]):
            txt = cmd + " " + ex
            e = Command(txt)
            h.put(e)
            events.append(e)
