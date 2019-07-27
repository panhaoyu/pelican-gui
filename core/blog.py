import os
from config import config
from .article import Article


class Blog(object):
    def __init__(self):
        self._blog_path = config.blog
        self.articles = list()
        self.read()

    def read(self):
        self.articles = list()
        for directory, sub_directories, file_names in os.walk(self._blog_path):
            # 跳过.git目录
            if '.git' in directory:
                continue
            for file_name in file_names:
                path = os.path.join(directory, file_name)
                article = Article()
                article.read(path)
                self.articles.append(article)

    @property
    def max_permalink(self):
        permalink_list = [article.permalink for article in self.articles]
        return max(permalink_list)

    @property
    def categories(self):
        categories = [article.category for article in self.articles]
        categories = set(categories)
        categories = list(categories)
        categories = sorted(categories)
        return categories
