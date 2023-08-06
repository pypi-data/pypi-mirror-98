# This file is placed in the Public Domain.

import unittest

from botl import cfg, edit
from botl.prs import parse

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parse(cfg, "mods=irc")
        self.assertEqual(cfg.sets.mods, "irc")

    def test_parse2(self):
        parse(cfg, "mods=csl")
        self.assertEqual(cfg.sets.mods, "csl")

    def test_edit(self):
        d = {"mods": "csl"}
        edit(cfg, d)
        self.assertEqual(cfg.mods, "csl")
