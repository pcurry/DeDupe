import unittest

import dedupe.util.helper_functions as helper_functions

class TestAddOrAppend(unittest.TestCase):
    """ Test that add_or_append works sanely.
    """

    def testAdd(self):
        test_key = 1
        test_value = "one"
        test_dict = {}
        self.assert_(test_key not in test_dict)
        helper_functions.add_or_append(test_key, test_value, test_dict)
        self.assert_(test_key in test_dict)
        self.assertEqual(test_value, test_dict[test_key])
    
    def testAppend(self):
        pass
