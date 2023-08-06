#
#  Copyright (c) 2021 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import os
import pathlib
import tempfile

from behave import given, then, when

from build_harness._utility import run_command
from tests.ci.support.repo import (
    FeatureDryrunTagOnHead,
    FeatureDryrunTags,
    TagOnDefaultHeadOnFeature,
    TagOnHead,
)

from .support import (
    _install_working_build_harness,
    chdir_project_dir,
    create_venv,
    git_repo_context,
)

DEBUG_INSTALL = False


@given("an environment without git installed")
def step_impl(context):
    # Just check that an error message is emitted for a bad git path. Deeper analysis
    # is done by unit tests.
    context.given_arguments = ["--git", "bad/path"]
    context.tag = "3.1.4"
    context.expected_version = context.tag
    context.create_repo = TagOnHead(context.tag)


@then("emits an install git error message to stderr")
def step_impl(context):
    assert "User specified git invalid" in context.run_result.stderr
    assert (
        "Git must be installed and configured to use this utility"
        in context.run_result.stdout
    )


@given("a working directory that is not a valid git repo")
def step_impl(context):
    context.given_arguments = list()


@when("release flow runs in a working directory that is not a valid git repo")
def step_impl(context):
    with tempfile.TemporaryDirectory() as this_dir:
        working_dir = pathlib.Path(this_dir)
        working_venv = working_dir / ".venv"
        working_venvbin = working_venv / "bin"

        create_venv(working_venv)
        _install_working_build_harness(working_venvbin)
        with chdir_project_dir(working_dir):
            assert os.getcwd() == str(working_dir)

            work_release_flow = working_venvbin / "release-flow"
            this_command = [str(work_release_flow)] + context.given_arguments
            result = run_command(
                this_command, capture_output=True, text=True, universal_newlines=True
            )

            print("result.stdout: {0}".format(result.stdout))
            print("result.stderr: {0}".format(result.stderr))

            context.run_result = result
            context.mock_project = working_dir


@then("emits an invalid git repo error message to stderr")
def step_impl(context):
    assert "Invalid git repository" in context.run_result.stderr


@given("a PEP-440 noncompliant tag is latest tag")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "non_pep440_tag"
    context.expected_version = context.tag
    context.create_repo = TagOnHead(context.tag)


@then("emits a bad tag error to stderr")
def step_impl(context):
    assert "Tags must be PEP-440 compliant" in context.run_result.stderr


@given("a PEP-440 compliant tag on default branch")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "1!2.3a4.dev6"
    context.expected_version = context.tag
    context.create_repo = TagOnHead(context.tag)


@when("release flow extracts the tag data")
def step_impl(context):
    with git_repo_context(context.create_repo, debug_install=DEBUG_INSTALL,) as (
        mock_repo,
        this_rf_command,
    ):
        with chdir_project_dir(mock_repo):
            assert os.getcwd() == str(mock_repo)

            this_command = [str(this_rf_command)] + context.given_arguments
            result = run_command(
                this_command, capture_output=True, text=True, universal_newlines=True
            )

            print("result.stdout: {0}".format(result.stdout))
            print("result.stderr: {0}".format(result.stderr))

            context.run_result = result
            context.mock_project = mock_repo


@then("the utility emits the constructed package version to stdout")
def step_impl(context):
    assert context.run_result.stdout == context.expected_version


@given("the tag excludes a post identifier")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "1!2.3a4.dev6"
    context.expected_version = context.tag


@given("HEAD commit on a feature branch")
def step_impl(context):
    context.expected_version = "1!2.3a4.post2.dev6"
    context.create_repo = TagOnDefaultHeadOnFeature(context.tag)


@given("the tag includes a post identifier")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "1!2.3a4.post11.dev6"


@given("a dryrun tag on default branch")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "1!2.3a4.post11.dev6+dryrun"
    # There's a single tag on default branch that is dryrun so expect the offset from
    # root commit.
    context.expected_version = "0.0.0.post2"
    context.create_repo = TagOnDefaultHeadOnFeature(context.tag)


@given("a PEP-440 compliant release tag on default branch")
def step_impl(context):
    context.given_arguments = list()
    context.tag = "1!2.3a4.dev6"


@given("dryrun tag in feature commit history on HEAD commit")
def step_impl(context):
    # Expect the dryrun tags to be overlooked to find the latest release tag.
    context.expected_version = "3.1+dryrun2"
    context.create_repo = FeatureDryrunTagOnHead(context.tag)


@given("dryrun tags in feature commit history prior to HEAD commit")
def step_impl(context):
    # Expect the dryrun tags to be overlooked to find the latest release tag.
    context.expected_version = "1!2.3a4.post4.dev6"
    context.create_repo = FeatureDryrunTags(context.tag)
