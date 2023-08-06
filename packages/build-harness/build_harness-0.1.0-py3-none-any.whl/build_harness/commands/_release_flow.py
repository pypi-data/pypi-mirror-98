#
#  Copyright (c) 2021 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Release flow command entry point."""

import logging
import os
import pathlib
import shutil
import sys
import typing

import click

from build_harness._utility import report_console_error
from build_harness._version import acquire_version
from build_harness.tools.git import (
    DEFAULT_DEFAULT_BRANCH_NAME,
    GitRepoError,
    get_tag_data,
)

from ._declarations import DEFAULT_PROJECT_PATH
from ._release_id import InvalidReleaseId, validate_release_id
from .state import CommandState, ExitState

log = logging.getLogger(__name__)


class GitNotFoundError(Exception):
    """Git executable not found error."""


def _validate_git(optional_git: typing.Optional[str]) -> None:
    """
    Validate that git is installed or the user has provided a valid git path.

    Args:
        optional_git: Path to git executable.

    Raises:
        GitNotFoundError: If git executable not found.
    """
    system_git = shutil.which("git")
    if optional_git:
        system_git = optional_git

    if not system_git:
        raise GitNotFoundError("Git not available on users PATH")
    if not os.path.exists(system_git):
        raise GitNotFoundError("User specified git invalid, {0}".format(system_git))


@click.command()
@click.version_option(version=acquire_version())
@click.option(
    "--default-branch",
    default=DEFAULT_DEFAULT_BRANCH_NAME,
    help="Git default/main branch name.",
    show_default=True,
    type=str,
)
@click.option(
    "--git",
    default=None,
    help="Git executable. [default: users PATH]",
    type=str,
)
@click.option(
    "--project",
    default=DEFAULT_PROJECT_PATH,
    help="Git project directory.",
    show_default=True,
    type=str,
)
def release_flow_main(
    default_branch: str, git: typing.Optional[str], project: str
) -> None:
    """
    Construct a release id from git tag and commit history.

    If HEAD commit is tagged then use the tag as the release id. Otherwise try to
    count the number of commits since the most recent tag, with a PEP-440 constructed
    release id of the form ``<tag>.post<N>``. Note that this implies that the tag
    must be PEP-440 compliant.

    If there are no tags in commit history then a default tag of ``0.0.0`` is
    inferred and the number of commits counted since the root (first) commit in
    commit history.

    The count method is slightly different when there are no tags in commit history
    so it is recommended to tag the root commit with ``0.0.0`` so that the count
    method is always the same.
    """
    try:
        state = CommandState(
            project_path=pathlib.Path(project),
            venv_path=pathlib.Path(sys.argv[0]).parent.absolute(),
        )

        _validate_git(git)

        tag_data = get_tag_data(state.project_path, default_branch)
        tag_version = validate_release_id(tag_data.tag)
        if tag_data.offset:
            updated_version = tag_version.replace(post=int(tag_data.offset))
            release_id = str(updated_version)
        else:
            release_id = str(tag_version)

        click.echo(release_id, err=False, nl=False)
    except InvalidReleaseId as e:
        report_console_error(str(e))
        sys.exit(ExitState.BAD_VERSION)
    except GitRepoError as e:
        report_console_error(str(e))
        sys.exit(ExitState.BAD_REPO)
    except GitNotFoundError as e:
        report_console_error(str(e))
        click.echo("Git must be installed and configured to use this utility.")
        click.echo("In Linux, something like this is necessary:")
        click.echo("    sudo apt install -y git || sudo yum install git")
        click.echo('    git config user.name "Your Name"')
        click.echo('    git config user.email "you@example.com"')
        sys.exit(ExitState.BAD_GIT_EXE)
    except Exception:
        message = "Unexpected error. Check log for details."
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.UNKNOWN_ERROR)
