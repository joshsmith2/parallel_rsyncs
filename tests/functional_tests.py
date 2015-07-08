from base import *

class FunctionalTest(GeneralTest):

    def make_full_paths_file(self):
        with open(self.full_paths_file, 'w') as fpf:
            with open(self.paths_file, 'r') as pf:
                for line in pf.readlines():
                    full_path = os.path.join(self.source, line)
                    fpf.write(full_path)
            fpf.write('\n')


    def test_can_get_help(self):
        output = sp.check_output([self.parallel_rsyncs, "-h"])
        self.assertNotEqual(output, b'')
        self.assertIn("Hopefully it can help you", str(output))

    def test_files_get_there_safely(self):
        sp.check_call([self.parallel_rsyncs,
                       '-s', self.source,
                       '-d', self.dest,
                       '-l', self.logs])
        for i in range(10):
            dest_root = os.path.join(self.dest, 'root ' + str(i+1))
            dest_child = os.path.join(dest_root, 'child ' + str(i+1))
            dest_content = os.path.join(dest_child, 'content.txt')

            self.check_exists(dest_root)
            self.check_exists(dest_child)
            self.check_exists(dest_content)

            with open(dest_content, 'r') as content:
                lines = [l.strip() for l in content.readlines()]
            self.assertIn('CONTENT IS HERE', lines)

    def test_you_can_read_paths_from_a_file_and_move_them_ok(self):
        self.make_full_paths_file()
        sp.check_call([self.parallel_rsyncs,
                       '-d', self.dest,
                       '-l', self.logs,
                       '-f', self.full_paths_file])
        for i in range(10):
            root = os.path.join(self.dest, 'root ' + str(i))
            child = os.path.join(self.dest, 'child ' + str(i))
            if i in [1, 8]:
                self.check_exists(root)
            elif i == 3:
                self.check_exists(child)
            else:
                self.check_exists(root, positive=False)


if __name__ == '__main__':
     unittest.main()