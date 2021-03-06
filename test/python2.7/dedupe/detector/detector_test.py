

import unittest

# Modules needed to support tests
import os
import os.path
import tempfile

# Module under test
import dedupe.detector.detector as detector

class TestProcessFilename(unittest.TestCase):
    
    def _make_standard_file_at(self, filename):
        fout = open(filename, 'w+b')
        fout.write(self.standard_test_string)
        fout.close()
        

    def setUp(self):
        self.files_by_size = {}
        self.extensions = {}
        self.standard_test_string = '1234567890'
        self.tempdir = tempfile.mkdtemp(suffix="_unittest")

    def tearDown(self):
        del self.files_by_size
        del self.extensions
        os.rmdir(self.tempdir)

    def test_text_file(self):
        test_extension = 'txt'
        test_filename = 'ima_unittest.' + test_extension
        test_fqn = os.path.join(self.tempdir, test_filename)
        self._make_standard_file_at(test_fqn)
        # Check pre-test state
        self.failIf(len(self.standard_test_string) in self.files_by_size,
                    "self.files_by_size incorrectly initialized.")
        self.failIf(test_extension in self.extensions,
                    "self.extensions incorrectly initialized.")
        # Test the function
        detector.process_filename(test_fqn, self.files_by_size, self.extensions)
        self.assert_(len(self.standard_test_string) in self.files_by_size,
                     "Didn't insert length into self.files_by_size correctly.")
        self.assert_(test_extension in self.extensions,
                     "Didn't insert extension into self.extensions correctly.")
        os.remove(test_fqn)
   

if __name__ == "__main__":
    unittest.main()
    
            
