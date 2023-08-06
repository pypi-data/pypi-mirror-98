# This file is placed in the Public Domain.

import unittest

from botl import cfg
from botl.evt import Command

from test.prm import param
from test.run import h

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(cfg.index or 1):
            for cmd in h.modnames:
                exec(cmd)

def exec(cmd):
    exs = getattr(param, cmd, [""])
    for ex in list(exs):
        txt = cmd + " " + ex
        e = Command(txt)
        h.put(e)
        e.wait()