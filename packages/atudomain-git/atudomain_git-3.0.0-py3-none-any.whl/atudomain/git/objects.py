#!/usr/bin/env python3

import datetime

from typing import List


class Commit:
    """
    Represents git repository commit as extracted from 'git log --pretty=raw'.
    Stores data as properties and has additional methods for getting dates as strings.
    """
    def __init__(
            self,
            is_merge: bool,
            commit_id: str,
            tree: str,
            parents: List[str],
            author: str,
            author_email: str,
            author_date: datetime.datetime,
            committer: str,
            committer_email: str,
            committer_date: datetime.datetime,
            message: str,
            message_subject: str,
            message_body: str
    ):
        self._is_merge = is_merge
        self._commit_id = commit_id
        self._tree = tree
        self._parents = parents
        self._author = author
        self._author_email = author_email
        self._author_date = author_date
        self._committer = committer
        self._committer_email = committer_email
        self._committer_date = committer_date
        self._message = message
        self._message_subject = message_subject
        self._message_body = message_body

    @property
    def is_merge(self) -> bool:
        """
        :rtype: bool
        """
        return self._is_merge

    @property
    def commit_id(self) -> str:
        """
        :rtype: str
        """
        return self._commit_id

    @property
    def tree(self) -> str:
        """
        :rtype: str
        """
        return self._tree

    @property
    def parents(self) -> List[str]:
        """
        :rtype: List[str]
        """
        return self._parents

    @property
    def author(self) -> str:
        """
        :rtype: str
        """
        return self._author

    @property
    def author_email(self) -> str:
        """
        :rtype: str
        """
        return self._author_email

    @property
    def author_date(self) -> datetime.datetime:
        """
        :rtype: datetime.datetime
        """
        return self._author_date

    @property
    def committer(self) -> str:
        """
        :rtype: str
        """
        return self._committer

    @property
    def committer_email(self) -> str:
        """
        :rtype: str
        """
        return self._committer

    @property
    def committer_date(self) -> datetime.datetime:
        """
        :rtype: datetime.datetime
        """
        return self._committer_date

    @property
    def message(self) -> str:
        """
        :rtype: str
        """
        return self._message

    @property
    def message_subject(self) -> str:
        """
        :rtype: str
        """
        return self._message_subject

    @property
    def message_body(self) -> str:
        """
        :rtype: str
        """
        return self._message_body

    def get_author_date_string(
            self,
            date_format='%Y-%m-%d %H:%M:%S %z'
    ) -> str:
        """
        Converts stored datetime author_date to UTC+0 string date.

        :param date_format: Optional date format as for datetime.strftime method.
        :type date_format: str
        :return: Converted date.
        :rtype: str
        """
        return self._author_date.strftime(
            date_format
        )

    def get_committer_date_string(
            self,
            date_format='%Y-%m-%d %H:%M:%S %z'
    ) -> str:
        """
        Converts stored datetime committer_date to UTC+0 string date.

        :param date_format: Optional date format as for datetime.strftime method.
        :type date_format: str
        :return: Converted date.
        :rtype: str
        """
        return self._committer_date.strftime(
            date_format
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            for attribute in [x for x in dir(self) if not x.startswith('__')]:
                if not hasattr(other, attribute):
                    return False
                else:
                    other_attr = getattr(other, attribute)
                    self_attr = getattr(self, attribute)
                    if not callable(self_attr):
                        if callable(other_attr):
                            return False
                        if self_attr != other_attr:
                            return False
            return True
        else:
            raise NotImplementedError()

    def __ne__(self, other) -> bool:
        return not self == other
