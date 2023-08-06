"""
Top level helpers
"""
import os
import subprocess
import uuid
from typing import Any

import click
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from tqdm.auto import tqdm

from aicrowd.utils.jupyter import is_jupyter


def is_subsequence(s1: str, s2: str) -> bool:
    """
    returns whether s1 is a subsequence of s2 or not

    Args:
        s1: probable subsequence of s2
        s2: string

    Returns:
        is s1 a subsequence of s2
    """
    i, j = 0, 0
    n1, n2 = len(s1), len(s2)

    while i < n1 and j < n2:
        # if matched, advance in both
        if s1[i] == s2[j]:
            i += 1

        # otherwise, try next char in s2
        j += 1

    # was s1 fully matched?
    return i == n1


class AliasedGroup(click.Group):
    """
    Click group allowing using prefix of command instead of the whole command
    """

    def get_command(self, ctx, cmd_name):
        """
        Returns a command of which the given word is a subsequence
        """
        rv = click.Group.get_command(self, ctx, cmd_name)

        if rv is not None:
            return rv

        matches = list(
            filter(
                lambda cmd_orig: is_subsequence(cmd_name, cmd_orig),
                self.list_commands(ctx),
            )
        )

        if not matches:
            return None

        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])

        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")
        return None


def zip_fs_path(fs_path: str, target_zip_path: str):
    fs_path = fs_path.replace(".zip", "")
    if not os.path.exists(fs_path):
        raise FileNotFoundError(f"The path {fs_path} does not exist")
    if (
        subprocess.run(f"zip -r '{target_zip_path}' '{fs_path}'", shell=True).returncode
        != 0
    ):
        raise Exception(f"Failed to zip {fs_path}")


class ProgressBar:
    def add(self, filename: str, total: int):
        raise NotImplementedError

    def update(self, progress_bar_id: Any, step: int):
        raise NotImplementedError

    def close(self, progress_bat_id: Any):
        raise NotImplementedError


class RichProgressBar(ProgressBar):
    def __init__(self):
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.progress.console.is_jupyter = is_jupyter()
        self._tasks = []

    def add(self, filename: str, total: int, **kwargs):
        task_id = self.progress.add_task(
            "download",
            filename=filename,
            total=total,
            start=True,
            refresh=True,
            **kwargs,
        )
        self._tasks.append(task_id)
        return task_id

    def update(self, progress_bar_id: TaskID, step: int):
        self.progress.update(progress_bar_id, advance=step, refresh=True)

    def close(self, progress_bar_id: TaskID):
        pass


class TqdmProgressBar(ProgressBar):
    def __init__(self):
        self.bars = {}

    def add(self, filename: str, total: int, **kwargs):
        bar_id = uuid.uuid4()
        self.bars[bar_id] = tqdm(
            desc=filename, total=total, unit="B", unit_scale=True, **kwargs
        )
        return bar_id

    def update(self, progress_bar_id: Any, step: int, **kwargs):
        self.bars[progress_bar_id].update(step, **kwargs)

    def close(self, progress_bar_id: str):
        self.bars[progress_bar_id].close()
