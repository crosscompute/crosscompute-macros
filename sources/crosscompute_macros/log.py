import re
from logging import (
    basicConfig,
    getLogger,
    DEBUG,
    INFO)
from os.path import expanduser
from time import perf_counter


class Timer:
    # https://stackoverflow.com/a/69156219/192092

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.time = perf_counter() - self.start


def configure_argument_parser_for_logging(argument_parser):
    argument_parser.add_argument(
        '--debug', dest='with_debug', action='store_true', default=False,
        help='show debugging messages')


def configure_logging_from(args, logging_level_by_package_name):
    with_debug = args.with_debug
    configure_logging(with_debug)
    configure_logging_level_by_package_name(logging_level_by_package_name)


def configure_logging(with_debug, timestamp='%Y%m%d-%H%M%S'):
    if with_debug:
        logging_level = DEBUG
        logging_prefix = '%(name)s:%(pathname)s:%(lineno)s '
    else:
        logging_level = INFO
        logging_prefix = '%(name)s:%(lineno)s '
    basicConfig(
        format=f'%(asctime)s %(levelname)s {logging_prefix} %(message)s',
        datefmt=timestamp,
        level=logging_level)


def configure_logging_level_by_package_name(logging_level_by_package_name):
    for package_name, logging_level in logging_level_by_package_name.items():
        getLogger(package_name).setLevel(logging_level)


def redact_path(x):
    return re.sub(r'^' + re.escape(expanduser('~')), '~', str(x))  # noqa: PTH111
