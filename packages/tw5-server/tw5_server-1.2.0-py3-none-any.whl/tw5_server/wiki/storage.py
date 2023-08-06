import abc
from functools import cached_property
from pathlib import Path
import os
import shutil
import sys
from urllib.request import urlretrieve

from git import Repo
from git.util import Actor
from tw5_server.settings import CONFIG


class WikiABC(abc.ABC):
    FILENAME = 'index.html'
    ROOT = CONFIG['TW5_WIKI_ROOT']

    def __init__(self, name):
        self.name = name
        self.file = self.ROOT / name / self.FILENAME

    def exists(self):
        return self.file.exists()

    @classmethod
    def initialize(cls, name):
        root = cls.ROOT / name
        filepath = root / cls.FILENAME
        if filepath.exists():
            raise ValueError(f'{name} already exists at {filepath}')
        cls.download_template()
        cls._init_storage(root)
        sys.stdout.write(f'file generated at {filepath}\n')
        return cls(name)

    @abc.abstractclassmethod
    def _init_storage(cls, root):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @staticmethod
    def download_template():
        if CONFIG['TW5_TEMPLATE_FILE'].exists():
            return
        url = CONFIG['TW5_TEMPLATE_URL']
        if not CONFIG['TW5_TEMPLATE_FILE'].parent.exists():
            os.makedirs(CONFIG['TW5_TEMPLATE_FILE'].parent)
        sys.stdout.write(f'downloading template from {url}')
        urlretrieve(url, CONFIG['TW5_TEMPLATE_FILE'])


class GitStorage(WikiABC):
    AUTHOR = Actor('tw5_server', '')

    @cached_property
    def repo(self):
        return Repo(self.ROOT / self.name)

    @classmethod
    def _init_storage(cls, root):
        if not root.exists():
            os.makedirs(root)
        try:
            repo = Repo.init(root)
            filepath = root / cls.FILENAME
            shutil.copy(CONFIG['TW5_TEMPLATE_FILE'], filepath)
            repo.index.add(cls.FILENAME)
            repo.index.commit('automatic create', author=cls.AUTHOR)
        except Exception as err:
            if root.exists():
                shutil.rmtree(root)
            raise err

    def update(self, file_obj):
        with open(self.file, 'wb') as f:
            shutil.copyfileobj(file_obj, f)
        self.repo.index.add(self.FILENAME)
        self.repo.index.commit('automatic commit', author=self.AUTHOR)


Wiki = GitStorage
