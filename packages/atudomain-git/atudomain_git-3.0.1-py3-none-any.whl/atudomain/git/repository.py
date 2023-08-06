#!/usr/bin/env python3

import re
import subprocess

from atudomain.git.objects import Commit
from atudomain.git.parsers import GitBranchParser
from atudomain.git.parsers import GitLogParser

from typing import List


class Git:
    """
    Represents git repository. Can be used to extract Commits and examine branches.
    It can also be used to conveniently run git commands and get their output.

    :param directory: Path to git repository or bare repository.
    :type directory: str
    :param binary_path: Path to directory with git binary.
    :type binary_path: str
    """
    def __init__(
            self,
            directory: str,
            binary_path=''
    ):
        self._binary_path = binary_path
        self._directory = None
        self._build_directory(
            directory=directory
        )
        self._git_log_parser = GitLogParser()
        self._git_branch_parser = GitBranchParser()

    def _build_directory(
            self,
            directory: str
    ) -> None:
        if directory != '/':
            directory = directory.rstrip('/')
        directory = directory.rstrip('\\')
        self._directory = directory
        if self._run('rev-parse --git-dir', check=False).returncode != 0:
            raise NotARepositoryError(directory)

    def _run(
            self,
            command: str,
            check=True
    ) -> subprocess.CompletedProcess:
        """
        Runs git commands and gets their output.

        :param command: Command to run without 'git' and repository location part ie. 'branch -v'.
        :type command: str
        :param check: True if exception should be raised when command return code is not 0.
        :type check: bool
        :return: Result of subprocess.run() execution.
        :rtype: subprocess.CompletedProcess
        """
        path = None
        env = None
        if self._binary_path != '':
            path = self._binary_path + ':PATH'
        if path:
            env = {'PATH': path}
        try:
            return subprocess.run(
                'git -C ' + self._directory + ' ' + command,
                check=check,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                shell=True,
                env=env
            )
        except subprocess.CalledProcessError as error:
            print(error.stderr)
            raise

    def get_commits(
            self,
            revision_range=''
    ) -> List[Commit]:
        """
        Extracts commits from git 'log --pretty=raw' command, creates Commit objects from them
        and appends them to a list.

        :param revision_range: Any revision range that could be used with git log command.
        :type revision_range: str
        :return: List of Commit objects extracted.
        :rtype: List[Commit]
        """
        return self._git_log_parser.extract_commits(
            self._run(
                'log {revision_range} --pretty=raw'.format(
                    revision_range=revision_range
                )
            ).stdout
        )

    def get_branches(
            self,
            include=None,
            exclude=None
    ) -> List[str]:
        """
        Extracts branch names from 'git branch --all' command and appends them to a list.
        Skips redundant information such as current branch pointer ('*') or relations ('->').

        :param include: Regex (re module) to include branch names in list. None means all.
        :type include: str
        :param exclude: Regex (re module) to exclude branch names from list.
        :type exclude: str
        :return: List of branch names.
        :rtype: List[str]
        """
        branches = self._git_branch_parser.extract_branches(
            self._run('branch --all').stdout
        )
        if include is not None:
            branches = [x for x in branches if re.search(include, x)]
        if exclude is not None:
            branches = [x for x in branches if not re.search(exclude, x)]
        return branches


class NotARepositoryError(Exception):
    pass
