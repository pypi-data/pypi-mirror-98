"""
%aicrowd magic command
"""
import json
import os
import subprocess
from functools import wraps
from typing import Callable, List, Dict, Any

# this will never get called unless you are using ipython (or jupyter)
# since they will already have IPython installed, there's no need to add this as a dependency
# pylint: disable=E0401
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic

# pylint: enable=E0401
from aicrowd.cli import cli


class ExecutionError(Exception):
    """Exception thrown when a shell command exits with non zero code"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "ExecutionError: {0} ".format(self.message)
        else:
            return "ExecutionError: code execution failed"


def is_evaluation_env():
    """Returns true if running as a part of evaluation"""
    return os.getenv("AICROWD_IS_EVALUATING") is not None


def write_array_as_txt(array: List[str], file_path: str):
    """Write the elements of the input array to a file

    Args:
        array: List of elements to write to a file
        file_path: Path to the file that needs to be written
    """
    with open(file_path, "w") as fp:
        fp.write("\n".join(array))


def execute_command(command: str) -> int:
    """Capture the outputs from subprocess and send them to current process'
    stdout

    The output to subprocess' stdout will not be printed on the jupyter
    notebook. So we need to capture the output and print to current process'
    stdout.

    Args:
        command: Bash command to execute

    Returns:
        Exit code of the bash command
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    def print_output(handle):
        if handle is not None:
            output = handle.read()
            if output:
                print(output.decode().strip())

    while True:
        if process.poll() is not None:
            break
        print_output(process.stdout)
        print_output(process.stderr)
    rc = process.poll()
    return rc


def override_evaluation_variables(user_ns: Dict[str, Any]):
    config = user_ns.get("AIcrowdConfig")
    if config is None:
        raise NameError("AIcrowdConfig is not defined")
    config.DATASET_PATH = os.getenv("DATASET_PATH")
    config.PREDICTIONS_PATH = os.path.join(
        os.getenv("OUTPUTS_DIR", "."),
        os.getenv("OUTPUT_FILE_NAME", "predictions.csv"),
    )
    for k, v in json.loads(os.getenv("AICROWD_CONFIG_ENV", "{}")):
        setattr(config, k, v)


def skip_during_evaluation(fn: Callable):
    """Executes notebook cell if not in evaluation mode

    Args:
        fn: Function to wrap
    """

    @wraps(fn)
    def _skipper(self, *args, **kwargs):
        if is_evaluation_env():
            override_evaluation_variables(self.shell.user_ns)
            return

        if len(args) == 2:
            cell = args[1]
        elif len(args) == 3:
            cell = args[2]
        else:
            cell = kwargs["cell"]

        self.shell.run_cell(cell)
        return fn(self, *args, **kwargs)

    return _skipper


def ignore_during_evaluation(fn: Callable):
    """Executes the method when not in evaluation mode

    Args:
        fn: Function to wrap
    """

    @wraps(fn)
    def _skipper(self, *args, **kwargs):
        if is_evaluation_env():
            override_evaluation_variables(self.shell.user_ns)
            return
        return fn(self, *args, **kwargs)

    return _skipper


@magics_class
class AIcrowdMagics(Magics):
    """AIcrowd magic commands"""

    @line_magic
    @ignore_during_evaluation
    def aicrowd(self, line: str):
        """Utility function to expose CLI commands as line magic commands

        Args:
            line: Text written next to the command
        """
        try:
            cli.main(line.split(" "), "%aicrowd")
        except Exception as e:
            print("An error occured:", e)
        except SystemExit:
            # Captures sys.exit from click
            pass

    @cell_magic
    @skip_during_evaluation
    def skip_aicrowd_evaluation(self, line: str, cell: str):
        """Skips the execution of a cell during evaluation

        Args:
            line: Text written next to the command
            cell: Contents of the cell excluding magic command
        """
        pass

    @cell_magic
    @skip_during_evaluation
    def pre_evaluation_steps(self, line: str, cell: str):
        """Skips the execution of a cell during evaluation

        Same as `skip_aicrowd_evaluation`. During the docker build stage
        we will get the contents of this cell and execute them. This is to
        cover complex use cases where it is not possible to get everything
        installed using single `apt install` or `pip install`.

        Args:
            line: Text next to the magic command
            cell: Contents of the cell excluding the magic command
        """
        pass

    @line_magic
    def save_assets(self, line: str):
        config = self.shell.user_ns.get("AIcrowdConfig")
        if config is None:
            raise NameError("`AIcrowdConfig` class is not defined")
        assets_dir = getattr(config, "ASSETS_DIR")
        if assets_dir is None:
            raise AttributeError("`ASSETS_DIR` should be defined on AIcrowdConfig")

    @line_magic
    def install_packages(self, line: str):
        """Install apt and pypi packages specified in `AIcrowdConfig` class

        Args:
            line: Text next to the magic command

        Example:
            To install wget using apt and numpy using pip, the user has to
            populate `AIcrowdConfig` as

            ```python
            class AIcrowdConfig:
                APT_PACKAGES = ["wget"]
                PIP_PACKAGES = ["numpy"]
            ```
        """
        config = self.shell.user_ns.get("AIcrowdConfig")
        if config is None:
            raise NameError("`AIcrowdConfig` class is not defined")

        if is_evaluation_env():
            config.DATASET_PATH = os.getenv("DATASET_PATH")
            config.PREDICTIONS_PATH = os.path.join(
                os.getenv("OUTPUTS_DIR", "."),
                os.getenv("OUTPUT_FILE_NAME", "predictions.csv"),
            )
            return

        apt_packages = getattr(config, "APT_PACKAGES", None)
        if apt_packages is not None:
            cmd = [
                "sudo apt -qq update",
                "sudo apt -qq install -y {}".format(" ".join(apt_packages)),
            ]
            if execute_command(" && ".join(cmd)) != 0:
                raise ExecutionError("Couldn't install apt packages")
            write_array_as_txt(apt_packages, "apt.txt")

        pip_packages = getattr(config, "PIP_PACKAGES", None)
        if pip_packages is not None:
            cmd = "pip install {}".format(" ".join(pip_packages))
            if execute_command(cmd) != 0:
                raise ExecutionError("Couldn't install pip packages")
            write_array_as_txt(pip_packages, "requirements.txt")


def load_ipython_extension(ipython):
    """Register our magic commands with ipython kernel

    The magic commands will be available as an extension amd can be loaded
    using

        %load_ext aicrowd.magic
    """
    ipython.register_magics(AIcrowdMagics)
