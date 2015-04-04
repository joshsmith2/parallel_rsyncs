from base import *

class FunctionalTest(GeneralTest):


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


if __name__ == '__main__':
     unittest.main()