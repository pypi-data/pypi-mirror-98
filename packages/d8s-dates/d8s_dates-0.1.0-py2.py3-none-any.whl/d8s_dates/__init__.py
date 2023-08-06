try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

from .dates_and_times import *

try:
    __version__ = version('democritus_dates')
except PackageNotFoundError:
    message = (
        'Unable to find a version number for "democritus_dates". '
        + 'This likely means the library was not installed properly. '
        + 'Please re-install it and, if the problem persists, '
        + 'raise an issue here: https://github.com/democritus-project/democritus-dates/issues.'
    )
    print(message)

__author__ = '''Floyd Hightower'''
__email__ = 'floyd.hightower27@gmail.com'
