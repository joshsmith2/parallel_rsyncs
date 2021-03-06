import unittest
import os
import shutil
import subprocess as sp

class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.files = os.path.join(self.current_dir, 'files')
        self.source = os.path.join(self.files, 'source')
        self.dest = os.path.join(self.files, 'dest')
        self.logs = os.path.join(self.files, 'logs')
        self.paths_file = os.path.join(self.files, 'data', 'paths.txt')
        self.full_paths_file = os.path.join(self.files, 'data', 'full_paths.txt')
        self.non_existent_dest = os.path.join(self.current_dir, 'new_dest')
        parallel_rsyncs_messy = os.path.join(self.current_dir,
                                             "../parallel_rsyncs.sh")
        self.parallel_rsyncs = os.path.abspath(parallel_rsyncs_messy)

        self.minimal_transfer = [self.parallel_rsyncs,
                                 '-s', self.source,
                                 '-d', self.dest,
                                 '-l', self.logs,]

        shutil.copytree(os.path.join(self.files, 'data'), self.source)
        self.system_binary = '/opt/local/bin/rsync'
        self.v2_binary = '/usr/bin/rsync'
        if os.path.exists(self.logs):
            shutil.rmtree(self.logs)
        os.mkdir(self.logs)
        if os.path.exists(self.dest):
            shutil.rmtree(self.dest)
        os.mkdir(self.dest)
        self.files_to_delete = []

    def tearDown(self):
        shutil.rmtree(self.source)
        if os.path.exists(self.non_existent_dest):
            shutil.rmtree(self.non_existent_dest)
        for file in self.files_to_delete:
            os.remove(file)
        try:
            shutil.rmtree(self.spaced_source)
        except (AttributeError, FileNotFoundError):
            pass

    def check_exists(self, path, positive=True):
        if positive:
            self.assertTrue(os.path.exists(os.path.abspath(path)),
                            msg=path + " does not exist.")
        else:
            self.assertFalse(os.path.exists(os.path.abspath(path)),
                             msg=path + " exists.")

if __name__ == '__main__':
    unittest.main()