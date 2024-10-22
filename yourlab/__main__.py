#! /usr/bin/env python3

"""
YourLab

YourLab simplifies the creation, backup, and management of Python projects,
while offering various tools to automate common developer tasks.

~~~~~~~~~~~~~~~~~~~~~
Source: https://github.com/KDUser12/YourLab
(c) 2024 KDUser12
Released under the Apache License 2.0
"""

import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from __init__ import __shortname__, __longname__, __version__
from utils._os import check_os_compatibility
from utils.env import check_python_version
from utils.packages import check_and_install_dependencies


def setup_logging(debug=False):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs.log', mode='a')
        ]
    )


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description=f"{__longname__} (Version {__version__})")
    parser.add_argument("-v", "--version", action="version", version=f"{__shortname__} v{__version__}", help="display version information and dependencies")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="display extra debugging information and metrics")
    parser.add_argument("-s", "--sandbox", action="store_true", default=False, help="run the program in a sandbox (for extensions whose source you do not know)")
    parser.add_argument("-r", "--recoverymode", action="store_true", default=False, help="allow you to launch the program in recovery mode")
    parser.add_argument("-dm", "--devmode", action="store_true", default=False, help="allow you to launch the program in developer mode.")

    args = parser.parse_args()
    setup_logging(args.debug)

    if args.recoverymode and args.devmode:
        logging.error("You cannot run multiple modes in the same program.")

    try:
        check_os_compatibility()
        check_python_version(['3.8'])
        check_and_install_dependencies(["requirements.txt"])
    except EnvironmentError as error:
        exit(logging.error(error))
