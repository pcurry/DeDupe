

import unittest

# Modules needed to support tests
import os
import os.path
import tempfile

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
        self.assert_(test_key in test_dict)
        self.assertEquals(1, len(test_dict[test_key]))
        helper_functions.add_or_append(test_key, test_value_2, test_dict)
        self.assertEquals(2, len(test_dict[test_key]))
        # Values should always be appended to the list 
        self.assertEquals([test_value_1, test_value_2], test_dict[test_key])
        self.assertNotEqual([test_value_2, test_value_1], test_dict[test_key])

    def testComplicatedUse(self):
        test_key_1 = 1
        test_key_2 = "two"
        test_key_3 = 3
        test_value_1 = "one"
        test_value_2 = "two"
        test_value_3 = 3
        test_dict = { test_key_1 : [test_value_1, test_value_2], 
                      test_key_3 : [] }
        self.assertEquals(2, len(test_dict))
        self.assertEquals(2, len(test_dict[test_key_1]))
        self.assert_(test_key_2 not in test_dict)
        self.assertEquals([], test_dict[test_key_3])
        helper_functions.add_or_append(test_key_1, test_value_3, test_dict)
        self.assertEquals(2, len(test_dict))
        self.assertEquals(3, len(test_dict[test_key_1]))
        helper_functions.add_or_append(test_key_2, test_value_1, test_dict)
        self.assertEquals(3, len(test_dict))
        self.assertEquals(1, len(test_dict[test_key_2]))


class TestIsSymlinkDir(unittest.TestCase):
    
    def setUp(self):
        """ Set up the possible cases to test """
        self.base_dir_path = tempfile.mkdtemp(suffix='_unit_test')
        file_descriptor, filename = tempfile.mkstemp(suffix='_unit_test',
                                                 dir=self.base_dir_path,
                                                 text="I am a test file.") 
        self.actual_file_path = os.path.join(self.base_dir_path, filename)

    def tearDown(self):
        """ Clean up the test paths. """
        os.remove(self.actual_file_path)
        os.rmdir(self.base_dir_path)

    def testNotLinkDir(self):
        self.failIf(helper_functions.is_symlink_dir(self.base_dir_path),
                    "Returned true on a dir that wasn't a link.")
    
    def testNotLinkNotDir(self):
        res = helper_functions.is_symlink_dir(self.actual_file_path)
        self.failIf(res, "Returned true on a regular file.")
        
    def testLinkNotDir(self):
        linkname = 'IMA_file_link_unit_test'
        linkpath = os.path.join(self.base_dir_path, linkname)
        os.symlink(self.actual_file_path, linkpath)
        res = helper_functions.is_symlink_dir(linkpath)
        os.remove(linkpath)
        self.failIf(res, "Returned true on a symlink to a file.")

    def testLinkDir(self):
        linkname = 'IMA_dir_link_unit_test'
        linkpath = os.path.join(self.base_dir_path, linkname)
        realdir = tempfile.mkdtemp(suffix='_unit_test', 
                                   dir=self.base_dir_path)
        os.symlink(realdir, linkpath)
        res = helper_functions.is_symlink_dir(linkpath)
        os.remove(linkpath)
        os.rmdir(realdir)
        self.assert_(res, "Linked dir not correctly identified.")


if __name__ == "__main__":
    unittest.main()
    
            
