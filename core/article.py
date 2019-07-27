import datetime
import os
import re
from config import config


class Article(object):
    _RE_FILENAME_METADATA = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2})\. (?P<title>.*)')

    def __init__(self, **kwargs):
        self.title = 'default'
        self.date = datetime.date.today()
        self.gallery = 'default'
        self.status = 'draft'
        self.storage = 1
        self.permalink = 1
        self.category = 'default'
        self.summary = ''
        self.content = ''
        for key, value in kwargs:
            setattr(self, key, value)

    def read(self, path=None):
        path = path if path else self.path
        path = os.path.realpath(path)
        directory, filename = os.path.split(path)
        base_name, extension_name = os.path.splitext(filename)
        date, title = self._RE_FILENAME_METADATA.match(base_name).groups()
        date = datetime.date(*map(int, date.split('-')))

        self.title = title
        self.date = date
        self.category = os.path.split(directory)[1]

        with open(self.path, mode='r', encoding='utf-8') as file:
            meta, content = file.read().split('\n\n', maxsplit=1)
            meta = [line.split(': ') for line in meta.split('\n')]
            meta = {key.lower(): value for key, value in meta}
            assert set(meta.keys()) == {'summary', 'gallery', 'permalink', 'status', 'storage'}

        self.content = content
        self.gallery = meta['gallery']
        self.permalink = int(meta['permalink'])
        self.status = meta['status']
        self.storage = int(meta['storage'])
        self.summary = meta['summary']

    def save(self):
        if os.path.exists(self.path):
            raise FileExistsError('文件已存在，无法覆盖')
        meta = (
            ('Gallery', self.gallery),
            ('Permalink', str(self.permalink)),
            ('Status', self.status),
            ('Storage', str(self.storage)),
            ('Summary', self.summary),
        )
        meta = ['{}: {}'.format(key, value) for key, value in meta]
        meta_string = '\n'.join(meta)
        content = '{}\n\n{}'.format(meta_string, self.content)
        with open(self.path, mode='w', encoding='utf-8') as file:
            file.write(content)

    @property
    def file_name(self):
        date_string = self.date.strftime('%Y-%m-%d')
        return '{}. {}.md'.format(date_string, self.title)

    @property
    def path(self):
        return os.path.join(config.blog, self.category, self.file_name)
