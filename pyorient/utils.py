__author__ = 'Ostico <ostico@gmail.com>'

import os
import sys
import logging
import configparser

from pyorient.exceptions import PyOrientConnectionException, PyOrientDatabaseException
from pyorient.otypes import OrientRecordLink
from pyorient.defaults import CFG_PATH, TESTING


def is_debug_active():
    if 'DEBUG' in os.environ:
        if os.environ['DEBUG'].lower() in ( '1', 'true' ):
            return True
    return False


def is_debug_verbose():
    if 'DEBUG_VERBOSE' in os.environ:
        if is_debug_active() and os.environ['DEBUG_VERBOSE'].lower() \
                in ( '1', 'true' ):
            return True
    return False


def dlog( msg ):
    # add check for DEBUG key because KeyError Exception is not caught
    # and if no DEBUG key is set, the driver crash with no reason when
    # connection starts
    if is_debug_active():
        print("[DEBUG]:: %s" % msg)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#
# need connection decorator
def need_connected(wrap):
    def wrap_function(*args, **kwargs):
        if not args[0].is_connected():
            raise PyOrientConnectionException(
                "You must be connected to issue this command", [])
        return wrap(*args, **kwargs)

    return wrap_function


#
# need db opened decorator
def need_db_opened(wrap):
    @need_connected
    def wrap_function(*args, **kwargs):
        if args[0].database_opened() is None:
            raise PyOrientDatabaseException(
                "You must have an opened database to issue this command", [])
        return wrap(*args, **kwargs)

    return wrap_function


def parse_cluster_id(cluster_id):
    try:

        if isinstance(cluster_id, str):
            pass
        elif isinstance(cluster_id, int):
            cluster_id = str(cluster_id)
        elif isinstance( cluster_id, bytes ):
            cluster_id = cluster_id.decode("utf-8")
        elif isinstance( cluster_id, OrientRecordLink ):
            cluster_id = cluster_id.get()
        elif sys.version_info[0] < 3 and isinstance(cluster_id, unicode):
            cluster_id = cluster_id.encode('utf-8')

        _cluster_id, _position = cluster_id.split( ':' )
        if _cluster_id[0] is '#':
            _cluster_id = _cluster_id[1:]
    except (AttributeError, ValueError):
        # String but with no ":"
        # so treat it as one param
        _cluster_id = cluster_id
    return _cluster_id


def parse_cluster_position(_cluster_position):
    try:

        if isinstance(_cluster_position, str):
            pass
        elif isinstance(_cluster_position, int):
            _cluster_position = str(_cluster_position)
        elif isinstance( _cluster_position, bytes ):
            _cluster_position = _cluster_position.decode("utf-8")
        elif isinstance( _cluster_position, OrientRecordLink ):
            _cluster_position = _cluster_position.get()

        _cluster, _position = _cluster_position.split( ':' )
    except (AttributeError, ValueError):
        # String but with no ":"
        # so treat it as one param
        _position = _cluster_position
    return _position


def create_test_section() -> None:
    """Creates the 'TESTING' section of the config file"""

    test_db = input("Test server database [GratefulDeadConcerts]: ") or 'GratefulDeadConcerts'
    test_uroot = input("Test server root user [root]: ") or 'root'
    test_proot = input("Test server password: ")

    while not test_proot:
        input("No password was provided!\nTest server password: ")

    test_server = input("Test server [localhost]: ") or 'localhost'
    test_port = int(input("Test server port [2424]: ") or '2424')

    write_to_config(TESTING, 'database', test_db)
    write_to_config(TESTING, 'user', test_uroot)
    write_to_config(TESTING, 'password', test_proot)
    write_to_config(TESTING, 'server', test_server)
    write_to_config(TESTING, 'port', test_port)


def write_to_config(section: str, option: str, value: str) -> None:
    """Write section, option and value to config file.

    Parameters
    ----------
    section : str
        Section name of configuration file.
    option : str
        Option name.
    value : str
        Option value.

    """
    cfp = CFG_PATH
    config = configparser.RawConfigParser()

    if not os.path.exists(cfp):
        with open(cfp, 'w') as config_file:
            config[section] = {option: value}
            config.write(config_file)
            logging.info('set in configuration file {} in section {} {}={}'.format(cfp, section, option, value))
    else:
        config.read(cfp)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)
        with open(cfp, 'w') as configfile:
            config.write(configfile)


if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def to_unicode(x):
        return str(x).decode('utf-8')

    def to_str(x):
        return unicode(x).encode('utf-8')
else:
    def u(x):
        return x

    def to_str(x):
        return str(x)

    def to_unicode(x):
        return str(x)
