import pelican
import pelican.settings
import settings


class Reader(object):
    def __init__(self, path=settings.PATH):
        self.config_path = path
        self.articles_generator = None
        self.pages_generator = None
        self.static_generator = None
        self.settings = pelican.settings.read_settings(path=self.config_path)
        self.pelican = pelican.Pelican(self.settings)
        self.generators = self.get_generators()

    def get_generators(self, local=False):
        context: dict = self.settings.copy()
        if local:
            context.update({
                'SITEURL': 'http://localhost'
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
        self.generators = self.get_generators(local)
        for p in self.generators:
            if hasattr(p, 'generate_context'):
                p.generate_context()
        for p in self.generators:
            if hasattr(p, 'refresh_metadata_intersite_links'):
                p.refresh_metadata_intersite_links()

    def serve(self, host='0.0.0.0', port=80):
        pelican.listen(host, port, self.pelican.output_path)

    def write(self):
        pelican.clean_output_dir(self.pelican.output_path, self.pelican.output_retention)
        for generator in self.generators:
            if hasattr(generator, 'refresh_metadata_intersite_links'):
                generator.refresh_metadata_intersite_links()
        writer = self.pelican.get_writer()
        for generator in self.generators:
            if hasattr(generator, 'generate_output'):
                generator.generate_output(writer)
