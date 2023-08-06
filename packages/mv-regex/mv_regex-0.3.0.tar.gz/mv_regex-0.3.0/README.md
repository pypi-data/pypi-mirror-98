
[![CI](https://github.com/tdegeus/mv_regex/workflows/CI/badge.svg)](https://github.com/tdegeus/mv_regex/actions)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/mv_regex.svg)](https://anaconda.org/conda-forge/mv_regex)

# mv_regex

Move files by applying an regular expression. This allows one to partly rename a batch of files.

# Contents

<!-- MarkdownTOC -->

- [Disclaimer](#disclaimer)
- [Getting mv_regex](#getting-mv_regex)
  - [Using conda](#using-conda)
  - [Using PyPi](#using-pypi)
  - [From source](#from-source)
- [Usage](#usage)

<!-- /MarkdownTOC -->

# Disclaimer

This library is free to use under the [MIT license](https://github.com/tdegeus/mv_regex/blob/master/LICENSE). Any additions are very much appreciated, in terms of suggested functionality, code, documentation, testimonials, word-of-mouth advertisement, etc. Bug reports or feature requests can be filed on [GitHub](https://github.com/tdegeus/mv_regex). As always, the code comes with no guarantee. None of the developers can be held responsible for possible mistakes.

Download: [.zip file](https://github.com/tdegeus/mv_regex/zipball/master) | [.tar.gz file](https://github.com/tdegeus/mv_regex/tarball/master).

(c - [MIT](https://github.com/tdegeus/mv_regex/blob/master/LICENSE)) T.W.J. de Geus (Tom) | tom@geus.me | www.geus.me | [github.com/tdegeus/mv_regex](https://github.com/tdegeus/mv_regex)


# Getting mv_regex

## Using conda

```bash
conda install -c conda-forge mv_regex
```

## Using PyPi

```bash
pip install mv_regex
```

## From source

```bash
# Download mv_regex
git checkout https://github.com/tdegeus/mv_regex.git
cd mv_regex

# Install
python -m pip install .
```

# Usage

The usage is as follows (see `mv_regex --help`):

```
mv_regex
  Rename files using regular expressions. The program will prompt the user for
  confirmation before renaming (unless the "--force" options is used).

Usage:
  mv_regex [options] <search> <replace> <files>...

Arguments:
  <search>        Regular expression to search.
  <replace>       Regular expression to use as replace.
  <files>         List of files on which to do the replacement.

Options:
  -f, --force     Force move, don\'t prompt for user interaction.
  -d, --dirname   Rename directory name (not the file-name).
  -h, --help      Show help.
      --version   Show version.


Example:
  mv_regex "(.*)(_raw.svg)" "\1.svg" *.svg
```
