#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command Line Interface."""
import os

from argparse import ArgumentParser
from copy import copy
from sys import stderr

from snap_tam.aggregate_filesystem import run


config_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'config.json')

intro = f"""
*======== SNaP TAM Aggregator ========*
| Aggregate SNaP reports on OneDrive.
| - Config file location: {config_path} 
*=====================================*
"""

err_msg = 'An error occurred while trying to read or write to the OneDrive ' \
          'folder or one of its subfolders. Please manually edit the config' \
          'file and ensure that the specified paths and folder names are ' \
          'correct.\n\n' \
          'Original system error message: '


def _required_fields(parser):
    """Add required fields to parser.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    return parser


def _optional_fields(parser):
    """Add optional fields.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    parser.add_argument(
        '-p', '--onedrive-path', help='Path to OneDrive installation.')

    return parser


def _add_arguments(parser):
    """Add arguments to parser.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    parser2 = _optional_fields(parser)
    parser3 = _required_fields(parser2)

    return parser3


def cli():
    """Command line interface for package.

    Side Effects: Executes program.
    """
    argeparser = ArgumentParser(description=intro)
    parser = _add_arguments(copy(argeparser))
    args = parser.parse_args()

    try:
        print(intro)
        run(onedrive_dir_path=args.onedrive_path)
    except FileNotFoundError as err:
        print(err_msg, file=stderr)
        print(err, file=stderr)


if __name__ == '__main__':
    cli()
