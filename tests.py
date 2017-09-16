import os
import shlex
import subprocess
import unittest


class TestCompyler(unittest.TestCase):
    def test_compyler(self):
        expected = 'test_output.h'
        actual = 'comp_code.h'

        subprocess.run(
            shlex.split(
                'python3 header.py'))

        self.assertEqual(
            os.path.getsize(expected),
            os.path.getsize(actual))

        with open(expected, 'r') as exp, open(actual, 'r') as act:
            self.assertEqual(
                exp.read(),
                act.read())
