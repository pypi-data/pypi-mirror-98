from tempfile import TemporaryDirectory
from copy import deepcopy
import logging
import json
import os

from jinja2 import contextfunction
from bs4 import BeautifulSoup

from sphinx.jinja2glue import _tobool, _todim, _toint, accesskey

from flamingo.plugins.menu.menu import Section
from flamingo import Content

from .sphinx_theme import SphinxTheme
from . import defaults

logger = logging.getLogger('flamingo.plugins.SphinxThemes')


class StaticFile:
    def __init__(self, filename):
        self.filename = filename


class Parent:
    def __init__(self, title, link=''):
        self.title = title
        self.link = link


class TocTree:
    def __init__(self, context, content, settings):
        self.context = context
        self.content = content
        self.settings = settings

    def __call__(self, *args, **kwargs):
        template_context = {
            'context': self.context,
            'content': self.content,
            'settings': self.settings,
        }

        return self.context.templating_engine.render(
            'sphinx_themes/toctree.html', template_context)


class SphinxThemes:
    # plugin options ##########################################################
    def reset_options(self):
        self.settings = {}

        ignore_keys = (
            'SPHINX_THEMES_HTML_THEME',
            'SPHINX_THEMES_HTML_THEME_OPTIONS',
        )

        for name in dir(defaults):
            if name.startswith('_') or name in ignore_keys:
                continue

            default = getattr(defaults, name)
            self.settings[name] = getattr(self.context.settings, name, default)

        self.html_theme = getattr(
            self.context.settings,
            'SPHINX_THEMES_HTML_THEME',
            defaults.SPHINX_THEMES_HTML_THEME,
        )

        self.html_theme_options = getattr(
            self.context.settings,
            'SPHINX_THEMES_HTML_THEME_OPTIONS',
            deepcopy(defaults.SPHINX_THEMES_HTML_THEME_OPTIONS),
        )

        self.build()

    def get_options(self):
        options = [
            'Settings',
            ('SPHINX_THEMES_HTML_THEME',
             [(i, i == self.html_theme, )
              for i in sorted(self.sphinx_theme.app.html_themes.keys())]),
            *[(i, self.settings[i], ) for i in sorted(self.settings.keys())],
            'HTML Options',
        ]

        theme_options = {
            **self._raw_theme_options,
            **self.html_theme_options,
        }

        for key in sorted(theme_options.keys()):
            options.append(
                (key, theme_options[key], )
            )

        return options

    def set_option(self, name, value):
        # change theme
        if name == 'SPHINX_THEMES_HTML_THEME':

            # reset theme options if theme name gets changed
            if value != self.html_theme:
                self.html_theme_options = {}

            self.html_theme = value

        # settings
        elif name in self.settings:
            self.settings[name] = value

        # theme option
        else:
            self.html_theme_options[name] = value

        self.build()

    # build helper ############################################################
    def build(self):
        # setup build dir
        if os.path.exists(self.build_dir):
            self.context.rm_rf(self.build_dir, force=True)

        self.context.mkdir_p(self.build_dir, force=True)

        # compile sphinx theme
        self.sphinx_theme = SphinxTheme(
            name=self.html_theme,
            build_dir=self.build_dir,
            options=self.html_theme_options,
        )

        # cache sphinx config and sphinx theme options
        self._theme_config = self.sphinx_theme.config.get_theme_config()

        self._raw_theme_options = \
            self.sphinx_theme.config.get_raw_theme_options()

        self._theme_options = self.sphinx_theme.config.get_theme_options()

    # flamingo hooks: templating ##############################################
    def settings_setup(self, context):
        self.context = context

        # setup menu settings
        if 'flamingo.plugins.Menu' not in context.settings.PLUGINS:
            logger.warn('flamingo.plugins.Menu is not installed')

        elif not context.settings.get('MENU_CREATE_INDICES', False):
            logger.debug('enabling MENU_CREATE_INDICES')

            context.settings.MENU_CREATE_INDICES = True

        # setup build directory
        self.temp_dir = TemporaryDirectory()

        self.build_dir = os.path.join(self.temp_dir.name,
                                      'sphinx-themes/theme')

        context.settings.LIVE_SERVER_IGNORE_PREFIX.append(self.temp_dir.name)

        # configure jinja2 environment
        if 'jinja2.ext.i18n' not in context.settings.JINJA2_EXTENSIONS:
            context.settings.JINJA2_EXTENSIONS.append('jinja2.ext.i18n')

        self.reset_options()

        # register flamingo theme
        self.THEME_PATHS = [
            os.path.join(os.path.dirname(__file__), 'theme'),
            self.build_dir,
        ]

    def templating_engine_setup(self, context, templating_engine):
        def _safe_dump(html):
            if not html:
                return '""'

            soup = BeautifulSoup(str(html), 'html.parser')

            while True:
                script = soup.find('script')

                if not script:
                    break

                script.decompose()

            return json.dumps(str(soup))

        context.settings.EXTRA_CONTEXT['safe_dump'] = _safe_dump

        templating_engine.env.filters['tobool'] = _tobool
        templating_engine.env.filters['toint'] = _toint
        templating_engine.env.filters['todim'] = _todim

        templating_engine.env.globals['accesskey'] = contextfunction(accesskey)

    def template_context_setup(self, context, content, template_name,
                               template_context):

        # generate toctree
        toctree = TocTree(
            context=context,
            content=content,
            settings=self.settings,
        )

        # generate parents
        parents = []

        for item in content.get('menu_path', []):
            if isinstance(item, Section):
                title = item.name
                link = item.content['url']

            elif isinstance(item, Content):
                title = item['title'] or item['content_title']

            parents.append(Parent(title=title, link=link))

        # generate sphinx template context
        settings = {
            key[len('SPHINX_THEMES_'):].lower(): value
            for key, value in self.settings.items()
        }

        for key, value in settings.items():
            if callable(value):
                settings[key] = value(context)

        sphinx_template_context = {
            **settings,

            # variables
            'embedded': False,
            'use_opensearch': False,
            'has_source': False,
            'show_source': '',
            'sourcelink_suffix': '',
            'file_suffix': '',
            'link_suffix': '',
            'style': '',
            'rellinks': [],
            'builder': '',
            'html5_doctype': '',

            # static files
            'css_files': [],
            'script_files': [],

            # template tags
            'hasdoc': self.hasdoc,
            'gettext': self.gettext,
            'pathto': self.pathto,
            'css_tag': self.css_tag,
            'js_tag': self.js_tag,
            'toctree': toctree,

            # content
            'parents': parents,
            'toc': toctree(),
            'pagename': content['title'] or content['content_title'],
            'title': content['title'] or content['content_title'],

            'body': '<h1>{}</h1>\n{}'.format(content['content_title'],
                                             content['content_body']),

            **self._theme_config,
            **self._theme_options,
        }

        # static files
        # css files
        sphinx_template_context['css_files'].append(
            StaticFile(os.path.join('/static',
                                    sphinx_template_context['stylesheet'])))

        if content['sphinx_themes_css_files']:
            if not isinstance(content['sphinx_themes_css_files'], list):
                content['sphinx_themes_css_files'] = [
                    content['sphinx_themes_css_files'],
                ]

            for path in content['sphinx_themes_css_files']:
                sphinx_template_context['css_files'].append(
                    StaticFile(path),
                )

        # script files
        sphinx_template_context['script_files'] += [
            StaticFile('/static/sphinx_themes/jquery.js'),
            StaticFile('/static/sphinx_themes/mark.min.js'),
            StaticFile('/static/sphinx_themes/helper.js'),
            StaticFile('/search_variables.js'),
        ]

        if content['sphinx_themes_script_files']:
            if not isinstance(content['sphinx_themes_script_files'], list):
                content['sphinx_themes_script_files'] = [
                    content['sphinx_themes_script_files'],
                ]

            for path in content['sphinx_themes_script_files']:
                sphinx_template_context['script_files'].append(
                    StaticFile(path),
                )

        sphinx_template_context['script_files'] += [
            StaticFile('/static/sphinx_themes/main.js'),
        ]

        # apply sphinx_template_context to template_context
        for key, value in sphinx_template_context.items():
            template_context[key] = value

    # template tags
    def hasdoc(self, *args, **kwargs):
        if len(args) >= 1 and args[0] == 'search':
            return True

        return False

    def gettext(self, string, **kwargs):
        return string

    def css_tag(self, static_file):
        return '<link rel="stylesheet" href="{}" type="text/css" />'.format(
            static_file.filename)

    def js_tag(self, static_file):
        return '<script src="{}"></script>'.format(static_file.filename)

    def pathto(self, *args, **kwargs):
        if len(args) >= 1 and args[0] == 'search':
            return self.settings['SPHINX_THEMES_SEARCH_URL']

        if isinstance(args[0], StaticFile):
            return args[0].filename

        if isinstance(args[0], str) and args[0].startswith('_static'):
            return '/' + args[0][1:]

        return '/'

    # flamingo hooks: search ##################################################
    def contents_parsed(self, context):
        # search.html
        context.contents.add(
            template=context.settings.DEFAULT_TEMPLATE,
            output=self.settings['SPHINX_THEMES_SEARCH_URL'][1:],
            content_title='Search',
            content_body='',
            sphinx_themes_script_files=[
                '/static/sphinx_themes/ractive.min.js',
                '/static/sphinx_themes/elasticlunr.min.js',
                '/search.js',
            ],
        )

        # search_variables.js
        search_ractive_target_selector = '.body'

        if self.html_theme == 'sphinx_rtd_theme':
            search_ractive_target_selector = '[role=main]'

        context.contents.add(
            template='sphinx_themes/search_variables.js',
            output='search_variables.js',
            search_ractive_target_selector=search_ractive_target_selector,
        )

        # search.js
        context.contents.add(
            template='sphinx_themes/search.js',
            output='search.js',
        )
