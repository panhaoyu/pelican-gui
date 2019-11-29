import os
import typing
import asyncio
import itertools
import functools
import pelican
import pelican.settings
import settings


class Pelican(object):
    def __init__(self, path=settings.PATH):
        self.config_path = path
        self.articles_generator: typing.Union[pelican.ArticlesGenerator, None] = None
        self.pages_generator = None
        self.static_generator = None
        self.settings = pelican.settings.read_settings(path=self.config_path)
        self.pelican = pelican.Pelican(self.settings)
        self.generators = self.get_generators()

    def get_generators(self, local=False):
        context: dict = self.settings.copy()
        if local:
            context.update({
                'SITEURL': 'http://localhost/blog/',
            })
        context['generated_content'] = {}
        context['static_links'] = set()
        context['static_content'] = {}
        context['localsiteurl'] = self.settings['SITEURL']
        generators = [
            cls(
                context=context,
                settings=self.settings,
                path=self.pelican.path,
                theme=self.pelican.theme,
                output_path=self.pelican.output_path,
            ) for cls in self.pelican.get_generator_classes()
        ]
        for generator in generators:
            if isinstance(generator, pelican.generators.ArticlesGenerator):
                self.articles_generator = generator
            elif isinstance(generator, pelican.generators.StaticGenerator):
                self.static_generator = generator
            elif isinstance(generator, pelican.generators.PagesGenerator):
                self.pages_generator = generator
        return generators

    def read(self, local=False):
        """
        读取文件夹中的所有博客
        :param local:
        :return:
        """
        self.generators = self.get_generators(local)
        for p in self.generators:
            if hasattr(p, 'generate_context'):
                p.generate_context()
        for p in self.generators:
            if hasattr(p, 'refresh_metadata_intersite_links'):
                p.refresh_metadata_intersite_links()

    def serve(self, host='0.0.0.0', port=80):
        """
        启动本地服务器
        :param host: IP，设置为0.0.0.0可以允许局域网的访问
        :param port: 端口，默认为80
        :return:
        """
        pelican.listen(host, port, self.pelican.output_path)

    def write(self):
        """
        将读取到的内容写入到输出文件夹
        :return:
        """
        pelican.clean_output_dir(self.pelican.output_path, self.pelican.output_retention)
        for generator in self.generators:
            if hasattr(generator, 'refresh_metadata_intersite_links'):
                generator.refresh_metadata_intersite_links()
        writer = self.pelican.get_writer()
        for generator in self.generators:
            if hasattr(generator, 'generate_output'):
                generator.generate_output(writer)

    def deploy(self):
        os.popen(f'git -C {self.pelican.output_path} push -f --set-upstream origin master')

    @property
    def articles(self):
        articles = list()
        articles.extend(self.articles_generator.articles)
        articles.extend(self.articles_generator.drafts)
        return articles
