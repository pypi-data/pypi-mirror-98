#
#  Copyright (c) 2021 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import pathlib
import tempfile

import pytest

from build_harness import __version__
from build_harness.commands._release_flow import (
    GitNotFoundError,
    _validate_git,
    release_flow_main,
)
from build_harness.commands.state import ExitState
from build_harness.tools.git import TagData
from tests.ci.support.click_runner import click_runner  # noqa: F401


class TestValidateGit:
    def test_system_clean(self, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.shutil.which",
            return_value="/usr/bin/git",
        )

        _validate_git(None)

    def test_system_bad(self, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.shutil.which", return_value=None
        )

        with pytest.raises(GitNotFoundError, match=r"^Git not available on users PATH"):
            _validate_git(None)

    def test_user_precedence(self, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.shutil.which",
            return_value="/usr/bin/git",
        )
        mock_exists = mocker.patch(
            "build_harness.commands._release_flow.os.path.exists", return_value=True
        )

        _validate_git("some/other/path")

        mock_exists.assert_called_once_with("some/other/path")

    def test_user_clean(self, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.shutil.which", return_value=None
        )
        mocker.patch(
            "build_harness.commands._release_flow.os.path.exists", return_value=True
        )

        _validate_git("some/other/path")

    def test_user_bad(self, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.shutil.which", return_value=None
        )

        with pytest.raises(GitNotFoundError, match=r"^User specified git invalid"):
            _validate_git("some/other/path")


class TestReleaseFlowMain:
    def test_clean(self, click_runner, mocker):
        mocker.patch(
            "build_harness.commands._release_flow.get_tag_data",
            return_value=TagData(tag="3.14.159", offset="11"),
        )

        result = click_runner.invoke(release_flow_main, [])

        assert result.exit_code == 0
        assert result.output == "3.14.159.post11"

    def test_default(self, click_runner, mocker):
        mock_get_tag = mocker.patch(
            "build_harness.commands._release_flow.get_tag_data",
            return_value=TagData(tag="3.14.159"),
        )
        result = click_runner.invoke(release_flow_main, [])

        assert result.exit_code == 0
        mock_get_tag.assert_called_once_with(pathlib.Path("."), "master")
        assert result.output == "3.14.159"

    def test_existing_post_overwritten(self, click_runner, mocker):
        mock_get_tag = mocker.patch(
            "build_harness.commands._release_flow.get_tag_data",
            return_value=TagData(tag="3.14.159.post5", offset="11"),
        )
        result = click_runner.invoke(release_flow_main, [])

        assert result.exit_code == 0
        mock_get_tag.assert_called_once_with(pathlib.Path("."), "master")
        assert result.output == "3.14.159.post11"

    def test_project(self, click_runner, mocker):
        expected_repo_path = "some/path"
        mock_get_tag = mocker.patch(
            "build_harness.commands._release_flow.get_tag_data",
            return_value=TagData(tag="3.14.159", offset=11),
        )

        result = click_runner.invoke(
            release_flow_main, ["--project", expected_repo_path]
        )

        assert result.exit_code == 0
        mock_get_tag.assert_called_once_with(
            pathlib.Path(expected_repo_path), mocker.ANY
        )
        assert result.output == "3.14.159.post11"

    def test_bad_repo(self, click_runner):
        with tempfile.TemporaryDirectory() as this_dir:
            result = click_runner.invoke(release_flow_main, ["--project", this_dir])

            assert result.exit_code == ExitState.BAD_REPO
            assert "FAILED: Invalid git repository" in result.output

    def test_bad_git(self, click_runner, mocker):
        mocker.patch(
            "build_harness.commands._release_flow._validate_git",
            side_effect=GitNotFoundError("Git must be installed to use this utility"),
        )
        result = click_runner.invoke(release_flow_main, ["--git", "bad/path"])

        assert result.exit_code == ExitState.BAD_GIT_EXE
        assert (
            "Git must be installed and configured to use this utility" in result.output
        )
        assert "sudo apt install -y git || sudo yum install git" in result.output

    def test_default_branch(self, click_runner, mocker):
        expected_branch = "alternate_main"
        mock_get_tag = mocker.patch(
            "build_harness.commands._release_flow.get_tag_data",
            return_value=TagData(tag="3.14.159"),
        )

        result = click_runner.invoke(
            release_flow_main, ["--default-branch", expected_branch]
        )

        assert result.exit_code == 0
        mock_get_tag.assert_called_once_with(mocker.ANY, expected_branch)

    def test_help(self, click_runner):
        result = click_runner.invoke(release_flow_main, ["--help"])

        assert result.exit_code == 0
        assert "Usage: release-flow-main" in result.output

    def test_version(self, click_runner):
        result = click_runner.invoke(release_flow_main, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.output
