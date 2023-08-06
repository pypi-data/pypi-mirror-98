#
#  Copyright (c) 2020 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Package publish subcommand implementation."""

import copy
import logging
import pathlib
import sys
import typing

import click

from build_harness._utility import (
    CommandArgs,
    command_path,
    report_console_error,
    run_command,
)

from .state import CommandState, ExitState

log = logging.getLogger(__name__)

TWINE_PUBLISH_CMD: CommandArgs = ["twine", "upload", "--non-interactive"]


class PublishingError(Exception):
    """Problem occurred during publishing."""


def _publish_packages(
    venv_path: pathlib.Path,
    is_dryrun: bool,
    password: typing.Optional[str],
    user: typing.Optional[str],
) -> None:
    """
    Publish sdist, wheel packages using twine.

    On dry run no publish occurs, but a summary of packages found that would have
    been published is printed to console.

    Args:
        venv_path: Path to Python virtual environment.
        is_dryrun: Signal if a publish dry run is requested.
        password: Remote repository password.
        user: Remote repository username

    Raises:
        FileNotFoundError: if password file does not exist.
        PublishingError: If package publish exits non-zero.
    """
    this_command = copy.deepcopy(TWINE_PUBLISH_CMD)
    this_command[0] = command_path(venv_path, this_command)
    this_command += ["dist/*.whl", "dist/*.tar.gz"]

    environment_variables = dict()
    if user:
        environment_variables["TWINE_USERNAME"] = user
    if password:
        environment_variables["TWINE_PASSWORD"] = password

    if not is_dryrun:
        result = run_command(
            this_command,
            env=environment_variables,
        )

        if any([x != 0 for x in [result.returncode]]):
            raise PublishingError("twine failed during package publishing.")
    else:
        message = "Dry run, {0}".format(this_command)
        log.warning(message)
        click.echo(message)


@click.command()
@click.pass_context
@click.option(
    "--dryrun",
    default=False,
    help="PEP-440 release id to apply to package. [default: do nothing]",
    is_flag=True,
)
@click.option(
    "--password",
    default=None,
    help="PEP-503 server login password",
    type=str,
)
@click.option(
    "--user",
    default=None,
    help="PEP-503 server login user name",
    type=str,
)
def publish(
    ctx: click.Context,
    dryrun: bool,
    password: typing.Optional[str],
    user: typing.Optional[str],
) -> None:
    """Publish project artifacts."""
    try:
        command_state: CommandState = ctx.obj

        _publish_packages(command_state.venv_path, dryrun, password, user)
    except PublishingError as e:
        message = str(e)
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.PUBLISHING_FAILED)
    except Exception:
        message = "Unexpected error. Check log for details."
        log.exception(message)
        report_console_error(message)
        sys.exit(ExitState.UNKNOWN_ERROR)
