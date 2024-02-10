import subprocess
import sys

from mcwb import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "mcwb", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
