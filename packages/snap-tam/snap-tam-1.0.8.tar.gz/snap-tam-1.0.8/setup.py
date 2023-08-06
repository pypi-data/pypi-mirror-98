"""Setup for Pypi"""
import os
from setuptools import setup, find_packages


version = '1.0.8'
packages = find_packages(exclude=['test'])


def get_pkg_data(pkg_name, data_dirs, extensions):
    """Recusrively get package data.

    This should be called from within setup.py's setuptools.setup() function,
    e.g. package_data={'my_package': get_pkg_data(pkg_name='my_pckage', ...)}

    Args:
        pkg_name (str): Name of package containing package data.
        data_dirs (list):
        extensions (list):

    Returns:
        list: List of glob strings where each string represents a terminal
        branch node (i.e. folder) and a glob of all files ending in designated
        extension(s).

    Examples:
        Args: get_pkg_data(pkg_name='my_package',
        src_dirs=['templates'], extensions=['html'])

        Returns: [
        'templates/*.html',
        'templates/content/*.html',
        'templates/content/prompt/*.html',
        'templates/content/prompt/inputs/*.html']
    """
    pkg_root = \
        os.path.dirname(os.path.realpath(__file__)) + '/{}/'.format(pkg_name)
    pkg_data = []
    for _dir in data_dirs:
        for ext in extensions:
            for i, j, y in os.walk(pkg_root + _dir):
                pkg_data.append(i + '/*.' + ext)
    return pkg_data


setup(
    name='snap-tam',
    version=version,
    author='Joe Flack',
    author_email='jflack@jhu.edu',
    url='http://www.modeltb.org',
    packages=packages,
    package_dir={
        'snap-tam': 'snap_tam'
    },
    package_data={
        'snap_tam': [
            'config.json'
        ]
    },
    entry_points={
        'console_scripts': [
            'snap-tam=snap_tam.cli:cli'
        ],
    },
    # license='LICENSE.txt',
    license='',
    description='Utility for ModelTB.org team. Aggregates SNaP reports to a '
                'single file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openpyxl>=3.0.5',
        'pandas>=1.1.5'
    ]
)
