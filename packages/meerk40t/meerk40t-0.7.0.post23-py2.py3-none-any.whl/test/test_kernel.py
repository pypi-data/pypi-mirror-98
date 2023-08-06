from __future__ import print_function

import unittest

from test import bootstrap


class TestKernel(unittest.TestCase):
    def test_kernel_commands(self):
        """
        Tests all commands with no arguments to test for crashes.

        :return:
        """
        kernel = bootstrap.bootstrap()

        for command in kernel.match("command/.*"):
            cmd = kernel.registered[command]
            if not cmd.regex:
                kernel.console(command.split("/")[-1] + "\n")
