import unittest
import subprocess
import os
import shutil


def run(cmd, verbose=False):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


class Test_cli_mv_regex(unittest.TestCase):

    def test_basic(self):

        for file in ['foo.log', 'bar.log', 'foo.log.bak', 'bar.log.bak']:
            if os.path.isfile(file):
                os.remove(file)

        with open('foo.log', 'w') as file:
            file.write('foo')

        with open('bar.log', 'w') as file:
            file.write('bar')

        run(r'mv_regex -f "(.*)(\.log)" "\1\2.bak" foo.log bar.log')

        self.assertTrue(not os.path.isfile('foo.log'))
        self.assertTrue(not os.path.isfile('bar.log'))
        self.assertTrue(os.path.isfile('foo.log.bak'))
        self.assertTrue(os.path.isfile('bar.log.bak'))

        os.remove('foo.log.bak')
        os.remove('bar.log.bak')

    def test_dryrun(self):

        for file in ['foo.log', 'bar.log', 'foo.log.bak', 'bar.log.bak']:
            if os.path.isfile(file):
                os.remove(file)

        with open('foo.log', 'w') as file:
            file.write('foo')

        with open('bar.log', 'w') as file:
            file.write('bar')

        run(r'mv_regex -n "(.*)(\.log)" "\1\2.bak" foo.log bar.log')

        self.assertTrue(os.path.isfile('foo.log'))
        self.assertTrue(os.path.isfile('bar.log'))
        self.assertTrue(not os.path.isfile('foo.log.bak'))
        self.assertTrue(not os.path.isfile('bar.log.bak'))

        os.remove('foo.log')
        os.remove('bar.log')

    def test_indir(self):

        for dirname in ['mydir']:
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
            os.mkdir(dirname)

        with open('mydir/foo.log', 'w') as file:
            file.write('foo')

        with open('mydir/bar.log', 'w') as file:
            file.write('bar')

        run(r'mv_regex -f "(.*)(\.log)" "\1\2.bak" mydir/foo.log mydir/bar.log')

        self.assertTrue(not os.path.isfile('mydir/foo.log'))
        self.assertTrue(not os.path.isfile('mydir/bar.log'))
        self.assertTrue(os.path.isfile('mydir/foo.log.bak'))
        self.assertTrue(os.path.isfile('mydir/bar.log.bak'))

        for dirname in ['mydir']:
            shutil.rmtree(dirname)


if __name__ == '__main__':

    unittest.main()

