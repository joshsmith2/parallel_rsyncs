from base import *


class FileTest(GeneralTest):

    def test_creates_dest_if_not_already_extant(self):
        self.assertFalse(os.path.exists(self.non_existent_dest))
        output = str(sp.check_output([self.parallel_rsyncs,
                                      '-s', self.source,
                                      '-d', self.non_existent_dest,
                                      '-l', self.logs,
                                      '-c']))

        message = "Destination does not exist. Creating " + self.non_existent_dest
        self.assertIn(message, output)
        self.check_exists(self.non_existent_dest)

    def test_exits_if_dest_not_extant_and_no_c_flag(self):
        self.assertFalse(os.path.exists(self.non_existent_dest))
        with self.assertRaises(sp.CalledProcessError):
            output = str(sp.check_output([self.parallel_rsyncs,
                                          '-s', self.source,
                                          '-d', self.non_existent_dest,
                                          '-l', self.logs]))
            message = "Destination " + self.non_existent_dest + " does not exist." \
                      "Run with -c flag if you'd like to create it."
            self.assertIn(message, output)
        self.assertFalse(os.path.exists(self.non_existent_dest))

class RsyncSyntaxTest(GeneralTest):

    def test_correct_version_of_rsync_used(self):
        default_output = str(sp.check_output(self.minimal_transfer))
        default_path = '/opt/local/bin/rsync' # CAREFUL - PLATFORM DEPENDANT
        self.assertIn(default_path, default_output)

        alternative_path = '/usr/bin/rsync'
        alternative_transfer = self.minimal_transfer
        alternative_transfer.extend(['-b', '/usr/bin/rsync'])
        alternative_output = str(sp.check_output(alternative_transfer))
        self.assertIn(alternative_path, alternative_output)


if __name__ == '__main__':
     unittest.main()
