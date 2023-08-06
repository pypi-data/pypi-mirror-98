#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

from build_harness._utility import extract_coverage, run_command


class TestRunCommand:
    def test_simple(self, mocker):
        mock_run = mocker.patch("build_harness._utility.subprocess.run")
        command = ["something", "--option"]

        result = run_command(command)

        mock_run.assert_called_once_with(command)
        assert result == mock_run.return_value


class TestExtractCoverage:
    def test_all_caps(self):
        mock_captured_report = """some/file.py                     5      0   100%
--------------------------------------------------------
TOTAL                                  170     44    91%
"""

        result = extract_coverage(mock_captured_report)

        assert result == 91

    def test_camel_case(self):
        mock_captured_report = """some/file.py                     5      0   100%
--------------------------------------------------------
Total                                  170     44    90%
"""

        result = extract_coverage(mock_captured_report)

        assert result == 90

    def test_lower_case(self):
        mock_captured_report = """some/file.py                     5      0   100%
--------------------------------------------------------
total                                  170     44    90%
"""

        result = extract_coverage(mock_captured_report)

        assert result == 90

    def test_zero(self):
        mock_captured_report = """some/file.py                     5      0   100%
--------------------------------------------------------
total                                  170     44    0%
"""

        result = extract_coverage(mock_captured_report)

        assert result == 0

    def test_100(self):
        mock_captured_report = """some/file.py                     5      0   100%
--------------------------------------------------------
total                                  170     44    100%
"""

        result = extract_coverage(mock_captured_report)

        assert result == 100
