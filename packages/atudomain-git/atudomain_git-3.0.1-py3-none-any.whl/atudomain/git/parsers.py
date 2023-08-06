#!/usr/bin/env python3

import datetime
import re

from atudomain.git.objects import Commit
from typing import List, Tuple


class GitBranchParser:
    @staticmethod
    def _extract_branch_strings(
            branches_string: str
    ) -> List[str]:
        return branches_string.split('\n')[:-1]

    def extract_branches(
            self,
            branches_string: str
    ) -> List[str]:
        branch_strings = self._extract_branch_strings(branches_string)
        branches = [
            x.strip().replace('* ', '')
            for x in branch_strings
            if not re.search(r'\s->\s', x)
            and not re.search(r'HEAD detached', x)
        ]
        return branches


class GitLogParser:
    @staticmethod
    def _split_person_line(
            person_line: str
    ) -> Tuple[str, str, datetime.datetime]:
        name = re.search(r'(.*)\s<', person_line).group(1)
        email = re.search(r'<(.*)>', person_line).group(1)
        date_source = re.search(r'>\s(.*)', person_line).group(1)
        timestamp, timezone = date_source.split(' ')
        date = datetime.datetime.fromtimestamp(
            int(timestamp),
            tz=datetime.timezone.utc
        )
        return name, email, date

    @staticmethod
    def _extract_commit_strings(
            raw_log_string: str
    ) -> List[str]:
        return re.split(
            r'\n(?=commit\s)',
            raw_log_string
        )

    @staticmethod
    def _extract_commit_id(
            commit_string: str
    ) -> str:
        return re.findall(
            r'(?:^|\n)commit (\w+)',
            commit_string
        )[0]

    @staticmethod
    def _extract_tree(
            commit_string: str
    ) -> str:
        return re.findall(
            r'\ntree (\w+)',
            commit_string
        )[0]

    @staticmethod
    def _extract_parents(
            commit_string: str
    ) -> List[str]:
        return list(
            re.findall(
                r'\nparent (\w+)',
                commit_string
            )
        )

    @staticmethod
    def _extract_author_line(
            commit_string: str
    ) -> str:
        return re.findall(
            r'\nauthor (.*)',
            commit_string
        )[0]

    @staticmethod
    def _extract_committer_line(
            commit_string: str
    ) -> str:
        return re.findall(
            r'\ncommitter (.*)',
            commit_string
        )[0]

    @staticmethod
    def _extract_message(
            commit_string: str
    ) -> str:
        message_lines = [re.sub(r'^\s{4}', '', x) for x in commit_string.split('\n') if re.search(r'^\s{4}', x)]
        message = '\n'.join(message_lines)
        return message.strip()

    @staticmethod
    def _split_message(
            message: str
    ) -> List[str]:
        split = [x.lstrip() for x in message.split('\n', 1)]
        if len(split) < 2:
            split.append('')
        return split

    def extract_commits(
            self,
            raw_log_string: str
    ) -> List[Commit]:
        commits = list()
        for commit_string in self._extract_commit_strings(raw_log_string):

            commit_id = self._extract_commit_id(commit_string)

            tree = self._extract_tree(commit_string)

            parents = self._extract_parents(commit_string)

            is_merge = True if len(parents) > 1 else False

            author_line = self._extract_author_line(commit_string)

            author, author_email, author_date = self._split_person_line(
                person_line=author_line
            )

            committer_line = self._extract_committer_line(commit_string)

            committer, committer_email, committer_date = self._split_person_line(
                person_line=committer_line
            )

            message = self._extract_message(commit_string)

            message_subject, message_body = self._split_message(message)

            commit = Commit(
                is_merge=is_merge,
                commit_id=commit_id,
                tree=tree,
                parents=parents,
                author=author,
                author_email=author_email,
                author_date=author_date,
                committer=committer,
                committer_email=committer_email,
                committer_date=committer_date,
                message=message,
                message_subject=message_subject,
                message_body=message_body
            )

            commits.append(commit)

        return commits
