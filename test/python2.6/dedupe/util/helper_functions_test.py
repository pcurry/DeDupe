
import unittest

# Module under test
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
        self.assertEqual([test_value], test_dict[test_key])
    
        
    def testAppend(self):
        test_key = 1
        test_value_1 = 'one'
        test_value_2 = 'two'
        test_dict = {test_key : [test_value_1]}
        self.assertEquals(1, len(test_dict[test_key]))
        helper_functions.add_or_append(test_key, test_value_2, test_dict)
        self.assertEquals(2, len(test_dict[test_key]))
        self.assertEquals([test_value_1, test_value_2], test_dict[test_key])
    

if __name__ == "__main__":
    unittest.main()
    
            
