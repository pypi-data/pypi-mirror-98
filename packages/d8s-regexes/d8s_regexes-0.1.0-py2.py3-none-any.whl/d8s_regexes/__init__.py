try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

from .regexes import *

try:
    __version__ = version('democritus_regexes')
except PackageNotFoundError:
    message = (
        'Unable to find a version number for "democritus_regexes". '
        + 'This likely means the library was not installed properly. '
        + 'Please re-install it and, if the problem persists, '
        + 'raise an issue here: https://github.com/democritus-project/democritus-regexes/issues.'
    )
    print(message)

__author__ = '''Floyd Hightower'''
__email__ = 'floyd.hightower27@gmail.com'
