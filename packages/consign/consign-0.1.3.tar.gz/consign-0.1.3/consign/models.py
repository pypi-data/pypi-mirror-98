import os
import sys
import json
import errno
import tempfile

from os.path import isfile

from .exceptions import (
    InvalidDataType, InvalidPath, ConsignWarning)

# Sadly, Python fails to provide the following magic number for us.
# Windows-specific error code indicating an invalid pathname.
ERROR_INVALID_NAME = 123


class Consignment():
    '''A user-created :class:`Consignment <Consignment>` object.
    Used to prepare a :class:`PreparedConsignment <PreparedConsignment>`, which is sent to the server.
    '''

    def __init__(self,
        method=None, data=None, url=None, delimiter=None, overwrite=True):

        # Default empty dicts for optional dict params.
        default_delimiter = ',' if method == 'CSV' else None
        delimiter = default_delimiter if delimiter is None else delimiter

        self.method = method
        self.data = data
        self.url = url
        self.delimiter = delimiter
        self.overwrite = overwrite


class PreparedConsignment():
    '''The fully mutable :class:`PreparedConsign <PreparedConsign>` object,
    containing the exact bytes that will be sent to the server.
    Instances are generated from a :class:`Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.
    '''

    def __init__(self):
        pass


    def prepare(self,
        method=None, data=None, url=None, delimiter=None, overwrite=None):
        '''Prepares the entire consignment with the given parameters.'''

        self.prepare_method(method)
        self.prepare_data(data, delimiter)
        self.prepare_url(url)
        self.prepare_file(url, overwrite)

        # Note that prepare_auth must be last to enable authentication schemes
        # such as OAuth to work on a fully prepared request.


    def prepare_method(self, method):
        '''Prepares the given Consignment method.'''
        self.method = method.upper()


    def prepare_data(self, data, delimiter):

        self.delimiter = delimiter

        if self.method == 'CSV':
            self.prepare_csv(data, delimiter)
        
        elif self.method == 'JSON':
            self.prepare_json(data)


    def prepare_json(self, data):
        '''Verifies data is valid JSON.
        '''
        if not isinstance(data, (list, dict)) or not self.is_json_safe(data):
            raise InvalidDataType('Data is not a valid JSON object.')
        self.data = data


    def is_json_safe(self, data): 
        if data is None:
            return True 
        elif isinstance(data, (bool, int, float, str)): 
            return True 
        elif isinstance(data, (tuple, list)): 
            return all(self.is_json_safe(x) for x in data) 
        elif isinstance(data, dict):
            return all(isinstance(k, str) and self.is_json_safe(v) for k, v in data.items())
        return False 


    def prepare_csv(self, data, delimiter):
        '''
        Verifies data is tabular and free of delimiter characters.
        '''
        is_tabular = isinstance(data, list)
        if not is_tabular:
            raise InvalidDataType('Data is not tabular.')

        is_free = not(any(delimiter in column for row in data for column in row))
        if not is_free:
            raise ConsignWarning('Delimiter %s is used in data' % (delimiter))

        self.data = data
        self.delimiter = delimiter


    def prepare_url(self, url):
        '''
        Verifies path existance, user permissions to write, and file extension
        matches the data format.
        '''
        if self.method in ['CSV', 'JSON', 'PDF', 'HTML', 'TXT']:
            self.prepare_pathname(url)
            self.url = url


    def is_pathname_valid(self, pathname: str) -> bool:
        '''
        `True` if the passed pathname is a valid pathname for the current OS;
        `False` otherwise.
        '''
        # If this pathname is either not a string or is but is empty, this pathname
        # is invalid.
        try:
            if not isinstance(pathname, str) or not pathname:
                return False

            # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
            # if any. Since Windows prohibits path components from containing `:`
            # characters, failing to strip this `:`-suffixed prefix would
            # erroneously invalidate all valid absolute Windows pathnames.
            _, pathname = os.path.splitdrive(pathname)

            # Directory guaranteed to exist. If the current OS is Windows, this is
            # the drive to which Windows was installed (e.g., the '%HOMEDRIVE%'
            # environment variable); else, the typical root directory.
            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

            # Append a path separator to this directory if needed.
            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

            # Test whether each path component split from this pathname is valid or
            # not, ignoring non-existent and non-readable path components.
            for pathname_part in pathname.split(os.path.sep):
                try:
                    os.lstat(root_dirname + pathname_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this pathname is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid pathnames:
                #
                # * Instances of the Windows-specific 'WindowsError' class
                #   defining the 'winerror' attribute whose value is
                #   'ERROR_INVALID_NAME'. Under Windows, 'winerror' is more
                #   fine-grained and hence useful than the generic 'errno'
                #   attribute. When a too-long pathname is passed, for example,
                #   'errno' is 'ENOENT' (i.e., no such file or directory) rather
                #   than 'ENAMETOOLONG' (i.e., file name too long).
                # * Instances of the cross-platform 'OSError' class defining the
                #   generic 'errno' attribute whose value is either:
                #   * Under most POSIX-compatible OSes, 'ENAMETOOLONG'.
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), 'ERANGE'.
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == ERROR_INVALID_NAME:
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        # If a 'TypeError' exception was raised, it almost certainly has the
        # error message 'embedded NUL character' indicating an invalid pathname.
        except TypeError as exc:
            return False
        # If no exception was raised, all path components and hence this
        # pathname itself are valid. (Praise be to the curmudgeonly python.)
        else:
            return True
        # If any other exception was raised, this is an unrelated fatal issue
        # (e.g., a bug). Permit this exception to unwind the call stack.
        #
        # Did we mention this should be shipped with Python already?


    def is_path_creatable(self, pathname: str) -> bool:
        '''
        `True` if the current user has sufficient permissions to create the passed
        pathname; `False` otherwise.
        '''
        # Parent directory of the passed path. If empty, we substitute the current
        # working directory (CWD) instead.
        dirname = os.path.dirname(pathname) or os.getcwd()
        return os.access(dirname, os.W_OK)


    def is_path_extension_adecuate(self, pathname):
        '''
        '''
        given_method = self.method.lower()
        given_extension = pathname.split('.')[-1]
        if not given_extension == given_method:
            raise InvalidPath('Wrong file extension. Should be '%s' instead of '%s'' % (given_method, given_extension))
        return True


    def prepare_pathname(self, pathname: str) -> bool:
        '''
        Source: https://stackoverflow.com/a/34102855
        'True' if the passed pathname is a valid pathname for the current OS _and_
        either currently exists or is hypothetically creatable; 'False' otherwise.

        This function is guaranteed to _never_ raise exceptions.
        '''
        try:
            # To prevent 'os' module calls from raising undesirable exceptions on
            # invalid pathnames, is_pathname_valid() is explicitly called first.
            if self.method == 'IMG':
                return self.is_pathname_valid(pathname) and (
                    os.path.exists(pathname) or self.is_path_creatable(pathname)
                    )
            else:
                return self.is_pathname_valid(pathname) and (
                    os.path.exists(pathname) or self.is_path_creatable(pathname)
                    ) and self.is_path_extension_adecuate(pathname)
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be inaccessible. All
        # other exceptions are unrelated fatal issues and should not be caught here.
        except OSError:
            return False


    def prepare_file(self, url, overwrite):
        '''
        If file is to be updated, it needs to exist.
        '''
        self.overwrite = True if not overwrite else overwrite
        if not self.overwrite and self.method in ['CSV', 'JSON']:
            if not isfile(url):
                raise InvalidPath('File to be updated does NOT exist.')
