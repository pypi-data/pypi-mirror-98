
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'mv_regex',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Move files by applying an regular expression',
    long_description = 'Move files by applying an regular expression',
    keywords = 'regex',
    url = 'https://github.com/tdegeus/mv_regex',
    packages = find_packages(),
    use_scm_version = {'write_to': 'mv_regex/_version.py'},
    setup_requires = ['setuptools_scm'],
    install_requires = ['click'],
    entry_points = {
        'console_scripts': ['mv_regex = mv_regex.cli.mv:main']})
