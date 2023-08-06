"""Functions to run processes in behalf of hdev users."""

import subprocess


def run_tox(env, cmd, check=True):
    """Run a `cmd` inside tox environment `env`."""
    return subprocess.run(
        f'tox -e {env} --run-command "{cmd}"', shell=True, check=check
    )  # pragma: no cover
