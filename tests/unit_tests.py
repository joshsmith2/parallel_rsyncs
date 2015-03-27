from base import *


class UnitTest(GeneralTest):

    def test_creates_dest_if_not_already_extant(self):
        output = str(sp.check_output([self.parallel_rsyncs,
                                      '-s', self.source,
                                      '-d', self.non_existent_dest,
                                      '-l', self.logs,
                                      '-c']))

        message = "Destination does not exist. Creating " + self.non_existent_dest
        self.assertIn(message, output)
        self.check_exists(self.non_existent_dest)


if __name__ == '__main__':
     unittest.main()
