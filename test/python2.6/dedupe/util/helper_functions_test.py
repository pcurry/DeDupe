

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


class TestIsUnvisitedSymlinkDir(unittest.TestCase):
    
    def setUp(self):
        """ Set up the possible cases to test """
        # FIXME: Do this setup once, not once per test.
        self.base_dir_path = tempfile.mkdtemp(suffix='_unit_test')
        self.actual_dir_path = tempfile.mkdtemp(suffix='_unit_test',
                                             dir=self.base_dir_path)
        self.linkdir_path = os.path.join(self.base_dir_path, 'IMA_link_dir')
        os.symlink(self.actual_dir_path, self.linkdir_path)

    def tearDown(self):
        """ Clean up the test paths. """
        os.remove(self.linkdir_path)
        os.rmdir(self.actual_dir_path)
        os.rmdir(self.base_dir_path)
        
    def test_target_dir_was_visited(self):
        visited = { self.actual_dir_path : True }
        realpath = os.path.realpath(self.actual_dir_path)
        if self.actual_dir_path != realpath:
            visited[realpath] = True
        self.assert_(self.actual_dir_path in visited, 
                     "Dictionary key testing false?!?")
        res = helper_functions.is_unvisited_symlink_dir(self.linkdir_path,
                                                        visited)
        self.failIf(res, "Returned true even though target was in visited.")

    def test_link_dir_was_visited(self):
        visited = { self.linkdir_path : True }
        self.assert_(self.linkdir_path in visited, 
                     "Dictionary key testing false?!?")
        res = helper_functions.is_unvisited_symlink_dir(self.linkdir_path,
                                                        visited)
        self.failIf(res, 
                    "Returned true even though linkdir_path was in visited.")


class TestProcessExtension(unittest.TestCase):
    
    def test_normal_filenames(self):
        test_extensions = ['txt', 'avi', 'JPEG', 'py', 'pyc', 'mov', 
                           'wmv', 'mp3']
        test_names = ['kitty', 'RENAME', 'personal', 'CamelCaseMe', 
                          'weird_name_1', 'weird-unixy-name']

        # Cartesian product filename list
        test_filenames = [ '.'.join([name, ext]) 
                           for name in test_names
                           for ext in test_extensions ]
        found_extensions = [ helper_functions.process_extension(test_filename)
                             for test_filename in test_filenames ]
        self.assertEquals(set(found_extensions),
                          set(test_extensions),
                          "Missed or misfiled one or more extensions")

    def test_zero_length_extension(self):
        test_filename = 'just_me.'
        found_extension = helper_functions.process_extension(test_filename)
        self.assertEquals('', found_extension)

    def test_no_extension(self):
        test_filename = 'I_am_myself'
        found_extension = helper_functions.process_extension(test_filename)
        self.assert_(found_extension is None)


if __name__ == "__main__":
    unittest.main()
    
            
