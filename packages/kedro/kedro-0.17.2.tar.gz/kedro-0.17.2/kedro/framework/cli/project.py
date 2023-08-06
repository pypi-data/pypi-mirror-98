# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""A collection of CLI commands for working with Kedro project."""

import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Sequence

import click
from click import secho

from kedro.framework.cli.utils import (
    KedroCliError,
    _check_module_importable,
    call,
    command_with_verbosity,
    env_option,
    forward_command,
    ipython_message,
    python_call,
)
from kedro.framework.startup import ProjectMetadata

NO_DEPENDENCY_MESSAGE = """{module} is not installed. Please make sure {module} is in
{src}/requirements.txt and run `kedro install`."""
LINT_CHECK_ONLY_HELP = """Check the files for style guide violations, unsorted /
unformatted imports, and unblackened Python code without modifying the files."""
OPEN_ARG_HELP = """Open the documentation in your default browser after building."""


def _build_reqs(source_path: Path, args: Sequence[str] = ()):
    """Run `pip-compile requirements.in` command.

    Args:
        source_path: Path to the project `src` folder.
        args: Optional arguments for `pip-compile` call, e.g. `--generate-hashes`.

    """
    requirements_in = source_path / "requirements.in"

    if not requirements_in.is_file():
        secho("No requirements.in found. Copying contents from requirements.txt...")
        requirements_txt = source_path / "requirements.txt"
        shutil.copyfile(str(requirements_txt), str(requirements_in))

    python_call("piptools", ["compile", "-q", *args, str(requirements_in)])


@click.group()
def project_group():
    """Collection of project commands."""


@forward_command(project_group, forward_help=True)
@click.pass_obj  # this will pass the metadata as first argument
def test(metadata: ProjectMetadata, args, **kwargs):  # pylint: disable=unused-argument
    """Run the test suite."""
    try:
        _check_module_importable("pytest")
    except KedroCliError as exc:
        source_path = metadata.source_dir
        raise KedroCliError(
            NO_DEPENDENCY_MESSAGE.format(module="pytest", src=str(source_path))
        ) from exc
    else:
        python_call("pytest", args)


@command_with_verbosity(project_group)
@click.option("-c", "--check-only", is_flag=True, help=LINT_CHECK_ONLY_HELP)
@click.argument("files", type=click.Path(exists=True), nargs=-1)
@click.pass_obj  # this will pass the metadata as first argument
def lint(
    metadata: ProjectMetadata, files, check_only, **kwargs
):  # pylint: disable=unused-argument
    """Run flake8, isort and black."""
    source_path = metadata.source_dir
    package_name = metadata.package_name
    files = files or (str(source_path / "tests"), str(source_path / package_name))

    if "PYTHONPATH" not in os.environ:
        # isort needs the source path to be in the 'PYTHONPATH' environment
        # variable to treat it as a first-party import location
        os.environ["PYTHONPATH"] = str(source_path)  # pragma: no cover

    for module_name in ("flake8", "isort", "black"):
        try:
            _check_module_importable(module_name)
        except KedroCliError as exc:
            raise KedroCliError(
                NO_DEPENDENCY_MESSAGE.format(module=module_name, src=str(source_path))
            ) from exc

    python_call("black", ("--check",) + files if check_only else files)
    python_call("flake8", files)

    check_flag = ("-c",) if check_only else ()
    python_call("isort", (*check_flag, "-rc") + files)  # type: ignore


@project_group.command()
@click.option(
    "--build-reqs/--no-build-reqs",
    "compile_flag",
    default=None,
    help="Run `pip-compile` on project requirements before install. "
    "By default runs only if `src/requirements.in` file doesn't exist.",
)
@click.pass_obj  # this will pass the metadata as first argument
def install(metadata: ProjectMetadata, compile_flag):
    """Install project dependencies from both requirements.txt
    and environment.yml (optional)."""
    # we cannot use `context.project_path` as in other commands since
    # context instantiation might break due to missing dependencies
    # we attempt to install here
    source_path = metadata.source_dir
    environment_yml = source_path / "environment.yml"
    requirements_in = source_path / "requirements.in"
    requirements_txt = source_path / "requirements.txt"

    if environment_yml.is_file():
        call(["conda", "env", "update", "--file", str(environment_yml), "--prune"])

    default_compile = bool(compile_flag is None and not requirements_in.is_file())
    do_compile = compile_flag or default_compile
    if do_compile:
        _build_reqs(source_path)

    pip_command = ["install", "-U", "-r", str(requirements_txt)]

    if os.name == "posix":
        python_call("pip", pip_command)
    else:
        command = [sys.executable, "-m", "pip"] + pip_command
        proc = subprocess.Popen(
            command, creationflags=subprocess.CREATE_NEW_CONSOLE, stderr=subprocess.PIPE
        )
        _, errs = proc.communicate()
        if errs:
            secho(errs.decode(), fg="red")
            raise click.exceptions.Exit(code=1)
    secho("Requirements installed!", fg="green")


