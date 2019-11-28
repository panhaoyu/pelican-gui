import os
import collections

import pelican.contents

PATH = [
    os.path.join(r'D:\OneDrive\长期文档\blog\code\pelicanconf.py'),
    os.path.join(r'C:\Users\wolf\OneDrive\长期文档\blog\code\pelicanconf.py')
]
PATH = [path for path in PATH if os.path.exists(path)][0]

EDITOR_PATH = r'C:\Program Files\Notepad++\notepad++.exe'


def get_fields(article: pelican.contents.Article):
    storage = article.metadata['storage']
    gallery = article.metadata['gallery'] if article.metadata['gallery'] else 'default'
    data = (
        ('编号', article.metadata['permalink']),
        ('分类', str(article.metadata['category'])),
        ('标题', article.title),
        ('日期', article.date.strftime('%y-%m-%d')),
        ('图片库', f'{storage}:{gallery}'),
        ('发布状态', article.status),
        # ('URL', article.url),
        # ('字数', len(article.content)),
    )
    return data
