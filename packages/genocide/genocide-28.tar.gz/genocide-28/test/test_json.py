# This file is placed in the Public Domain.

"test objects"

# imports

import op
import unittest

# classes

class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = op.O()
        o.test = "bla"
        v = op.json(o)
        self.assertEqual(str(o), v)
    