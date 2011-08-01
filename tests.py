#!/usr/local/bin/env python
"""Unit tests for scriptable.

Requires:
    - Nose: 'python-nose' in Ubuntu, or 'nose' in PyPI.
    - Coverage: 'python-coverage' in Ubuntu, or 'coverage' in PyPI.

Run like this:
    nosetests --with-coverage --cover-package=scriptable tests.py
"""

import sys
import StringIO
from unittest import TestCase, main

import scriptable
import test_support


class TestAll(TestCase):
    """Test the scriptable method"""

    def setUp(self):
        self.real_stdin = sys.stdin
        self.real_stdout = sys.stdout

        sys.stdin = self.stdin = StringIO.StringIO()
        sys.stdout = self.stdout = StringIO.StringIO()

    def tearDown(self):
        sys.stdin = self.real_stdin
        sys.stdout = self.real_stdout

    def test_str_arr(self):
        """Tests calling with string array"""

        test_str = 'one\ntwo\n'
        self.stdin.write(test_str)
        self.stdin.seek(0)

        scriptable.scriptable('test_support.echo')

        self.stdout.seek(0)
        self.assertEquals(self.stdout.read(), test_str)

    def test_run_via_main(self):
        """Tests running scriptable via 'main' method"""
        test_str = 'one\ntwo\n'
        self.stdin.write(test_str)
        self.stdin.seek(0)

        scriptable.main(['-test-', 'test_support.echo'])

        self.stdout.seek(0)
        self.assertEquals(self.stdout.read(), test_str)

    def test_no_args(self):
        """Test a function that takes no arguments"""
        scriptable.scriptable('test_support.no_args')
        self.stdout.seek(0)

        expected_output = '\n'.join(test_support.NO_ARGS_OUTPUT) + '\n'
        self.assertEquals(self.stdout.read(), expected_output)


    def test_returns_string(self):
        """Test a function that returns a string"""

        test_str = 'one\ntwo\n'
        self.stdin.write(test_str)
        self.stdin.seek(0)

        scriptable.scriptable('test_support.first_of_array')

        self.stdout.seek(0)
        self.assertEquals(self.stdout.read(), test_str.split('\n')[0] + '\n')

    def test_returns_single_value(self):
        """Test a function that doesn't return an iterable."""

        self.stdin.write('any\nthing\n')
        self.stdin.seek(0)

        scriptable.scriptable('test_support.return_int')

        self.stdout.seek(0)
        self.assertEquals(self.stdout.read(), u'42\n')

    def test_usage(self):
        """Test the 'main' method output usage information"""

        argv = ['-test']
        ret = scriptable.main(argv)
        self.assertEquals(ret, 1)

        self.stdout.seek(0)
        self.assertIn('Usage', self.stdout.read())


if __name__ == '__main__':
    main()
