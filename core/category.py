import os
import glob
from .article import Article as _Article


class Category(object):
    def __init__(self):
        self._path = None
        self._articles = list()

    @property
    def path(self):
        assert self.path
        return self.path

    @path.setter
    def path(self, value):
        self._path = value
        self._articles = list()
        path = os.path.join(self.path, '*.md')
        files = glob.glob(path)
        for file in files:
            article = _Article()
            article.path = file
            self._articles.append(article)

    @property
    def articles(self):
        return self._articles

    def append(self, article):
        assert isinstance(article, _Article)
        self._articles.append(article)
