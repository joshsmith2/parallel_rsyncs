import unittest
import os
import shutil

class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.files = os.path.join(self.current_dir, 'files')
        self.source = os.path.join(self.files, 'source')
        self.dest = os.path.join(self.files, 'dest')
        self.logs = os.path.join(self.files, 'logs')
        self.parallel_rsyncs_messy = os.path.join(self.current_dir,
                                                  "../parallel_rsyncs.sh")
        self.parallel_rsyncs = os.path.abspath(self.parallel_rsyncs_messy)

        shutil.copytree(os.path.join(self.files, 'data'), self.source)



    def tearDown(self):
        shutil.rmtree(self.source)

if __name__ == '__main__':
    unittest.main()