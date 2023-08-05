#!/usr/bin/env python3

__author__ = "João Paulo Barraca, Jevgeni Kiski"
__copyright__ = "Copyright 2018-2019, João Paulo Barraca"
__credits__ = ["Tihomir Heidelberg", "Louis Rossouw"]
__license__ = "EPL"
__maintainer__ = "João Paulo Barraca"
__email__ = "jpbarraca@gmail.com"
__status__ = "Beta"

import argparse
import sys

if sys.version_info < (3, 6,):
    print(
        "You are using Python %s.%s, but PAI requires at least Python 3.6"
        % (sys.version_info[0], sys.version_info[1])
    )
    sys.exit(-1)


def main():
    from paradox.main import main

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="specify path to an alternative configuration file",
    )

    args = parser.parse_args()

    main(args)


if __name__ == "__main__":
    from paradox.lib import help

    try:
        main()
    except ImportError as error:
        help.import_error_help(error)
