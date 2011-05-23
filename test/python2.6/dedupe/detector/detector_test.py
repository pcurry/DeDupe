

import unittest

# Modules needed to support tests
import os
import os.path
import tempfile

# Module under test
import dedupe.detector.detector as detector

class TestProcessFile(unittest.TestCase):
    
    
    def setUp(self):
        self.sizes = {}
        self.extensions = {}
        self.standard_test_string = '1234567890'

    def tearDown(self):
        del self.sizes
        del self.extensions

    def testTextFile(self):
        tempdir = tempfile.mkdtemp(suffix="_unittest")
        test_extension = 'txt'
        test_filename = 'ima_unittest.' + test_extension
        test_fqn = os.path.join(tempdir, test_filename)
        fout = open(test_fqn, 'w+b')
        fout.write(self.standard_test_string)
        fout.close()
        self.failIf(len(self.standard_test_string) in self.sizes,
                    "self.sizes incorrectly initialized.")
        self.failIf(test_extension in self.extensions,
                    "self.extensions incorrectly initialized.")
        detector.processFilename(test_fqn, self.sizes, self.extensions)
        self.assert_(len(self.standard_test_string) in self.sizes,
                     "Didn't insert length into self.sizes correctly.")
        
        
        

    #def testFileWithoutExtension(self):
        


if __name__ == "__main__":
    unittest.main()
    
            
