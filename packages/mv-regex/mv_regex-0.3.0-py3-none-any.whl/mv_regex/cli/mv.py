r"""Rename files using regular expressions.

The program will prompt the user for confirmation before renaming
(unless the "--force" options is used).

:usage:

    mv_regex [options] <search> <replace> <files>...

:arguments:

    <search>
        Regular expression to search.

    <replace>
        Regular expression to use as replace.

    <files>
        List of files on which to do the replacement.

:options:

    -f, --force
        Force move, don't prompt for user interaction.

    -n, --dry-run
        Perform a trial run with no changes made.

    --colors=arg
        Select color scheme from: none, dark. [default: dark]

    -h, --help
        Show help.

    --version
        Show version.

:example:

    mv_regex "(.*)(_raw.svg)" "\1.svg" *.svg

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/mv_regex
"""

import argparse
from .. import version
from .. import mv

def main():

    try:

        class Parser(argparse.ArgumentParser):
            def print_help(self):
                print(__doc__)

        parser = Parser()
        parser.add_argument('-f', '--force', required=False, action='store_true')
        parser.add_argument('-n', '--dry-run', required=False, action='store_true')
        parser.add_argument(      '--colors', required=False, default='dark')
        parser.add_argument('-v', '--version', action='version', version=version)
        parser.add_argument('search')
        parser.add_argument('replace')
        parser.add_argument('files', nargs='+')
        args = parser.parse_args()

        mv(
            args.search,
            args.replace,
            args.files,
            force = None if args.dry_run else args.force,
            theme_name = args.colors)

    except Exception as e:

        print(e)
        return 1


if __name__ == '__main__':

    main()
