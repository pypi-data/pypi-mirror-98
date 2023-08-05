"""Demo Module

A demo module example.

"""
from .__version__ import __title__
from .__version__ import __description__
from .__version__ import __url__
from .__version__ import __version__
from .__version__ import __author__
from .__version__ import __author_email__
from .__version__ import __license__


def read_module_meta() -> dict:
    """A simple function for test coverage coveralls.io integration."""

    # print(f'__title__ {__title__}')
    # print(f'__description__ {__description__}')
    # print(f'__url__ {__url__}')
    # print(f'__version__ {__version__}')
    # print(f'__author_email__ {__author_email__}')
    # print(f'__author__ {__author__}')
    # print(f'__license__ {__license__}')
    return {
        '__title__': __title__,
        '__description__': __description__,
        '__url__': __url__,
        '__version__': __version__,
        '__author_email__': __author_email__,
        '__author__': __author__,
        '__license__': __license__,
    }
