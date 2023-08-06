from .bootstrap.plugins import Bootstrap3, Bootstrap4  # NOQA
from .jquery.plugins import jQuery1, jQuery2, jQuery3  # NOQA
from .photoswipe.plugin import PhotoSwipe  # NOQA
from .rst.bootstrap3 import rstBootstrap3  # NOQA
from .rst.plugin import reStructuredText  # NOQA
from .authors.authors import Authors  # NOQA
from .rst.include import rstInclude  # NOQA
from .rtd.plugin import ReadTheDocs  # NOQA
from .redirects import Redirects  # NOQA
from .rst.image import rstImage  # NOQA
from .rst.link import rstLink  # NOQA
from .tags.tags import Tags  # NOQA
from .menu.menu import Menu  # NOQA
from .html import HTML  # NOQA
from .i18n import I18N  # NOQA
from .time import Time  # NOQA
from .yaml import Yaml  # NOQA
from .git import Git  # NOQA

try:
    from .rst.pygments import rstPygments  # NOQA

except ImportError:  # pragma: no cover
    pass


try:
    from .feeds import Feeds  # NOQA

except ImportError:  # pragma: no cover
    pass


try:
    from .md import Markdown  # NOQA

except ImportError:  # pragma: no cover
    pass


try:
    from .thumbnails import Thumbnails  # NOQA

except ImportError:  # pragma: no cover
    pass


try:
    from .sphinx_themes.plugin import SphinxThemes  # NOQA

except ImportError:  # pragma: no cover
    pass