@forward_command(project_group, forward_help=True)
@env_option
@click.pass_obj  # this will pass the metadata as first argument
def ipython(
    metadata: ProjectMetadata, env, args, **kwargs
):  # pylint: disable=unused-argument
    """Open IPython with project specific variables loaded."""
    _check_module_importable("IPython")

    os.environ["IPYTHONDIR"] = str(metadata.project_path / ".ipython")
    if env:
        os.environ["KEDRO_ENV"] = env
    if "-h" not in args and "--help" not in args:
        ipython_message()
    call(["ipython"] + list(args))


@project_group.command()
@click.pass_obj  # this will pass the metadata as first argument
def package(metadata: ProjectMetadata):
    """Package the project as a Python egg and wheel."""
    source_path = metadata.source_dir
    call(
        [sys.executable, "setup.py", "clean", "--all", "bdist_egg"],
        cwd=str(source_path),
    )
    call(
        [sys.executable, "setup.py", "clean", "--all", "bdist_wheel"],
        cwd=str(source_path),
    )


@project_group.command("build-docs")
@click.option(
    "--open",
    "-o",
    "open_docs",
    is_flag=True,
    multiple=False,
    default=False,
    help=OPEN_ARG_HELP,
)
@click.pass_obj  # this will pass the metadata as first argument
def build_docs(metadata: ProjectMetadata, open_docs):
    """Build the project documentation."""
    source_path = metadata.source_dir
    package_name = metadata.package_name

    python_call("pip", ["install", str(source_path / "[docs]")])
    python_call("pip", ["install", "-r", str(source_path / "requirements.txt")])
    python_call("ipykernel", ["install", "--user", f"--name={package_name}"])
    shutil.rmtree("docs/build", ignore_errors=True)
    call(
        [
            "sphinx-apidoc",
            "--module-first",
            "-o",
            "docs/source",
            str(source_path / package_name),
        ]
    )
    call(["sphinx-build", "-M", "html", "docs/source", "docs/build", "-a"])
    if open_docs:
        docs_page = (Path.cwd() / "docs" / "build" / "html" / "index.html").as_uri()
        secho(f"Opening {docs_page}")
        webbrowser.open(docs_page)


@forward_command(project_group, name="build-reqs")
@click.pass_obj  # this will pass the metadata as first argument
def build_reqs(
    metadata: ProjectMetadata, args, **kwargs
):  # pylint: disable=unused-argument
    """Build the project dependency requirements."""
    source_path = metadata.source_dir
    _build_reqs(source_path, args)
    secho(
        "Requirements built! Please update requirements.in "
        "if you'd like to make a change in your project's dependencies, "
        "and re-run build-reqs to generate the new requirements.txt.",
        fg="green",
    )


@command_with_verbosity(project_group, "activate-nbstripout")
@click.pass_obj  # this will pass the metadata as first argument
def activate_nbstripout(
    metadata: ProjectMetadata, **kwargs
):  # pylint: disable=unused-argument
    """Install the nbstripout git hook to automatically clean notebooks."""
    source_path = metadata.source_dir
    secho(
        (
            "Notebook output cells will be automatically cleared before committing"
            " to git."
        ),
        fg="yellow",
    )

    try:
        _check_module_importable("nbstripout")
    except KedroCliError as exc:
        raise KedroCliError(
            NO_DEPENDENCY_MESSAGE.format(module="nbstripout", src=str(source_path))
        ) from exc

    try:
        res = subprocess.run(  # pylint: disable=subprocess-run-check
            ["git", "rev-parse", "--git-dir"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if res.returncode:
            raise KedroCliError("Not a git repository. Run `git init` first.")
    except FileNotFoundError as exc:
        raise KedroCliError("Git executable not found. Install Git first.") from exc

    call(["nbstripout", "--install"])
