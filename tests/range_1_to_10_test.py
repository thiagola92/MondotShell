import time
import unittest
from subprocess import Popen

from test_shell import TestShell

from mondot_shell.error import ERR_FILE_EOF
from mondot_shell.page import Page


class HelloWorldTest(TestShell):
    def setUp(self):
        self.code_file = "tests/code/list/range_1_to_10.py"
        self.tmp_file = "tmp/tmp.py"
        self.process = Popen(
            f"python run.py --code-path {self.code_file} --tmp-path  {self.tmp_file}",
            shell=True,
        )

    def tearDown(self):
        self._delete_output_files(self.code_file)
        self.process.kill()

    def test_range_1_to_10(self):
        time.sleep(1)

        page: Page = self._read_output(self.code_file, 0)
        self._validate_output(page)

        assert not self._output_exists(self.code_file, 1)

    def _validate_output(self, page: Page):
        assert page.error_code == ERR_FILE_EOF
        assert page.result == list(range(10))
        assert page.number == 0


if __name__ == "__main__":
    unittest.main()
