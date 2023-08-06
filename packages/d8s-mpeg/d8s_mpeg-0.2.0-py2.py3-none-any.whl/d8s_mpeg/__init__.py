try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

from .mpeg import *

try:
    __version__ = version('d8s_mpeg')
except PackageNotFoundError:
    message = (
        'Unable to find a version number for "d8s_mpeg". '
        + 'This likely means the library was not installed properly. '
        + 'Please re-install it and, if the problem persists, '
        + 'raise an issue here: https://github.com/democritus-project/democritus-mpeg/issues.'
    )
    print(message)

__author__ = '''Floyd Hightower'''
__email__ = 'floyd.hightower27@gmail.com'
