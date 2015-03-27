from base import *
import subprocess as sp

class FunctionalTest(GeneralTest):

    def test_can_get_help(self):

        output = sp.check_output([self.parallel_rsyncs, "-h"])
        self.assertNotEqual(output, b'')
        self.assertIn("Hopefully it can help you", str(output))

if __name__ == '__main__':
     unittest.main()