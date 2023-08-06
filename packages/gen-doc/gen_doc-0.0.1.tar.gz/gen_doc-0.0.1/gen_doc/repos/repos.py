"""
Module for build links to file for next versions
"""
from __future__ import annotations

import os
import re
from pathlib import Path

REGEX_GET_DOMAIN = r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)'


class Repository:
    @property
    def base_url(self) -> str:
        raise NotImplementedError

    def __init__(self, url, branch='master'):
        self.url_repository = url
        self.branch = branch

    def get_path_to_file_in_repository(self, file: Path):
        subclasses = [cls for cls in Repository.__subclasses__()]
        base_url_repository = re.findall(REGEX_GET_DOMAIN, self.url_repository)
        print(base_url_repository)
        for subclass in subclasses:
            if base_url_repository == re.findall(REGEX_GET_DOMAIN, subclass.base_url):
                return subclass.build_url_to_file(file, self.url_repository, self.branch)
        return None

    def build_url_to_file(self):
        raise NotImplementedError


class GitHubRepository(Repository):
    base_url = 'https://github.com'
    'tree/master/'

    @staticmethod
    def build_url_to_file(file: Path, url, branch):
        if str(file)[:2] == '..':
            file_parts = str(file).split(os.sep)[2:]
        else:
            file_parts = str(file).split(os.sep)
        if url.split('.')[-1] == 'git':
            url = '.'.join(url.split('.')[:-1])
        return url + f'/tree/{branch}/' + '/'.join(file_parts)


class GitLabRepository(Repository):
    base_url = 'https://gitlab.com/'

    @staticmethod
    def build_url_to_file(file: Path, url, branch):
        if str(file)[:2] == '..':
            file_parts = str(file).split(os.sep)[2:]
        else:
            file_parts = str(file).split(os.sep)
        if url.split('.')[-1] == 'git':
            url = '.'.join(url.split('.')[:-1])
        return url + f'/-/tree/{branch}/' + '/'.join(file_parts)
