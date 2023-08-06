
import os
import re
import click
import difflib

from ._version import *

def diff_theme(theme=None):
    r'''
Return dictionary of colors.

.. code-block:: python

    {
        'equal' : '...',
        'insert' : '...',
        'delete': '...',
        'replace' : '...',
    }

:param str theme: Select color-theme.

:rtype: dict
    '''

    if theme == 'dark':
        return \
        {
            'equal' : '',
            'insert' : '1;32',
            'delete': '1;31',
            'replace' : '1;37',
        }

    return \
    {
        'equal' : '',
        'insert' : '',
        'delete': '',
        'replace' : '',
    }


def theme(theme=None):
    r'''
Return dictionary of colors.

.. code-block:: python

    {
        'new' : '...',
        'overwrite' : '...',
        'skip' : '...',
        'bright' : '...',
    }

:param str theme: Select color-theme.

:rtype: dict
    '''

    if theme == 'dark':
        return \
        {
            'new' : '1;32',
            'overwrite': '1;31',
            'skip' : '1;30',
            'bright' : '1;37',
        }

    return \
    {
        'new' : '',
        'overwrite': '',
        'skip' : '',
        'bright' : '',
    }


class String:
    r'''
Rich string.

.. note::

    All options are attributes, that can be modified at all times.

.. note::

    Available methods:

    *   ``A.format()`` :  Formatted string.
    *   ``str(A)`` : Unformatted string.
    *   ``A.isnumeric()`` : Return if the "data" is numeric.
    *   ``int(A)`` : Dummy integer.
    *   ``float(A)`` : Dummy float.

:type data: str, None
:param data: The data.

:type width: None, int
:param width: Print width (formatted print only).

:type color: None, str
:param color: Print color, e.g. "1;32" for bold green (formatted print only).

:type align: ``'<'``, ``'>'``
:param align: Print alignment (formatted print only).

:type dummy: 0, int, float
:param dummy: Dummy numerical value.

:methods:


    '''

    def __init__(self, data, width=None, align='<', color=None, dummy=0):

        self.data  = data
        self.width = width
        self.color = color
        self.align = align
        self.dummy = dummy

    def format(self):
        r'''
Return formatted string: align/width/color are applied.
        '''

        if self.width and self.color:
            fmt = '\x1b[{color:s}m{{0:{align:s}{width:d}.{width:d}s}}\x1b[0m'.format(**self.__dict__)
        elif self.width:
            fmt = '{{0:{align:s}{width:d}.{width:d}s}}'.format(**self.__dict__)
        elif self.color:
            fmt = '\x1b[{color:s}m{{0:{align:s}s}}\x1b[0m'.format(**self.__dict__)
        else:
            fmt = '{{0:{align:s}s}}'.format(**self.__dict__)

        return fmt.format(str(self))

    def isnumeric(self):
        r'''
Return if the "data" is numeric : always zero for this class.
        '''
        return False

    def __str__(self):
        return str(self.data)

    def __int__(self):
        return int(self.dummy)

    def __float__(self):
        return float(self.dummy)

    def __repr__(self):
        return str(self)

    def __lt__(self,other):
        return str(self) < str(other)


def show_diff(text, new_text, theme_name):
    r'''
Highlighted string with difference between two string.
See http://stackoverflow.com/a/788780

:param str text: A string.
:param str new_text: The new string.
:param str theme_name: The name of the color-theme. See :py:mod:`mv_regex.diff_theme`.
:return: ``(text, new_text)`` The highlighted string.
    '''

    color = diff_theme('dark')
    seqm = difflib.SequenceMatcher(None, text, new_text)
    ret = []
    n_ret = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        ret.append(String(seqm.a[a0:a1], color=color[opcode]).format())
        n_ret.append(String(seqm.b[b0:b1], color=color[opcode]).format())

    return ''.join(ret), ''.join(n_ret)


def mv(search, replace, files, force=False, quiet=False, theme_name='none'):
    r'''
Rename files using a regular expression.

:param str search: Regular expression to search.
:param str replace: Regular expression to use as replace.
:param list files: List of files on which to do the replacement.
:param bool force: If ``True`` apply without prompt. If ``None`` preform only dry run.
:param bool quiet: If ``True`` the operation summary is suppressed.
:param str theme_name: The name of the color-theme. See :py:mod:`mv_regex.theme`.
:return: ``files`` after applying renaming.
    '''

    if type(files) == str:
        files = [files]

    color = theme(theme_name.lower())

    for file in files:
        if not os.path.isfile(file) and not os.path.isdir(file):
            raise IOError('Input {0:s} does not exist'.format(file))

    # only keep input files that match the input regular-expression
    files = [file for file in files if re.match(search, file)]

    # rename the remaining files
    ret = [re.sub(search, replace, file) for file in files]

    # only keep files that will be renamed
    idx = [i for i, (old, new) in enumerate(zip(files, ret)) if old != new]
    files = [files[i] for i in idx]
    renamed = [ret[i] for i in idx]

    # no files remaining -> quit
    if len(renamed) == 0:
        return ret

    # prompt the user for confirmation
    if force != True:

        if not quiet:

            l = max([len(file) for file in files])

            for file, new in zip(files, renamed):

                f, n = show_diff(file, new, theme_name.lower())

                if not os.path.isfile(new):
                    print('{0:s}{1:s} {2:s} {3:s}'.format(
                        f,
                        ' ' * (l - len(file)),
                        String('->', color=color['new']).format(),
                        n
                    ))
                else:
                    print('{0:s}{1:s} {2:s} {3:s}'.format(
                        f,
                        ' ' * (l - len(file)),
                        String('=>', color=color['overwrite']).format(),
                        n
                    ))

        if force is None:
            return ret

        if not click.confirm('Proceed?'):
            raise IOError('Aborted')

    # proceed with the renaming of all files
    for file, new in zip(files, renamed):
        os.rename(file, new)

    return ret
