import os
import unittest

from atudomain.git.parsers import GitBranchParser
from tests.util import ResourceReader
from tests import RESOURCES_DIR


MODULE_RESOURCES_DIR = os.path.join(RESOURCES_DIR, "test_GitBranchParser")

git_branch_parser = GitBranchParser()


def test_extract_branch_strings() -> None:
    branches_string_1 = ResourceReader.read(
        file=os.path.join(f"{MODULE_RESOURCES_DIR}", "test_extract_branch_strings_1.txt")
    )
    branch_strings_1 = git_branch_parser._extract_branch_strings(
        branches_string=branches_string_1
    )
    assert [
            '  branch/1/2019',
            '  branch/2/2019',
            '  branch/3/2019',
            '* master'
        ] == branch_strings_1

def test_extract_branches() -> None:
    branches_string_1 = ResourceReader.read(
        file=f"{MODULE_RESOURCES_DIR}/test_extract_branches_1.txt"
    )
    branches = git_branch_parser.extract_branches(
        branches_string=branches_string_1
    )
    assert [
            'master',
            'remotes/origin/master'
        ] == branches
