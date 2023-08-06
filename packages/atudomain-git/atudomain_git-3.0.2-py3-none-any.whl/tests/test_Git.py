import os
import unittest

from atudomain.git.repository import Git


def test_readonly_methods() -> None:
    git = Git(os.getcwd())
    git.get_commits()
    git.get_branches()
