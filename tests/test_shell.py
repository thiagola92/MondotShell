import json
from pathlib import Path
from unittest import TestCase

from mondot.error import Error


class TestShell(TestCase):
    def _read_output(self, code_file, page) -> str:
        output_file = f"{code_file}_{page}"

        assert self._output_exists(code_file, page)

        with open(output_file) as f:
            return json.load(f)

    def _output_exists(self, code_file, page) -> bool:
        output_file = f"{code_file}_{page}"
        return Path(output_file).exists()

    def _request_next_output(self, code_file):
        input_file = f"{code_file}_i"
        Path(input_file).write_text("1")

    def _delete_output_files(self, code_file):
        page = 1

        while Path(f"{code_file}_{page}").exists():
            Path(f"{code_file}_{page}").unlink(missing_ok=True)
            page += 1

    def _delete_input_file(self, code_file):
        input_file = f"{code_file}_i"
        Path(input_file).unlink(missing_ok=True)

    def _validate_last_output(self, code_file, page):
        output = self._read_output(code_file, page)

        self._validate_output_format(output)

        assert output["error"] == Error.ERR_FILE_EOF

    def _validate_output_format(self, output):
        assert isinstance(output, dict)
        assert "error" in output
        assert "result" in output
        assert isinstance(output["error"], int)
        assert isinstance(output["result"], list)
