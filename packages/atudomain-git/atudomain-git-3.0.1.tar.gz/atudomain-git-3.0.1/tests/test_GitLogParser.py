import datetime
import os
import unittest

from atudomain.git.objects import Commit
from atudomain.git.parsers import GitLogParser
from tests.util import ResourceReader
from tests import RESOURCES_DIR


MODULE_RESOURCES_DIR = os.path.join(RESOURCES_DIR, "test_GitLogParser")

git_log_parser = GitLogParser()


def test_extract_commits() -> None:
    raw_log_string_1 = ResourceReader.read(
        file=os.path.join(f"{MODULE_RESOURCES_DIR}","test_extract_commits_1.txt")
    )

    commits = git_log_parser.extract_commits(
        raw_log_string=raw_log_string_1
    )

    assert 5 == len(commits)

    commit = Commit(
        is_merge=False,
        commit_id="6b934071528ebac0cf38cb051121228d268d9ed6",
        tree="20c24b3631ef204a9820e808847eec9cfc787055",
        parents=["a726619390acd3989a7e1b07b4cebf7da952ddbd"],
        author="Adrian Tuzimek",
        author_email="tuziomek@gmail.com",
        author_date=datetime.datetime(
            year=2019,
            month=11,
            day=8,
            hour=22,
            minute=53,
            second=44,
            tzinfo=datetime.timezone.utc
        ),
        committer="Adrian Tuzimek",
        committer_email="tuziomek@gmail.com",
        committer_date=datetime.datetime(
            year=2019,
            month=11,
            day=8,
            hour=22,
            minute=53,
            second=44,
            tzinfo=datetime.timezone.utc
        ),
        message="Added tests",
        message_subject="Added tests",
        message_body=""
    )

    assert commit == commits[0]
