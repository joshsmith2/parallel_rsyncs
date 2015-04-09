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
        try:
            output = str(sp.check_output([self.parallel_rsyncs,
                                          '-s', self.source,
                                          '-d', self.non_existent_dest,
                                          '-l', self.logs]))
            self.fail("Script did not exit.")
        except sp.CalledProcessError as e:
            message = "Destination " + self.non_existent_dest + " does not exist." \
                      " Run with -c flag if you'd like to create it."
            self.assertIn(message, str(e.output))
        self.assertFalse(os.path.exists(self.non_existent_dest))

    def test_single_files_are_moved(self):
        singleton_in_source = os.path.join(self.source, 'singleton')
        with open(singleton_in_source, 'w') as f:
            f.write("HERE IT IS THE CONTENT")
        sp.check_call(self.minimal_transfer)

        singleton_in_dest = os.path.join(self.dest, 'singleton')
        self.assertTrue(os.path.exists(singleton_in_dest))

class ArgumentTest(GeneralTest):

    def test_script_fails_with_nonexistent_source(self):
        nonexistant_source = '/tmp/bum/bah/jubble/lop/lop/lop.lop'
        self.assertFalse(os.path.exists(nonexistant_source))
        try:
            output = str(sp.check_output([self.parallel_rsyncs,
                                          '-s', nonexistant_source,
                                          '-d', self.dest,
                                          '-l', self.logs]))
            self.fail("Script did not exit on a nonexistant source")
        except sp.CalledProcessError as e:
            message = "Source " + nonexistant_source + " does not exist." \
            " Nothing to do."
            self.assertIn(message, str(e.output))

    def test_script_fails_with_source_not_specified(self):
        try:
            output = str(sp.check_output([self.parallel_rsyncs,
                                          '-d', self.dest,
                                          '-l', self.logs]))
            self.fail("Script did not exit on unspecified source")
        except sp.CalledProcessError as e:
            message = "Please specify a source with the '-s' flag."
            self.assertIn(message, str(e.output))


class RsyncSyntaxTest(GeneralTest):

    def test_correct_version_of_rsync_used(self):
        default_output = str(sp.check_output(self.minimal_transfer))
        self.assertIn(self.system_binary, default_output)

        alternative_transfer = self.minimal_transfer
        alternative_transfer.extend(['-b', '/usr/bin/rsync'])
        alternative_output = str(sp.check_output(alternative_transfer))
        self.assertIn(self.v2_binary, alternative_output)

        version_message = "You are using rsync version 2"
        self.assertIn(version_message, alternative_output)

    def test_correct_extended_attribute_flag_passed(self):
        v3_flag = "-WrltDX"
        v2_flag = "-WrltDE"
        default_flag = '-WrltD'

        # No ex attrs
        default_output = str(sp.check_output(self.minimal_transfer))
        for flag in [v3_flag, v2_flag]:
            self.assertNotIn(flag, default_output)
        self.assertIn(default_flag, default_output)

        #v3
        v3_transfer = self.minimal_transfer
        v3_transfer.append('-x')
        v3_output = str(sp.check_output(v3_transfer))
        self.assertIn(v3_flag, v3_output)

        #v2
        v2_transfer = self.minimal_transfer
        v2_transfer.extend(['-b', self.v2_binary, '-x'])
        v2_output = str(sp.check_output(v2_transfer))
        self.assertIn(v2_flag, v2_output)

    def test_move_mode_flag_passed(self):
        move_transfer = self.minimal_transfer
        move_transfer.append('-m')
        output = str(sp.check_output(move_transfer))
        self.assertIn('--remove-source-files', output)

class LogFileTest(GeneralTest):

    def test_every_directory_gets_a_log_file(self):
        sp.check_call(self.minimal_transfer)
        for dest in os.listdir(self.dest):
            log_path = os.path.join(self.logs, dest + ".log")
            message = log_path + " does not exist."
            self.assertTrue(os.path.exists(log_path), msg=message)

    def test_every_successful_file_gets_logged(self):
        sp.check_call(self.minimal_transfer)
        for i in range(1,10):
            file_path = os.path.join('root ' + str(i),
                                     'child ' + str(i),
                                     'content.txt')
            file_in_logs = False
            log_file = os.path.join(self.logs, "root " + str(i) + ".log")
            with open (log_file, 'r') as f:
                log_contents = f.readlines()
            for line in log_contents:
                if file_path in line:
                    file_in_logs = True
            self.assertTrue(file_in_logs, msg=file_path + " not logged")

    def test_errors_log_created(self):
        sp.check_call(self.minimal_transfer)
        error_file = os.path.join(self.logs, 'rsync_errors.log')
        self.assertTrue(os.path.exists(error_file))

if __name__ == '__main__':
     unittest.main()
