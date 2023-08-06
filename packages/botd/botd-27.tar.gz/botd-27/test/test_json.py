# This file is placed in the Public Domain.

"test objects"

# imports

import botl
import unittest

# classes

class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = botl.O()
        o.test = "bla"
        v = botl.json(o)
        self.assertEqual(str(o), v)
    